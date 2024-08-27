# **Download data** ⬇️

## 🌐 **`getPixels` and `computePixels`**

- **Description**: These functions download images or image collections as GeoTIFF files using `ee.data.getPixels` or `ee.data.computePixels`.
- **Arguments**:
  - 🗂️ `table`: A Data6+3Frame containing the metadata for the download.
  - ⚙️ `nworkers`: Number of threawds (workers) for concurrent downloading.
  - 🔄 `deep_level`/`max_deep_level`: Maximum depth for recursion when downloading large images.
- **Returns**: A list of paths 📂 to the downloaded GeoTIFF files.

```python
fastcubo.getPixels(table, nworkers=4, output_path="demo1") # for table in query_getPixels_image
```

<p align="center">
  <img src="https://huggingface.co/datasets/JulioContrerasH/DataMLSTAC/resolve/main/demo1.png" width="100%">
</p>

```python
fastcubo.computePixels(table, nworkers=4, output_path="demo3") # for table in query_computePixels_image
```
<p align="center">
  <img src="https://huggingface.co/datasets/JulioContrerasH/DataMLSTAC/resolve/main/demo3.png" width="100%">
</p>