# FastCubo

A simple API for `ee.data.pixels` inspired by [cubo](https://github.com/ESDS-Leipzig/cubo), designed for creating and managing data cubes up to 10 times faster.

## Installation

Install the latest version from PyPI:

```bash
pip install fastcubo
```

## How to use


Download a ee.Image

```python
import ee
import fastcubo

ee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")


table = fastcubo.query_getPixels_image(
    points=[(-76.5, -9.5), (-76.5, -10.5), (-77.5, -10.5)],
    collection="NASA/NASADEM_HGT/001",
    bands=["elevation"],
    edge_size=128,
    resolution=90
)

fastcubo.getPixels(table, nworkers=4, output_path="demo1")
```

Download a ee.ImageCollection

```python
import fastcubo
import ee

ee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")

table = fastcubo.query_getPixels_imagecollection(
    point=(51.079225, 10.452173),
    collection="COPERNICUS/S2_HARMONIZED", # Id of the GEE collection
    bands=["B4","B3","B2"], # Bands to retrieve
    data_range=["2016-06-01", "2017-07-01"], # Date range of the data
    edge_size=128, # Edge size of the cube (px)
    resolution=10, # Pixel size of the cube (m)
)
fastcubo.getPixels(table, nworkers=4, output_path="demo2")
```


Download a ee.Image Compute Pixels

```python
import fastcubo
import ee

ee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")

table = fastcubo.query_computePixels_image(
    points=[(-76.5, -9.5), (-76.5, -10.5), (-77.5, -10.5)],
    expression=ee.Image("NASA/NASADEM_HGT/001").divide(1000),
    bands=["elevation"],
    edge_size=128,
    resolution=90
)
fastcubo.computePixels(table, nworkers=4, output_path="demo3")
```