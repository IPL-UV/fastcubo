import pathlib
from typing import Any, List, Literal, Optional, Union

import pydantic
import torch
from fasts2.task1 import t1_worker
from fasts2.task2 import t2_cleaner, t2_worker
from fasts2.utils import fix_coordinates, load_cloud_model


class S2GoogleTask(pydantic.BaseModel):
    """Create a new download task for retrieve
    Sentinel-2 relying only in Google Earth Engine
    provider. GEE has a very good cloud masking algorithm
    so it is very simple to get cloud free images
    at any resolution. The cloud are already
    computed for each image.

    The latitude and longtitude are always aligned to the
    MGRS grid, considering the affine of the Band 1.

    Attributes:
        lat: Latitude of the point of interest.
        lon: Longtitude of the point of interest.
        start_date: Start date of the download.
        end_date: End date of the download.
        download_dir: Directory to download the images.
        max_cloud_cover: Maximum cloud cover allowed.
        resolution: Resolution of the images to
            download.
        bands: List of bands to download.
        patch_size: Size of the patch to download.
        chunk_size: Size of the chunk to download.
    """

    lat: float
    lon: float
    start_date: str
    end_date: str
    nworkers: int
    level: Literal["L1C", "L2A"]
    download_dir: Union[str, pathlib.Path]
    max_cloud_cover: float
    resolution: float
    bands: list
    patch_size: int
    quiet: bool = True

    # Optional attributes (they are estimated automatically)
    lon_utm: Optional[float] = None
    lat_utm: Optional[float] = None
    crs: Optional[str] = None
    mgrs_tile: Optional[str] = None
    s2_topleft_coords: Optional[List[float]] = None

    def fix_coordinates(self):
        return fix_coordinates(self)

    def download_s2(self):
        # Download Sentinel-2 data
        if self.quiet:
            print("Downloading Sentinel-2 data...")
        t1_worker(self)


class S2CoupledTask(pydantic.BaseModel):
    """Download Sentinel-2 L2A balancing the download
    volume between Google Earth Engine and Planetary
    Computer. The download is splitted considering the
    date range. The first part is downloaded from Planetary
    Computer and the second part from Google Earth Engine.
    This is useful since the Planetary Computer has started
    to provide Sentinel-2 data from 2015 while Google
    Earth Engine has data from 2017.

    The latitude and longtitude are always aligned to the
    MGRS grid, considering the affine of the Band 1. We
    use a cloud masking algorithm trained in CloudSEN12
    to double check the clouds in the images.
    """

    lat: float
    lon: float
    start_date: List[str]
    end_date: List[str]
    nworkers: int
    download_dir: Union[str, pathlib.Path]
    cloud_model: Any
    max_cloud_cover: float
    patch_size: int
    device: Union[str, Any] = "cpu"
    quiet: bool = True

    # Optional attributes (they are estimated automatically)
    lon_utm: Optional[float] = None
    lat_utm: Optional[float] = None
    crs: Optional[str] = None
    mgrs_tile: Optional[str] = None
    s2_topleft_coords: Optional[List[float]] = None

    @pydantic.field_validator("cloud_model")
    def check_cloud_model(cls, v):
        if not isinstance(v, torch.jit.ScriptModule):
            raise ValueError("cloud_model must be a torch.jit.ScriptModule")
        return v

    @pydantic.field_validator("device")
    def check_device(cls, v):
        if not isinstance(v, str):
            if not isinstance(v, torch.device):
                raise ValueError("device must be a string or torch.device")
        return v

    def fix_coordinates(self):
        return fix_coordinates(self)

    def download_s2(self):
        # Download Sentinel-2 data
        if self.quiet:
            print("Downloading Sentinel-2 data...")
        t2_worker(self)

        # Run the cloud model
        if self.quiet:
            print("Running the cloud model...")
        t2_cleaner(self)
