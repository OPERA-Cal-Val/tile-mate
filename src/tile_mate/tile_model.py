import geopandas as gpd
from pandera import Column, DataFrameSchema

TILE_SCHEMA = DataFrameSchema(
    {
        'tile_id': Column(str, required=True),
        'url': Column(str, required=True),
        'year': Column(int, required=False),
        'temporal_baseline_days': Column(int, required=False),
        'season': Column(str, required=False),
        'geometry': Column(gpd.array.GeometryDtype, required=True),
    }
)
