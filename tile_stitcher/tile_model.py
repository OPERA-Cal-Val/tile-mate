import geopandas as gpd
from pandera import Column, DataFrameSchema

TILE_SCHEMA = DataFrameSchema({
    "tile_id": Column(str, required=True),
    "url": Column(str, required=True),
    "geometry": Column(gpd.array.GeometryDtype, required=True)
})
