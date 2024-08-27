# **Query metadata** 📊

## 🔍 **`query_getPixels_image`**

- **Description**: Returns a DataFrame with the metadata required to retrieve data using `ee.data.getPixels`.
- **Arguments**:
  - 📍 `points`: A list of tuples with coordinates (longitude, latitude).
  - 📚 `collection`: GEE collection to query.
  - 🎨 `bands`: Image bands to query.
  - 🖼️ `edge_size`: Size of the query square.
  - 🎯 `resolution`: Resolution of the query.
- **Returns**: `pd.DataFrame` containing the metadata necessary for download.

```python
table = fastcubo.query_getPixels_image(
    points=[(-76.5, -9.5), (-76.5, -10.5), (-77.5, -10.5)],
    collection="NASA/NASADEM_HGT/001",
    bands=["elevation"],
    edge_size=128,
    resolution=90
)

print(table)
```

<style>
.scrollable-table {
    display: block;
    width: 100%;
    overflow-x: clip;
    white-space: nowrap;
    border: 1px solid #ddd;
    margin-bottom: 20px;
    border-radius: 5px;
}

table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    text-align: left;
    padding: 8px;
    border-bottom: 1px solid #ddd;
}
</style>

<div class="scrollable-table">
<table>
    <thead>
        <tr>
            <th>lon</th>
            <th>lat</th>
            <th>x</th>
            <th>y</th>
            <th>epsg</th>
            <th>collection</th>
            <th>bands</th>
            <th>edge_size</th>
            <th>resolution</th>
            <th>manifest</th>
            <th>outname</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>-76.5</td>
            <td>-9.5</td>
            <td>329583.7418991233</td>
            <td>8955272.65902687</td>
            <td>EPSG:32718</td>
            <td>NASA/NASADEM_HGT/001</td>
            <td>elevation</td>
            <td>128</td>
            <td>90</td>
            <td>{'assetId': 'NASA/NASADEM_HGT/001', 'fileFormat': 'GEO_TIFF', 'bandIds': ['elevation'], 'grid': {'dimensions': {'width': 128, 'height': 128}, 'affineTransform': {'scaleX': 90, 'shearX': 0, 'translateX': 329583.7418991233, 'shearY': 0, 'scaleY': -90, 'translateY': 8955272.65902687}, 'crsCode': 'EPSG:32718'}}</td>
            <td>NASA_NASADEM_HGT_001__0000.tif</td>
        </tr>
        <tr>
            <td>-76.5</td>
            <td>-10.5</td>
            <td>330086.6486314098</td>
            <td>8844673.258434067</td>
            <td>EPSG:32718</td>
            <td>NASA/NASADEM_HGT/001</td>
            <td>elevation</td>
            <td>128</td>
            <td>90</td>
            <td>{'assetId': 'NASA/NASADEM_HGT/001', 'fileFormat': 'GEO_TIFF', 'bandIds': ['elevation'], 'grid': {'dimensions': {'width': 128, 'height': 128}, 'affineTransform': {'scaleX': 90, 'shearX': 0, 'translateX': 330086.6486314098, 'shearY': 0, 'scaleY': -90, 'translateY': 8844673.258434067}, 'crsCode': 'EPSG:32718'}}</td>
            <td>NASA_NASADEM_HGT_001__0001.tif</td>
        </tr>
        <tr>
            <td>-77.5</td>
            <td>-10.5</td>
            <td>220598.83698345214</td>
            <td>8843976.459310157</td>
            <td>EPSG:32718</td>
            <td>NASA/NASADEM_HGT/001</td>
            <td>elevation</td>
            <td>128</td>
            <td>90</td>
            <td>{'assetId': 'NASA/NASADEM_HGT/001', 'fileFormat': 'GEO_TIFF', 'bandIds': ['elevation'], 'grid': {'dimensions': {'width': 128, 'height': 128}, 'affineTransform': {'scaleX': 90, 'shearX': 0, 'translateX': 220598.83698345214, 'shearY': 0, 'scaleY': -90, 'translateY': 8843976.459310157}, 'crsCode': 'EPSG:32718'}}</td>
            <td>NASA_NASADEM_HGT_001__0002.tif</td>
        </tr>
    </tbody>
</table>
</div>


## 📅 **`query_getPixels_imagecollection`**

- **Description**: Similar to `query_getPixels_image`, but works with image collections instead of individual images.
- **Arguments**: Adds `data_range` ⏳ to specify the date range.
- **Returns**: `pd.DataFrame` 📝 with metadata needed to download image collections.

```python
table = fastcubo.query_getPixels_imagecollection(
    point=(51.079225, 10.452173),
    collection="COPERNICUS/S2_HARMONIZED",
    bands=["B4","B3","B2"],
    data_range=["2016-06-01", "2017-07-01"],
    edge_size=128,
    resolution=10,
)

print(table)
```

<style>
.scrollable-table {
    display: block;
    width: 100%;
    overflow-x: clip;
    white-space: nowrap;
    border: 1px solid #ddd;
    margin-bottom: 20px;
    border-radius: 5px;
}

table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    text-align: left;
    padding: 8px;
    border-bottom: 1px solid #ddd;
}
</style>

<div class="scrollable-table">
<table>
    <thead>
        <tr>
            <th>lon</th>
            <th>lat</th>
            <th>x</th>
            <th>y</th>
            <th>epsg</th>
            <th>collection</th>
            <th>bands</th>
            <th>edge_size</th>
            <th>resolution</th>
            <th>img_id</th>
            <th>img_date</th>
            <th>manifest</th>
            <th>outname</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>51.079225</td>
            <td>10.452173</td>
            <td>508030.43405854504</td>
            <td>1156048.1056529859</td>
            <td>EPSG:32639</td>
            <td>COPERNICUS/S2_HARMONIZED</td>
            <td>B4, B3, B2</td>
            <td>128</td>
            <td>10</td>
            <td>COPERNICUS/S2_HARMONIZED/20160608T064632_20160608T070007_T39PVM</td>
            <td>2016-06-08 07:00:07</td>
            <td>{'assetId': 'COPERNICUS/S2_HARMONIZED/20160608T064632_20160608T070007_T39PVM', 'fileFormat': 'GEO_TIFF', 'bandIds': ['B4', 'B3', 'B2'], 'grid': {'dimensions': {'width': 128, 'height': 128}, 'affineTransform': {'scaleX': 10, 'shearX': 0, 'translateX': 508030.43405854504, 'shearY': 0, 'scaleY': -10, 'translateY': 1156048.1056529859}, 'crsCode': 'EPSG:32639'}}</td>
            <td>20160608T064632_20160608T070007_T39PVM.tif</td>
        </tr>
        <tr>
            <td>51.079225</td>
            <td>10.452173</td>
            <td>508030.43405854504</td>
            <td>1156048.1056529859</td>
            <td>EPSG:32639</td>
            <td>COPERNICUS/S2_HARMONIZED</td>
            <td>B4, B3, B2</td>
            <td>128</td>
            <td>10</td>
            <td>COPERNICUS/S2_HARMONIZED/20160608T064632_20160608T070007_T39PWM</td>
            <td>2016-06-08 07:00:07</td>
            <td>{'assetId': 'COPERNICUS/S2_HARMONIZED/20160608T064632_20160608T070007_T39PWM', 'fileFormat': 'GEO_TIFF', 'bandIds': ['B4', 'B3', 'B2'], 'grid': {'dimensions': {'width': 128, 'height': 128}, 'affineTransform': {'scaleX': 10, 'shearX': 0, 'translateX': 508030.43405854504, 'shearY': 0, 'scaleY': -10, 'translateY': 1156048.1056529859}, 'crsCode': 'EPSG:32639'}}</td>
            <td>20160608T064632_20160608T070007_T39PWM.tif</td>
        </tr>
        <tr>
            <td>51.079225</td>
            <td>10.452173</td>
            <td>508030.43405854504</td>
            <td>1156048.1056529859</td>
            <td>EPSG:32639</td>
            <td>COPERNICUS/S2_HARMONIZED</td>
            <td>B4, B3, B2</td>
            <td>128</td>
            <td>10</td>
            <td>COPERNICUS/S2_HARMONIZED/20160608T070007_20160608T103645_T39PVM</td>
            <td>2016-06-08 07:00:07</td>
            <td>{'assetId': 'COPERNICUS/S2_HARMONIZED/20160608T070007_20160608T103645_T39PVM', 'fileFormat': 'GEO_TIFF', 'bandIds': ['B4', 'B3', 'B2'], 'grid': {'dimensions': {'width': 128, 'height': 128}, 'affineTransform': {'scaleX': 10, 'shearX': 0, 'translateX': 508030.43405854504, 'shearY': 0, 'scaleY': -10, 'translateY': 1156048.1056529859}, 'crsCode': 'EPSG:32639'}}</td>
            <td>20160608T070007_20160608T103645_T39PVM.tif</td>
        </tr>
    </tbody>
</table>
</div>
