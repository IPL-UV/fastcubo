
# **Functions for images and image collections**

This section explores the functions provided by the `fastcubo` package for working with images and image collections in Google Earth Engine (GEE).

## **Introduction to `fastcubo` functions** 📚

The `fastcubo` package is designed to facilitate efficient data retrieval and processing from Google Earth Engine (GEE). It provides a set of streamlined functions specifically tailored for handling satellite imagery and geospatial data. The functions in `fastcubo` allow users to:

1. **Query metadata**: Functions like `query_getPixels_image` and `query_getPixels_imagecollection` enable users to query metadata from GEE, obtaining essential information to retrieve and analyze geospatial data efficiently.
   
2. **Process images**: With `query_computePixels_image`, users can specify complex image processing operations directly in GEE using expressions, enhancing the capability to derive more meaningful insights from satellite data.

3. **Download data**: The core functions `getPixels` and `computePixels` manage the downloading of geospatial data as GeoTIFF files, supporting both individual images and collections, with options for concurrent downloading and recursive handling of large data sets.

Below is a detailed explanation of each function, including their purpose, arguments, and return types, along with examples of their usage.

## **Main functions** 🚀

Here's a quick summary of the main functions available in the `fastcubo` package:

- **`query_getPixels_image`**: Retrieves metadata necessary for downloading individual images based on specific points and parameters.
  
- **`query_getPixels_imagecollection`**: Similar to `query_getPixels_image`, but focuses on collections of images within a specified date range.

- **`query_computePixels_image`**: Allows for more complex queries by using image expressions (e.g., mathematical operations on images) before downloading.

- **`getPixels`** and **`computePixels`**: The primary functions for downloading images or collections as GeoTIFF files. These functions handle the actual retrieval of data, leveraging metadata queried through the other functions.

By utilizing these functions, users can efficiently manage large-scale geospatial data retrieval and processing tasks, leveraging the full power of Google Earth Engine through a simplified Python interface.



