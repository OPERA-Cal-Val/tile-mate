# TODO: remove this once DockerizedTopsapp is updated to pandera>=0.24.0
try:
    # Preferred location for pandera >= 0.24.0
    from pandera.pandas import Column, DataFrameSchema
except ImportError:
    # Fallback for older versions
    from pandera import Column, DataFrameSchema


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
