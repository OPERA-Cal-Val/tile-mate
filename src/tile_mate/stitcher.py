from functools import lru_cache
from pathlib import Path
from typing import Optional

import geopandas as gpd
import rasterio
from dem_stitcher.geojson_io import read_geojson_gzip
from dem_stitcher.merge import merge_tile_datasets_within_extent
from rasterio.errors import RasterioIOError
from shapely.geometry import box

from .exceptions import NoTileCoverage, TilesetNotSupported
from .tile_model import TILE_SCHEMA

DATA_DIR = Path(__file__).resolve().parent / 'data'
GEOJSON_DICT = {
    'pekel_water_occ_2021': 'pekel_water_occurrence_2021.geojson.zip',
    'esa_world_cover_2020': 'esa_world_cover_2020.geojson.zip',
    'esa_world_cover_2021': 'esa_world_cover_2021.geojson.zip',
    'hansen_annual_mosaic': 'hansen_landsat_mosaic_2022.geojson.zip',
    'hansen_lossyear': 'hansen_landsat_mosaic_2022.geojson.zip',
    'hansen_gain': 'hansen_landsat_mosaic_2022.geojson.zip',
    'hansen_treecover_2000': 'hansen_landsat_mosaic_2022.geojson.zip',
    's1_coherence_2020': 's1_coherence_2020.geojson.zip',
    'cop_100_lulc_discrete': 'cop_100m_lulc_discrete_classes.geojson.zip',
    'radd_deforestation_alerts_2022': 'radd_deforestation_alerts_2022.geojson.zip',
    'hand': 'asf_hand_2021.geojson.zip',
    'glad_landcover': 'glad_landcover_2020.geojson.zip',
    'glad_change': 'glad_landcover_2020.geojson.zip',
}
DATASET_SHORTNAMES = list(GEOJSON_DICT.keys())

DATASETS_WITH_YEAR = ['hansen_annual_mosaic', 'cop_100_lulc_discrete', 'glad_landcover']
HANSEN_MOSAIC_YEARS = [2000] + list(range(2013, 2023))
COP_100_YEARS = list(range(2015, 2020))
CURRENT_HANSEN_VERSION = 10
CURRENT_HANSEN_YEAR = 2022
SEASONS = ['fall', 'winter', 'spring', 'summer']
S1_TEMPORAL_BASELINE_DAYS = [6, 12, 18, 24, 36, 48]
S1_MODEL_VARIABLES = ['rho', 'tau', 'rmse']
GLAD_LANDCOVER_YEARS = [2000, 2005, 2010, 2015, 2020]


@lru_cache
def get_all_tile_data(tile_key: str) -> gpd.GeoDataFrame:
    if tile_key not in DATASET_SHORTNAMES:
        raise TilesetNotSupported
    geojson_name = GEOJSON_DICT[tile_key]
    geojson_path = DATA_DIR / geojson_name
    df_tiles = read_geojson_gzip(geojson_path)
    return df_tiles


@lru_cache
def get_tile_data(
    tile_key: str,
    year: Optional[int] = None,
    season: Optional[str] = None,
    temporal_baseline_days: Optional[str] = None,
    s1_decay_model_param: Optional[str] = None,
) -> gpd.GeoDataFrame:
    # Because tile data is cached - we need to copy it.
    df_tiles = get_all_tile_data(tile_key).copy()

    if tile_key in ['hansen_treecover_2000', 'hansen_lossyear', 'hansen_gain']:

        def toggle_hansen_url(url: str) -> str:
            url_lut = {'hansen_treecover_2000': 'treecover2000', 'hansen_lossyear': 'lossyear', 'hansen_gain': 'gain'}
            return url.replace('_last_', f'_{url_lut[tile_key]}_')

        df_tiles.url = df_tiles.url.map(toggle_hansen_url)
    if tile_key == 'glad_change':

        def update_glad_change_url(url: str) -> str:
            url_updated = url[:76] + '2000-2020change' + url[80:]
            return url_updated

        df_tiles.url = df_tiles.url.map(update_glad_change_url)

    if year is not None:
        if tile_key not in DATASETS_WITH_YEAR:
            raise ValueError('Year is only supported ' f'with {DATASETS_WITH_YEAR}')
        if tile_key == 'hansen_annual_mosaic':

            def update_hansen_landsat_mosaic_url_p(url):
                return update_hansen_landsat_mosaic_url(url, year)

            df_tiles.url = df_tiles.url.map(update_hansen_landsat_mosaic_url_p)
        if tile_key == 'glad_landcover':

            def update_glad_landcover_url(url: str, year: int = year) -> str:
                url_updated = url[:76] + f'{year}' + url[80:]
                return url_updated

            df_tiles.url = df_tiles.url.map(update_glad_landcover_url)

        if tile_key == 'cop_100_lulc_discrete':
            if year not in COP_100_YEARS:
                cop_100_years_str = list(map(str, COP_100_YEARS))
                raise ValueError(f'Year must be in {cop_100_years_str}')
            df_tiles = df_tiles[df_tiles.year == year].reset_index(drop=True)

    if year is None:
        if tile_key in DATASETS_WITH_YEAR:
            raise ValueError('Year is required for tile lookup')

    if tile_key == 's1_coherence_2020':
        if (season is None) and (s1_decay_model_param is None):
            raise ValueError(f'{tile_key} requires *both* season or s1_decay_model_param to be specified')
        # XOR of variables
        if (temporal_baseline_days is None) == (s1_decay_model_param is None):
            raise ValueError(f'{tile_key} requires either s1_decay_model_param or temporal baseline to be specified')
        if season not in SEASONS:
            raise ValueError(f'season keyword must be in {", ".join(SEASONS)}')
        if temporal_baseline_days not in [None, *S1_TEMPORAL_BASELINE_DAYS]:
            tb_days_str = list(map(str, S1_TEMPORAL_BASELINE_DAYS))
            raise ValueError(f'temporal_baseline_days must be in {", ".join(tb_days_str)}')
        if s1_decay_model_param not in [None, *S1_MODEL_VARIABLES]:
            raise ValueError(f's1_decay_model_param keyword must be in {", ".join(S1_MODEL_VARIABLES)}')
        # we need season, but we can either do temporal baseline, or variable
        ind_season = df_tiles.season == season
        # temporal baseline and season
        if temporal_baseline_days is not None:
            ind_tb = df_tiles.temporal_baseline_days == temporal_baseline_days
            total_ind = ind_tb & ind_season
            df_tiles = df_tiles[total_ind].reset_index(drop=True)
        # s1_decay_model_param
        else:
            # use 12 day temporal baseline to replace with s1_decay_model_param
            ind_tb = df_tiles.temporal_baseline_days == 12
            total_ind = ind_tb & ind_season
            df_tiles = df_tiles[total_ind].reset_index(drop=True)
            df_tiles.loc[:, 'url'] = df_tiles.loc[:, 'url'].str.replace('_COH12', f'_{s1_decay_model_param}')

    if df_tiles.empty:
        raise NoTileCoverage(f'{tile_key} has no global tiles with the parameters provided')
    return df_tiles


def update_hansen_landsat_mosaic_url(url: str, year: int):
    if year not in HANSEN_MOSAIC_YEARS:
        hansen_years_str = list(map(str, HANSEN_MOSAIC_YEARS))
        raise ValueError(f'Year must be in {", ".join(hansen_years_str)}')

    if year == 2000:
        url_updated = url.replace('last', 'first')
    elif year <= 2015:
        # Gets the "last_00N_040W.tif" portion of the url
        url_end = url[-17:]
        url_updated = (
            'https://storage.googleapis.com/earthenginepartners-hansen/' f'GFC{year}/Hansen_GFC{year}_{url_end}'
        )
    else:
        year_diff = CURRENT_HANSEN_YEAR - year
        version_updated = CURRENT_HANSEN_VERSION - year_diff
        url_updated = url.replace(str(CURRENT_HANSEN_YEAR), str(year))
        url_updated = url_updated.replace(f'v1.{CURRENT_HANSEN_VERSION}', f'v1.{version_updated}')

    return url_updated


def get_urls_from_tile_df(extent: list[float], df_tiles: gpd.GeoDataFrame) -> list[str]:
    bbox = box(*extent)
    ind_inter = df_tiles.geometry.intersects(bbox)
    df_subset = df_tiles[ind_inter].reset_index(drop=True)
    urls = df_subset.url.tolist()
    if not urls:
        raise NoTileCoverage('There are no tiles over the requested area')
    return urls


def get_additional_tile_metadata(urls: list[str], max_tile_tries: int = 10) -> dict:
    """Some tile sets may have missing data when they should not. Ideally we
    can remove said tiles from dataframe. However, in the case of Hansen
    mosiacs, these errors seem to be year-to-year e.g. 2017 where the upper left
    corner has tiles that are missing in contrast to subsequent years
    so are doing this less elegant error handling to find a *present* tile"""
    for k, url in enumerate(urls):
        if k == max_tile_tries:
            metadata = {}
            break
        try:
            with rasterio.open(url) as ds:
                tags = ds.tags()
                try:
                    cmap = {k + 1: ds.colormap(k + 1) for k in range(ds.count)}
                # no colormap in existing dataset yields a ValueError in Rasterio
                except ValueError:
                    cmap = {}
            metadata = {'tags': tags, 'colormap': cmap}
            break
        # When dataset does not exist with given url
        except RasterioIOError:
            continue
    return metadata


def get_raster_from_tiles(
    extent: list[float],
    tile_shortname: Optional[str] = None,
    df_tiles: Optional[gpd.GeoDataFrame] = None,
    year: Optional[int] = None,
    season: Optional[str] = None,
    temporal_baseline_days: Optional[int] = None,
    s1_decay_model_param: Optional[str] = None,
) -> tuple:
    if (tile_shortname is None) and (df_tiles is None):
        raise ValueError('Either "tile_shortname" or "df_tiles" must be provided')

    if (tile_shortname is not None) and (df_tiles is not None):
        raise ValueError('"tile_shortname" and "df_tiles" cannot both be provided')

    if isinstance(tile_shortname, str):
        df_tiles = get_tile_data(
            tile_shortname,
            year=year,
            temporal_baseline_days=temporal_baseline_days,
            season=season,
            s1_decay_model_param=s1_decay_model_param,
        )

    df_tiles = TILE_SCHEMA.validate(df_tiles)

    urls = df_tiles.url.tolist()
    tile_metadata = get_additional_tile_metadata(urls)

    urls_subset = get_urls_from_tile_df(extent, df_tiles)
    X_merged, p_merged = merge_tile_datasets_within_extent(urls_subset, extent)

    # Are stored in the profile for provenance
    p_merged.update(**tile_metadata)
    return X_merged, p_merged
