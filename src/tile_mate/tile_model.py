from pandera.pandas import Column, DataFrameSchema

TILE_SCHEMA = DataFrameSchema(
    {
        'tile_id': Column(str, required=True),
        'url': Column(str, required=True),
        'year': Column(int, required=False),
        'temporal_baseline_days': Column(int, required=False),
        'season': Column(str, required=False),
        'geometry': Column('geometry', required=True),
    }
)
