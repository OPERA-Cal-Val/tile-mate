from tile_stitcher import get_raster_from_tiles


def test_api():
    bounds = [-120.45, 34.85, -120.15, 35.15]
    X, p = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2021')
    assert len(X.shape) == 3

    X, p = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2020')
    assert len(X.shape) == 3

    X, p = get_raster_from_tiles(bounds, tile_shortname='peckel_water_occ_2021')
    assert len(X.shape) == 3
