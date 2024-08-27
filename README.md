# 
<p align="center">
  <img src="https://huggingface.co/datasets/JulioContrerasH/DataMLSTAC/resolve/main/banner.png" width="100%">
</p>

<p align="center">
    <em>A Python package for efficient processing of cubic earth observation (EO) data</em> 🚀
</p>

<p align="center">
<a href='https://pypi.python.org/pypi/fastcubo'>
    <img src='https://img.shields.io/pypi/v/fastcubo.svg' alt='PyPI' />
</a>
<a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</a>
<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
<a href="https://pycqa.github.io/isort/" target="_blank">
    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="isort">
</a>
</p>

---

**GitHub**: [https://github.com/IPL-UV/fastcubo](https://github.com/IPL-UV/fastcubo) 🌐

**PyPI**: [https://pypi.org/project/fastcubo/](https://pypi.org/project/fastcubo/) 🛠️

---

## **Overview 📊**

**FastCubo** is a powerful and simple API, inspired by the [cubo](https://github.com/ESDS-Leipzig/cubo) package, designed to simplify and accelerate the process of working with Google Earth Engine (GEE) data. FastCubo offers an optimized interface for creating and managing data cubes, enabling operations up to 10 times faster than traditional methods. Whether you're working with single images, collections, or complex computations, FastCubo provides the tools you need to handle large datasets efficiently.

## **Key Features ✨**
- **Fast Image and Collection downloads**: Retrieve images and image collections from GEE with unparalleled speed, leveraging multi-threaded downloads. 📥
- **Efficient data cube management**: Split large images into smaller, manageable sub-cubes for optimized processing. 🧩
- **Compute pixels with ease**: Perform complex pixel computations directly on GEE images, with results efficiently processed and downloaded. 🖥️
- **Scalable to large datasets**: Handle large-scale data without compromising performance, thanks to advanced memory and processing optimizations. 📈

## **Installation ⚙️**
Install the latest version from PyPI:

```bash
pip install fastcubo
```

## **How to use 🛠️**


### **Download a `ee.Image` 🌍**

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

### **Download a `ee.ImageCollection` 📚**

```python
import fastcubo
import ee

ee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")

table = fastcubo.query_getPixels_imagecollection(
    point=(51.079225, 10.452173),
    collection="COPERNICUS/S2_HARMONIZED",
    bands=["B4","B3","B2"],
    data_range=["2016-06-01", "2017-07-01"],
    edge_size=128,
    resolution=10,
)
fastcubo.getPixels(table, nworkers=4, output_path="demo2")
```


### **Download a `ee.Image` Compute Pixels 🧮**

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