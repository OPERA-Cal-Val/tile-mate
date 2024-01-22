import pytest

from tile_mate import get_raster_from_tiles
from tile_mate.stitcher import (
    COP_100_YEARS,
    HANSEN_MOSAIC_YEARS,
    S1_TEMPORAL_BASELINE_DAYS,
    SEASONS,
)


def test_esa_world_cover():
    bounds = [-120.45, 34.85, -120.15, 35.15]
    X, _ = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2021')
    assert len(X.shape) == 3

    X, _ = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2020')
    assert len(X.shape) == 3


def test_pekel_water_occ():
    bounds = [-120.45, 34.85, -120.15, 35.15]
    X, _ = get_raster_from_tiles(bounds, tile_shortname='peckel_water_occ_2021')
    assert len(X.shape) == 3


@pytest.mark.parametrize('year', [HANSEN_MOSAIC_YEARS[k] for k in [0, 2, 4, 6, 10]])
def test_hansen_datasets(year):
    # Note only getting 1 tile - these are large datasets!
    bounds = [-120.45, 34.85, -120.15, 34.95]
    X, _ = get_raster_from_tiles(bounds, tile_shortname='hansen_annual_mosaic', year=year)
    assert len(X.shape) == 3


@pytest.mark.parametrize('season', SEASONS)
@pytest.mark.parametrize('temporal_baseline_days', S1_TEMPORAL_BASELINE_DAYS)
def test_coherence_dataset(season, temporal_baseline_days):
    # Note only getting 1 tile
    bounds = [-120.45, 34.85, -120.15, 34.95]
    X, _ = get_raster_from_tiles(
        bounds,
        tile_shortname='s1_coherence_2020',
        season=season,
        temporal_baseline_days=temporal_baseline_days,
    )
    assert len(X.shape) == 3


@pytest.mark.parametrize('year', COP_100_YEARS)
def test_cop100_dataset(year: int):
    bounds = [-120.45, 34.85, -120.15, 34.95]
    X, _ = get_raster_from_tiles(bounds, tile_shortname='cop_100_lulc_discrete', year=year)
    assert len(X.shape) == 3


def test_hand():
    bounds = [-120.45, 34.85, -120.15, 34.95]
    X, _ = get_raster_from_tiles(bounds, tile_shortname='hand')
    assert len(X.shape) == 3
