import asyncio
import concurrent.futures
import pathlib
import warnings

import ee
import planetary_computer as pc
import pydantic
import pystac_client
import rasterio as rio
import stackstac
import torch


def t1_worker(params: pydantic.BaseModel) -> None:
    # Create the output directory
    download_path = pathlib.Path(params.download_dir)
    download_path.mkdir(parents=True, exist_ok=True)

    # Define the ImageCollection
    if params.level == "L1C":
        ic = ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
    else:
        ic = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")

    cloudmask = ee.ImageCollection("GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED")

    # Define the point of interest
    ee_point = ee.Geometry.Point(params.lon, params.lat)

    # Filter the S2 images
    def get_cc(img):
        cloud_mask = img.select("cs").gte(0.6)
        cc_area = cloud_mask.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=ee_point.buffer(params.patch_size // 2).bounds(),
            scale=60,
        ).get("cs")
        return img.set("cc", cc_area)

    # Define the S2 ImageCollection
    s2_ic = (
        ic.filterBounds(ee_point)
        .filterDate(params.start_date, params.end_date)
        .filterMetadata("MGRS_TILE", "equals", params.mgrs_tile)
        .filterMetadata("CLOUDY_PIXEL_PERCENTAGE", "less_than", 30)
        .linkCollection(cloudmask, ["cs"])
        .map(get_cc)
    )

    # Filter based on the CloudScore+
    s2_product_ids = s2_ic.aggregate_array("PRODUCT_ID").getInfo()
    s2_ids = s2_ic.aggregate_array("system:id").getInfo()
    s2_cc_img = s2_ic.aggregate_array("cc").getInfo()

    s2_ids = [
        s2_ids[index] for index, x in enumerate(s2_cc_img) if x > params.max_cloud_cover
    ]
    s2_product_ids = [
        s2_product_ids[index]
        for index, x in enumerate(s2_cc_img)
        if x > params.max_cloud_cover
    ]

    # Create the manifest
    manifests = []
    names = []
    for gee_id, product_id in zip(s2_ids, s2_product_ids):
        metadata = {
            "assetId": gee_id,
            "fileFormat": "GEO_TIFF",
            "bandIds": params.bands,
            "grid": {
                "dimensions": {
                    "width": params.patch_size // 10,
                    "height": params.patch_size // 10,
                },
                "affineTransform": {
                    "scaleX": params.resolution,
                    "shearX": 0,
                    "translateX": params.lon_utm,
                    "shearY": 0,
                    "scaleY": -params.resolution,
                    "translateY": params.lat_utm,
                },
                "crsCode": params.crs,
            },
        }
        name = download_path / f"google__S2__{pathlib.Path(product_id).stem}.tif"
        manifests.append(metadata)
        names.append(name)

    # Convert the bytes to GeoTIFF
    def from_bytes_to_geotiff(manifest: dict, filename: str) -> str:
        bytes = ee.data.getPixels(manifest)
        with open(filename, "wb") as f:
            f.write(bytes)

    # Using ThreadPoolExecutor to manage concurrent downloads
    with concurrent.futures.ThreadPoolExecutor(max_workers=params.nworkers) as executor:
        futures = [
            executor.submit(from_bytes_to_geotiff, manifest, name)
            for manifest, name in zip(manifests, names)
        ]
        # If there is an exception, raise it
        for future in concurrent.futures.as_completed(futures):
            if future.exception() is not None:
                raise future.exception()


# send package to the pypi
# poetry build
# poetry publish
# twine upload dist/*
