import random

import pytest

from tile_stitcher import get_raster_from_tiles
from tile_stitcher.stitcher import HANSEN_MOSAIC_YEARS


def test_esa_world_cover():
    bounds = [-120.45, 34.85, -120.15, 35.15]
    X, p = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2021')
    assert len(X.shape) == 3

    X, p = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2020')
    assert len(X.shape) == 3


def test_pekel_water_occ():
    bounds = [-120.45, 34.85, -120.15, 35.15]
    X, p = get_raster_from_tiles(bounds, tile_shortname='peckel_water_occ_2021')
    assert len(X.shape) == 3


@pytest.mark.parametrize("year",
                         [HANSEN_MOSAIC_YEARS[k] for k in [0, 2, 4, 6, 10]]  # random.sample(HANSEN_MOSAIC_YEARS, 3)
                         )
def test_hansen_datasets(year):
    # Note only getting 1 tile - these are large datasets!
    bounds = [-120.45, 34.85, -120.15, 34.95]
    X, p = get_raster_from_tiles(bounds, tile_shortname='hansen_annual_mosaic', year=year)
    assert len(X.shape) == 3
