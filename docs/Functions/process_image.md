# **Process image** 🖼️

## 🔍 **`query_computePixels_image`**

- **Description**: Similar to `query_getPixels_image`, but uses a GEE image expression (`ee.Image`) for more complex queries.
- **Arguments**: Adds `expression` to specify the GEE image expression.
- **Returns**: `pd.DataFrame` with metadata required to download processed images.

```python
table = fastcubo.query_computePixels_image(
    points=[(-76.5, -9.5), (-76.5, -10.5), (-77.5, -10.5)],
    expression=ee.Image("NASA/NASADEM_HGT/001").divide(1000),
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
    overflow-x: clip; /* Usa 'auto' en lugar de 'hidden' para permitir desplazamiento si es necesario */
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
