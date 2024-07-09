import concurrent.futures
import pathlib
import re
from typing import List, Optional, Tuple, Union

import ee
import pandas as pd

from fastcubo.utils import getImage_batch, query_utm_crs_info


def query_getPixels_image(
    points: List[Tuple[float, float]],
    collection: str,
    bands: List[str],
    edge_size: float,
    resolution: float,
    outnames: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Returns a DataFrame with the metadata needed to
    retrieve the data using `ee.data.getPixels`

    Args:
        points (List[Tuple[float, float]]): The centroid
            of the square to be queried.
        outnames (List[str]): The name of the output files
            to be saved.
        collection (str): The collection to be queried
        bands (List[str]): The bands to be queried
        start_date (str): The start date of the query
        end_date (str): The end date of the query
        edge_size (float): The size of the square to be queried
        resolution (float): The resolution of the query

    Returns:
        pd.DataFrame: A DataFrame with the metadata needed to
            retrieve the data using `ee.data.getPixels`
    """

    if outnames is None:
        basename = collection.replace("/", "_")
        outnames = [f"%s__%04d.tif" % (basename, i) for i in range(len(points))]

    # From EPSG to UTM
    epsg = [query_utm_crs_info(lon, lat) for lon, lat in points]
    lon_utm, lat_utm, zone_epsg = zip(*epsg)

    # Fix the center of the square to be the upper left corner
    lon_utm = [x - edge_size * resolution / 2 for x in lon_utm]
    lat_utm = [y + edge_size * resolution / 2 for y in lat_utm]

    # Create the query_table
    query_table = pd.DataFrame(
        {
            "lon": [lon for lon, _ in points],
            "lat": [lat for _, lat in points],
            "x": lon_utm,
            "y": lat_utm,
            "epsg": zone_epsg,
            "collection": collection,
            "bands": ", ".join(bands),
            "edge_size": edge_size,
            "resolution": resolution,
        }
    )

    # Add manifest to the query_table
    manifests = []
    for index, row in query_table.iterrows():
        manifest = {
            "assetId": row["collection"],
            "fileFormat": "GEO_TIFF",
            "bandIds": bands,
            "grid": {
                "dimensions": {
                    "width": row["edge_size"],
                    "height": row["edge_size"],
                },
                "affineTransform": {
                    "scaleX": row["resolution"],
                    "shearX": 0,
                    "translateX": row["x"],
                    "shearY": 0,
                    "scaleY": -row["resolution"],
                    "translateY": row["y"],
                },
                "crsCode": zone_epsg[index],
            },
        }
        manifests.append(str(manifest))
    query_table["manifest"] = manifests

    # Save the outnames
    query_table["outname"] = outnames

    return query_table


def query_getPixels_imagecollection(
    point: Tuple[float, float],
    collection: str,
    bands: List[str],
    edge_size: float,
    resolution: float,
    data_range: Tuple[str, str],
    outnames: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Returns a DataFrame with the metadata needed to
    retrieve the data using `ee.data.getPixels`

    Args:
        points (List[Tuple[float, float]]): The centroid
            of the square to be queried.
        outnames (List[str]): The name of the output files
            to be saved.
        collection (str): The collection to be queried
        bands (List[str]): The bands to be queried
        data_range (Tuple[str, str]): The range of dates to
            be queried in the format (start_date, end_date).
        edge_size (float): The size of the square to be queried
        resolution (float): The resolution of the query

    Returns:
        pd.DataFrame: A DataFrame with the metadata needed to
            retrieve the data using `ee.data.getPixels`
    """
    # From EPSG to UTM
    lon_utm, lat_utm, zone_epsg = query_utm_crs_info(*point)

    # Fix the center of the square to be the upper left corner
    lon_utm = lon_utm - edge_size * resolution / 2
    lat_utm = lat_utm + edge_size * resolution / 2

    # Get the images
    images = (
        ee.ImageCollection(collection)
        .filterBounds(ee.Geometry.Point((lon_utm, lat_utm), proj=zone_epsg))
        .filterDate(data_range[0], data_range[1])
        .select(bands)
    )

    # Get the ids and dates
    ids = images.aggregate_array("system:id").getInfo()
    dates = images.aggregate_array("system:time_start").getInfo()
    dates_str = [
        pd.to_datetime(date, unit="ms").strftime("%Y-%m-%d %H:%M:%S") for date in dates
    ]

    # Create the query_table
    query_table = pd.DataFrame(
        {
            "lon": point[0],
            "lat": point[1],
            "x": lon_utm,
            "y": lat_utm,
            "epsg": zone_epsg,
            "collection": collection,
            "bands": ", ".join(bands),
            "edge_size": edge_size,
            "resolution": resolution,
            "img_id": ids,
            "img_date": dates_str,
        }
    )

    # Add manifest to the query_table
    manifests = []
    for index, row in query_table.iterrows():
        manifest = {
            "assetId": row["img_id"],
            "fileFormat": "GEO_TIFF",
            "bandIds": bands,
            "grid": {
                "dimensions": {
                    "width": row["edge_size"],
                    "height": row["edge_size"],
                },
                "affineTransform": {
                    "scaleX": row["resolution"],
                    "shearX": 0,
                    "translateX": row["x"],
                    "shearY": 0,
                    "scaleY": -row["resolution"],
                    "translateY": row["y"],
                },
                "crsCode": row["epsg"],
            },
        }
        manifests.append(str(manifest))

    # Save the manifests
    query_table["manifest"] = manifests

    if outnames is None:
        query_table["outname"] = query_table["img_id"].apply(
            lambda x: pathlib.Path(x).stem + ".tif"
        )
    else:
        query_table["outname"] = outnames

    return query_table


def getPixels(
    table: pd.DataFrame,
    nworkers: Optional[int] = None,
    deep_level: Optional[int] = 5,
    output_path: Union[str, pathlib.Path, None] = None,
    quiet: bool = False,
) -> None:
    """Create a GeoTIFF file from a query_table

    Args:
        table (pd.DataFrame): The query_table to be downloaded
        nworkers (Optional[int], optional): The number of
            workers to be used. Defaults to None. If None,
            the download will be done sequentially.
        deep_level (Optional[int], optional): If the image
            is too big, a quadtree will be created to download
            the image in parts. This parameter defines the
            maximum deep level of the quadtree. Defaults to 5.
        output_path (Optional[str], optional): The path to save
            the file. Defaults to None.
    """

    # Save the output_path
    if output_path is None:        
        output_path = pathlib.Path(
            table.iloc[0].collection.replace("/", "_")
        )
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = pathlib.Path(output_path)

    if nworkers is None:
        results = []
        for _, row in table.iterrows():
            
            # Download the image and return the path
            result: pathlib.Path = getImage_batch(
                row=row,
                output_path=output_path,
                type="getPixels",
                deep_level=deep_level,
                quiet=quiet
            )
            
            if result is not False:
                results.append(result)
    else:
        # Using ThreadPoolExecutor to manage concurrent downloads
        with concurrent.futures.ThreadPoolExecutor(max_workers=nworkers) as executor:
            futures = [
                executor.submit(getImage_batch, row, output_path, "getPixels", quiet)
                for _, row in table.iterrows()
            ]
            # If there is an output_path, raise it
            results = []
            for future in concurrent.futures.as_completed(futures):
                if future.exception() is not None:
                    raise future.exception()
                if future.result() is not False:
                    results.append(future.result())
    return results


def query_computePixels_image(
    points: List[Tuple[float, float]],
    expression: ee.Image,
    bands: List[str],
    edge_size: float,
    resolution: float,
    outnames: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Returns a DataFrame with the metadata needed to
    retrieve the data using `ee.data.getPixels`

    Args:
        points (List[Tuple[float, float]]): The centroid
            of the square to be queried.
        outnames (List[str]): The name of the output files
            to be saved.
        collection (str): The collection to be queried
        bands (List[str]): The bands to be queried
        start_date (str): The start date of the query
        end_date (str): The end date of the query
        edge_size (float): The size of the square to be queried
        resolution (float): The resolution of the query

    Returns:
        pd.DataFrame: A DataFrame with the metadata needed to
            retrieve the data using `ee.data.getPixels`
    """
    if outnames is None:
        regex_exp = re.compile(r'"constantValue":\s*"([^"]*)"')
        product_id = re.findall(regex_exp, expression.serialize())[0]
        basename = product_id.replace("/", "_")
        outnames = [f"%s__%04d.tif" % (basename, i) for i in range(len(points))]

    # From EPSG to UTM
    epsg = [query_utm_crs_info(lon, lat) for lon, lat in points]
    lon_utm, lat_utm, zone_epsg = zip(*epsg)

    # Fix the center of the square to be the centroid
    lon_utm = [x - edge_size * resolution / 2 for x in lon_utm]
    lat_utm = [y + edge_size * resolution / 2 for y in lat_utm]

    # Create the query_table
    query_table = pd.DataFrame(
        {
            "lon": [lon for lon, _ in points],
            "lat": [lat for _, lat in points],
            "x": lon_utm,
            "y": lat_utm,
            "epsg": zone_epsg,
            "expression": expression.serialize(),
            "bands": ", ".join(bands),
            "edge_size": edge_size,
            "resolution": resolution,
        }
    )

    # Add manifest to the query_table
    manifests = []
    for index, row in query_table.iterrows():
        manifest = {
            "expression": row["expression"],
            "fileFormat": "GEO_TIFF",
            "bandIds": bands,
            "grid": {
                "dimensions": {
                    "width": row["edge_size"],
                    "height": row["edge_size"],
                },
                "affineTransform": {
                    "scaleX": row["resolution"],
                    "shearX": 0,
                    "translateX": row["x"],
                    "shearY": 0,
                    "scaleY": -row["resolution"],
                    "translateY": row["y"],
                },
                "crsCode": zone_epsg[index],
            },
        }
        manifests.append(str(manifest))
    query_table["manifest"] = manifests

    # Save the outnames
    query_table["outname"] = outnames

    return query_table


def computePixels(
    table: pd.DataFrame,
    nworkers: Optional[int] = None,
    output_path: Union[str, pathlib.Path, None] = None,
    quiet: bool = False,
) -> None:
    """Create a GeoTIFF file from a query_table

    Args:
        qtable (pd.DataFrame): The query_table to be downloaded
        output_path (Optional[str], optional): The path to save
            the file. Defaults to None.
    """

    # Save the output_path
    if output_path is None:
        output_path = pathlib.Path(".")
    else:
        output_path = pathlib.Path(output_path)

    if nworkers is None:
        results = []
        for _, row in table.iterrows():
            result = getImage_batch(row, output_path, "computePixels", quiet)
            results.append(result)
    else:
        # Using ThreadPoolExecutor to manage concurrent downloads
        with concurrent.futures.ThreadPoolExecutor(max_workers=nworkers) as executor:
            futures = [
                executor.submit(getImage_batch, row, output_path, "computePixels", quiet)
                for _, row in table.iterrows()
            ]
            # If there is an output_path, raise it
            results = []
            for future in concurrent.futures.as_completed(futures):
                if future.exception() is not None:
                    raise future.exception()
                results.append(future.result())

    return results
