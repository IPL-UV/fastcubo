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


def t2_worker(params: pydantic.BaseModel) -> pydantic.BaseModel:
    """Blazingly fast download of S2 images using three
    different sources: GEE and Microsoft Planetary Computer.
    Args:
        params (Task): The parameters of the task.

    Returns:
        bool: True if the download was successful
    """
    # Create the output directory
    download_path = pathlib.Path(params.download_dir)
    download_path.mkdir(parents=True, exist_ok=True)

    # Run the task
    asyncio.run(async_download_s2(params=params))

    return params


async def async_download_s2(params: pydantic.BaseModel) -> None:
    """Request S2 tiles to three different datapoints.

    Args:
        params (Task): The parameters of the task.
    """
    loop = asyncio.get_running_loop()

    # display the date range
    if not params.quiet:
        print("DateRange PC:", params.start_date[0], params.end_date[0])
        print("DateRange GEE:", params.start_date[1], params.end_date[1])

    # Download the S2 images - PC
    future1 = loop.run_in_executor(None, t2_worker_pc, params)

    # Download the S2 images - GEE
    future2 = loop.run_in_executor(None, t2_worker_gee, params)

    await asyncio.gather(future1, future2)


def t2_worker_gee(params):
    # Download Sentinel-2 data
    provider = "google"

    # Define the ImageCollection
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
        .filterDate(params.start_date[1], params.end_date[1])
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
    all_bands = [
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
        "B6",
        "B7",
        "B8",
        "B8A",
        "B9",
        "B11",
        "B12",
    ]
    download_path = pathlib.Path(params.download_dir)
    for gee_id, product_id in zip(s2_ids, s2_product_ids):
        metadata = {
            "assetId": gee_id,
            "fileFormat": "GEO_TIFF",
            "bandIds": all_bands,
            "grid": {
                "dimensions": {
                    "width": params.patch_size // 10,
                    "height": params.patch_size // 10,
                },
                "affineTransform": {
                    "scaleX": 10,
                    "shearX": 0,
                    "translateX": params.lon_utm,
                    "shearY": 0,
                    "scaleY": -10,
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


def t2_worker_pc(params):
    # Download Sentinel-2 data
    provider = "microsoft"

    # Set the STAC endpoint
    stac = "https://planetarycomputer.microsoft.com/api/stac/v1"
    CATALOG = pystac_client.Client.open(stac)

    # Search considering the central point
    top_left_coord = (params.lon, params.lat)

    # Request items from the Planetary Computer
    point = {"type": "Point", "coordinates": [params.lon, params.lat]}
    items = CATALOG.search(
        intersects=point,
        datetime=f"{params.start_date[0]}/{params.end_date[0]}",
        collections=["sentinel-2-l2a"],
        query={
            "eo:cloud_cover": {"lt": 30},
            "s2:mgrs_tile": {"eq": params.mgrs_tile},
        },
    ).item_collection()
    items = pc.sign(items)

    if len(items) == 0:
        warnings.warn("No items found in the Planetary Computer")
        return None

    # Request the items
    all_bands = [
        "B01",
        "B02",
        "B03",
        "B04",
        "B05",
        "B06",
        "B07",
        "B08",
        "B8A",
        "B09",
        "B11",
        "B12",
    ]
    cube = stackstac.stack(
        items,
        assets=all_bands,
        resolution=10,
        bounds=[
            params.lon_utm,
            params.lat_utm - params.patch_size,
            params.lon_utm + params.patch_size,
            params.lat_utm,
        ],
        epsg=int(params.crs.split(":")[1]),
    )

    # Define the affine transformation
    affine = rio.transform.from_origin(params.lon_utm, params.lat_utm, 10, 10)

    rio_meta = {
        "driver": "GTiff",
        "height": cube[0].shape[1],
        "width": cube[0].shape[2],
        "count": len(all_bands),
        "dtype": "uint16",
        "crs": params.crs,
        "transform": affine,
        "compress": "deflate",
        "tiled": True,
        "blockxsize": 256,
        "blockysize": 256,
        "nodata": 65535,
        "bigtiff": "yes",
        "interleave": "band",
        "predictor": 2,
    }

    # Define the output path
    params.download_dir = pathlib.Path(params.download_dir)
    params.download_dir.mkdir(parents=True, exist_ok=True)

    # Define the download function
    def download_s2_stacstack_patch(array, params, rio_meta):
        img_id = str(array.coords["id"].values)
        name = params.download_dir / f"microsoft__S2__{img_id}.tif"
        with rio.open(name, "w", **rio_meta) as dst:
            dst.write(array.values)

    # Using ThreadPoolExecutor to manage concurrent downloads
    with concurrent.futures.ThreadPoolExecutor(max_workers=params.nworkers) as executor:
        futures = [
            executor.submit(download_s2_stacstack_patch, array, params, rio_meta)
            for array in cube
        ]
        # If there is an exception, raise it
        for future in concurrent.futures.as_completed(futures):
            if future.exception() is not None:
                raise future.exception()


def t2_cleaner(params: pydantic.BaseModel) -> None:
    # List all the S2 L2A images
    s2files = list(params.download_dir.glob("*.tif"))
    s2files.sort()

    # if necessary, move the model to the device
    cloud_model = params.cloud_model.to(params.device)

    for s2file in s2files:
        with rio.open(s2file) as src:
            s2_img = src.read() / 10000
        s2_img_torch = torch.from_numpy(s2_img)[None].float().to(params.device)

        # padd the image in order to have a multiple of 32
        if ((s2_img_torch.shape[-1] % 32) != 0) or ((s2_img_torch.shape[-2] % 32) != 0):
            pad = (
                0,
                32 - s2_img_torch.shape[-1] % 32,
                0,
                32 - s2_img_torch.shape[-2] % 32,
            )
            s2_img_torch_pad = torch.nn.functional.pad(s2_img_torch, pad)
        else:
            s2_img_torch_pad = s2_img_torch

        with torch.no_grad():
            cloud_probs = cloud_model(s2_img_torch_pad)
            cloud_mask = cloud_probs.argmax(1).squeeze().cpu().numpy() != 0
        threshold = cloud_mask.size * params.max_cloud_cover

        if cloud_mask.sum() > threshold:
            print(f"Deleting {s2file}")
            s2file.unlink()

    return None
