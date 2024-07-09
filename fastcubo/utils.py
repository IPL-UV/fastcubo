import io
import pathlib
from copy import deepcopy
from typing import List, Literal, Optional, Tuple

import ee
import numpy as np
import pandas as pd
import rasterio as rio
import utm


def query_utm_crs_info(lon: float, lat: float) -> Tuple[float, float, str]:
    """Converts a pair of lat, lon to UTM coordinates

    Args:
        lon (float): The longitude of the point
        lat (float): The latitude of the point
    Returns:
        Tuple[float, float, str]: The UTM coordinates and the
            EPSG code of the zone
    """
    x, y, zone, _ = utm.from_latlon(lat, lon)
    zone_epsg = f"326{zone:02d}" if lat >= 0 else f"327{zone:02d}"
    return x, y, "EPSG:" + zone_epsg


def quadsplit_manifest(manifest: dict) -> List[dict]:
    """Splits a manifest in 4 smaller manifests

    Args:
        manifest (dict): The manifest to be split

    Returns:
        List[dict]: A list of 4 manifests
    """

    # deep copy the manifest
    manifest_copy = deepcopy(manifest)
    new_width = manifest["grid"]["dimensions"]["width"] // 2
    new_height = manifest["grid"]["dimensions"]["height"] // 2
    manifest_copy["grid"]["dimensions"]["width"] = new_width
    manifest_copy["grid"]["dimensions"]["height"] = new_height

    manifests = []
    for idx in range(4):

        # Load a new manifest
        new_manifest = deepcopy(manifest_copy)

        # Set the scale
        res_x = manifest["grid"]["affineTransform"]["scaleX"]
        res_y = manifest["grid"]["affineTransform"]["scaleY"]

        # Adjust the width and height
        if idx == 0:
            add_x = 0
            add_y = 0
        if idx == 1:
            add_x = new_width * res_x
            add_y = 0
        elif idx == 2:
            add_x = 0
            add_y = new_height * res_y
        elif idx == 3:
            add_x = new_width * res_x
            add_y = new_height * res_y

        # Adjust the translation
        new_manifest["grid"]["affineTransform"]["translateX"] += add_x
        new_manifest["grid"]["affineTransform"]["translateY"] += add_y

        # Append the new manifest
        manifests.append(new_manifest)

    return manifests


def computePixels_np(
    manifest_dict: dict,
    quiet: Optional[bool] = False,
    deep_level: Optional[int] = 0,
) -> np.ndarray:
    """Implements the computePixels method from
    the Earth Engine API. If the image is too large,
    it splits the image in 4 and downloads the data
    in batches.

    Args:
        manifest_dict (dict): The manifest to be downloaded

    Returns:
        np.ndarray: The image as a numpy array
    """
    if deep_level == 5:
        raise ValueError(
            "Deep level reached 5. Aborting." f" Manifest: {manifest_dict}"
        )

    try:
        # Download the data
        data = ee.data.computePixels(manifest_dict)
        with rio.open(io.BytesIO(data)) as f:
            data_np = f.read()
    except Exception as e:
        
        # Check if the error is due to the image "not being found"
        if check_not_found_error(str(e)):
            return False        
        
        # Create a container for the data
        data_np = np.zeros(
            (
                len(manifest_dict["bandIds"]),
                manifest_dict["grid"]["dimensions"]["width"],
                manifest_dict["grid"]["dimensions"]["height"],
            )
        )

        # Split the manifest in 4
        manifest_dicts = quadsplit_manifest(manifest_dict)

        for idx, manifest_dict_batch in enumerate(manifest_dicts):
            if not quiet:
                print(f"Downloading {idx} of 4...")

            # Try to obtain the data for the batch
            dnp = computePixels_np(
                manifest_dict=manifest_dict_batch,
                quiet=quiet,
                deep_level=deep_level + 1,
            )

            # Insert the data in the container
            if idx == 0:
                data_np[:, : dnp.shape[1], : dnp.shape[2]] = dnp
            elif idx == 1:
                data_np[:, : dnp.shape[1], -dnp.shape[2] :] = dnp
            elif idx == 2:
                data_np[:, -dnp.shape[1] :, : dnp.shape[2]] = dnp
            elif idx == 3:
                data_np[:, -dnp.shape[1] :, -dnp.shape[2] :] = dnp

    return data_np


def getPixels_np(
    manifest_dict: dict,    
    deep_level: Optional[int] = 0,
    quiet: Optional[bool] = False
) -> np.ndarray:
    """Implements the getPixels method from
    the Earth Engine API. If the image is too large,
    it splits the image in 4 and downloads the data
    in batches.

    Args:
        manifest_dict (dict): The manifest to be downloaded

    Returns:
        np.ndarray: The image as a numpy array
    """
    if deep_level == 5:
        raise ValueError(
            "Deep level reached 5. Aborting." f" Manifest: {manifest_dict}"
        )

    try:
        # Download the data
        data = ee.data.getPixels(manifest_dict)

        with rio.open(io.BytesIO(data)) as f:
            data_np = f.read()

    except Exception as e:

        # Check if the error is due to the image "not being found"
        if check_not_found_error(str(e)):
            return False

        # Create a container for the data
        data_np = np.zeros(
            (
                len(manifest_dict["bandIds"]),
                manifest_dict["grid"]["dimensions"]["width"],
                manifest_dict["grid"]["dimensions"]["height"],
            )
        )

        # Split the manifest in 4
        manifest_dicts = quadsplit_manifest(manifest_dict)

        for idx, manifest_dict_batch in enumerate(manifest_dicts):
            if not quiet:
                print(f"Downloading {idx} of 4...")

            # Obtain the data for the batch
            dnp = getPixels_np(
                manifest_dict=manifest_dict_batch,
                quiet=quiet,
                deep_level=deep_level + 1,
            )

            # Insert the data in the container
            if idx == 0:
                data_np[:, : dnp.shape[1], : dnp.shape[2]] = dnp
            elif idx == 1:
                data_np[:, : dnp.shape[1], -dnp.shape[2] :] = dnp
            elif idx == 2:
                data_np[:, -dnp.shape[1] :, : dnp.shape[2]] = dnp
            elif idx == 3:
                data_np[:, -dnp.shape[1] :, -dnp.shape[2] :] = dnp

    return data_np


def getImage_batch(
    row: pd.Series,
    output_path: str,
    type: Literal["getPixels", "computePixels"],
    deep_level: Optional[int] = 0,
    quiet: Optional[bool] = False,    
) -> pathlib.Path:
    """Downloads the image from the manifest as a
    GeoTIFF file.

    Args:
        manifest_dict (dict): The manifest to be downloaded
        output_path (str): The path where the file will be saved
    """
    if not quiet:
        print(f"Downloading {row.outname}...")

    # Load the manifest
    manifest_dict = eval(row.manifest)

    # Download the data
    if type == "computePixels":
        manifest_dict["expression"] = ee.deserializer.decode(
            eval(manifest_dict["expression"])
        )
        data_np = computePixels_np(
            manifest_dict=manifest_dict,            
            deep_level=deep_level,
            quiet=quiet,
        )
    
    if type == "getPixels":
        data_np = getPixels_np(
            manifest_dict=manifest_dict,
            deep_level=deep_level,
            quiet=quiet
        )
    
    if data_np is False:
        return False

    # Save the data
    metadata_rio = {
        "driver": "GTiff",
        "count": data_np.shape[0],
        "dtype": data_np.dtype,
        "height": manifest_dict["grid"]["dimensions"]["height"],
        "width": manifest_dict["grid"]["dimensions"]["width"],
        "transform": rio.Affine(
            manifest_dict["grid"]["affineTransform"]["scaleX"],
            manifest_dict["grid"]["affineTransform"]["shearX"],
            manifest_dict["grid"]["affineTransform"]["translateX"],
            manifest_dict["grid"]["affineTransform"]["shearY"],
            manifest_dict["grid"]["affineTransform"]["scaleY"],
            manifest_dict["grid"]["affineTransform"]["translateY"],
        ),
        "crs": manifest_dict["grid"]["crsCode"],
    }

    # Create the output folder
    outfile = pathlib.Path(output_path) / (row.outname)
    outfile.parent.mkdir(parents=True, exist_ok=True)

    # Save the data
    with rio.open(outfile, "w", **metadata_rio) as dst:
        dst.write(data_np)

    return outfile


def check_not_found_error(error_msg) -> bool:
    wrong_trace_message = "not found"
    if wrong_trace_message in error_msg:
        return True
    return False
