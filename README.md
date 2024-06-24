# FastCubo

A simple API for `ee.data.pixels` inspired by [cubo](https://github.com/ESDS-Leipzig/cubo), designed for creating and managing data cubes up to 10 times faster.

## Installation

Install the latest version from PyPI:

```bash
pip install cubo
```

Install cubo with the required GEE dependencies from PyPI:

```bash
pip install cubo[ee]
```

Upgrade cubo by running:

```bash
pip install -U cubo
```

Install the latest version from conda-forge:

```bash
conda install -c conda-forge cubo
```

Install the latest dev version from GitHub by running:

```bash
pip install git+https://github.com/davemlz/cubo
```


## How to use


Download a S2 data cube.

```python

import fastcubo
import ee

ee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")

table = fastcubo.query_image(
    task_id= "EU2560_E4521N3012",
    points=[(51.079225, 10.452173), (-76.5, -9.5)],
    outnames=["demo_0.tif", "demo_1.tif"],
    collection="NASA/NASADEM_HGT/001",
    bands=["elevation", "num", "swb"],
    edge_size=256,
    resolution=90
)

da = fastcubo.downloader(table=table, nworkers=8)
```

Download DEM data cube


```python
import fastcubo
import ee

ee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")

table = fastcubo.query_imagecollection(
    task_id= "EU2560_E4521N3011", # Task id
    point=(51.079225, 10.452173),
    collection="COPERNICUS/S2_HARMONIZED", # Id of the GEE collection
    bands=["B4","B3","B2"], # Bands to retrieve
    start_date="2016-06-01", # Start date of the cube
    end_date="2017-07-01", # End date of the cube
    edge_size=128, # Edge size of the cube (px)
    resolution=10, # Pixel size of the cube (m)
)

da = fastcubo.downloader(table=table, nworkers=8)    
```