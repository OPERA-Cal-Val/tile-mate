import pytest

from tile_mate import get_raster_from_tiles
from tile_mate.exceptions import NoTileCoverage, TilesetNotSupported
from tile_mate.stitcher import (
    COP_100_YEARS,
    HANSEN_MOSAIC_YEARS,
    S1_TEMPORAL_BASELINE_DAYS,
    SEASONS,
)


def test_esa_world_cover():
    """This is an extra small area because these are so large"""
    bounds = [-120.45, 34.85, -120.15, 35.15]
    X, _ = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2021')
    assert len(X.shape) == 3

    X, _ = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2020')
    assert len(X.shape) == 3


@pytest.mark.parametrize('year', [HANSEN_MOSAIC_YEARS[k] for k in [0, 2, 4, 6, 10]])
def test_hansen_mosaic_datasets(year):
    # Note only getting 1 tile - these are large datasets!
    bounds = [-120.45, 34.85, -120.15, 34.95]
    X, _ = get_raster_from_tiles(bounds, tile_shortname='hansen_annual_mosaic', year=year)
    assert len(X.shape) == 3


def test_hansen_mosaic_requires_year():
    # Note only getting 1 tile - these are large datasets!
    bounds = [-120.45, 34.85, -120.15, 34.95]
    with pytest.raises(ValueError):
        X, _ = get_raster_from_tiles(bounds, tile_shortname='hansen_annual_mosaic')


def test_valid_year_exceptions():
    bounds = [-120.45, 34.85, -120.15, 34.95]
    with pytest.raises(ValueError):
        X, _ = get_raster_from_tiles(bounds, tile_shortname='hansen_annual_mosaic', year=2002)
    with pytest.raises(ValueError):
        X, _ = get_raster_from_tiles(bounds, tile_shortname='cop_100_lulc_discrete', year=2002)


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


@pytest.mark.parametrize(
    'dataset_shortname',
    [
        'hansen_gain',
        'hansen_treecover_2000',
        'hansen_lossyear',
        'hand',
        'pekel_water_occ_2021',
        'radd_deforestation_alerts_2022',
    ],
)
def test_no_kwarg_datasets(dataset_shortname):
    if dataset_shortname == 'radd_deforestation_alerts_2022':
        # Must be in Southern hemisphere near equator; RADD has limited coverage
        bounds = [-53, -2, -52.95, -1.95]
    else:
        # Los Angeles Area
        bounds = [-120.45, 34.85, -120.15, 34.95]
    X, _ = get_raster_from_tiles(bounds, tile_shortname=dataset_shortname)
    assert len(X.shape) == 3

    # Should not allow for additional kwargs
    with pytest.raises(ValueError):
        X, _ = get_raster_from_tiles(bounds, tile_shortname=dataset_shortname, year=2000)


def test_tile_mate_exceptions():
    # Over the Atlantic ocean
    bounds = [-48, 40, -47, 41]
    with pytest.raises(NoTileCoverage):
        X, _ = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2021')

    bounds = [-120.45, 34.85, -120.15, 34.95]
    with pytest.raises(TilesetNotSupported):
        X, _ = get_raster_from_tiles(bounds, tile_shortname='foo')


def test_s1_coherence_exceptions():
    bounds = [-120.45, 34.85, -120.15, 34.95]
    # None of the necessary parameters
    with pytest.raises(ValueError):
        X, _ = get_raster_from_tiles(bounds, tile_shortname='s1_coherence_2020')

    # Wrong season
    with pytest.raises(ValueError):
        X, _ = get_raster_from_tiles(bounds, tile_shortname='s1_coherence_2020', season='foo', temporal_baseline_days=6)

    # Wrong TB
    with pytest.raises(ValueError):
        X, _ = get_raster_from_tiles(
            bounds, tile_shortname='s1_coherence_2020', season='fall', temporal_baseline_days=5
        )
