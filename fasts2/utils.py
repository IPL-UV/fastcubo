import ee
import pydantic

from pyproj import Transformer
from shapely.geometry import Polygon


def fix_coordinates(params: pydantic.BaseModel) -> tuple:
    # Get the projection metadata
    projection_data = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
          .filterBounds(ee.Geometry.Point(params.lon, params.lat))
          .filterDate("2021-01-01", "2021-01-31")
          .select("B1")
    )

    # Create a reference polygon
    ref_polygon = Polygon(
        (
            ee.Geometry.Point(params.lon, params.lat)
                       .buffer(params.patch_size//2)
                       .bounds()
                       .getInfo()["coordinates"][0]
        )
    )


    # Get the grids available searching in a month
    grids_available_options = projection_data.aggregate_array("MGRS_TILE").getInfo()
    grids_available = []
    for index, grid in enumerate(grids_available_options):
        if grid not in grids_available:
            grids_available.append(grid)


    # The best grid is the one with the biggest intersection
    best_grid = 0
    for grid in grids_available:
        footprint = (
            projection_data.filterMetadata("MGRS_TILE", "equals", grid)
                           .first()
                           .get("system:footprint")
                           .getInfo()
        )
        footprint_polygon = Polygon(footprint["coordinates"])

        # get the intersection area
        intersection = footprint_polygon.intersection(ref_polygon)
        if intersection.area > best_grid:
            best_tile = grid

    projection_data = (
        projection_data.filterMetadata("MGRS_TILE", "equals", best_tile)
                       .first()
                       .projection()
                       .getInfo()
    )

    # Get the CRS
    crs = projection_data["crs"]

    # Get the coordinates of the upper left corner
    ulx = projection_data["transform"][2]
    uly = projection_data["transform"][5]

    # Get the scale of the minicube
    scale_x = projection_data["transform"][0]
    scale_y = projection_data["transform"][4]

    # From WGS84 to UTM     
    transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    utm_coords = transformer.transform(params.lon, params.lat)

    # Fix the coordinates
    display_x = round((utm_coords[0] - ulx) / scale_x)
    display_y = round((utm_coords[1] - uly) / scale_y)

    # New coordinates in UTM
    new_x = ulx + display_x * scale_x
    new_y = uly + display_y * scale_y

    # New coordinates in WGS84
    transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
    new_x_geo, new_y_geo = transformer.transform(new_x, new_y)

    # S2 scene coordinates
    s2_topleft_coords = [ulx, uly]

    # Update the parameters
    params.lon_utm = new_x
    params.lat_utm = new_y
    params.lon = new_x_geo
    params.lat = new_y_geo
    params.crs = crs
    params.mgrs_tile = best_tile
    params.s2_topleft_coords = s2_topleft_coords

    return params