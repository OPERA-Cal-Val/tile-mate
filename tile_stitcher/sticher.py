from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile

import geopandas as gpd
import rasterio.mask
from dem_stitcher.geojson_io import read_geojson_gzip
from osgeo import gdal
from shapely.geometry import box

from .exceptions import TilesetNotSupported
from .tile_model import TILE_SCHEMA

DATA_DIR = Path(__file__).resolve().parent / 'data'
GEOJSON_DICT = {
    'peckel_water_occ_2021': 'pekel_water_occurrence_2021.geojson.zip',
    'esa_world_cover_2020': 'esa_world_cover_2020.geojson.zip',
    'esa_world_cover_2021': 'esa_world_cover_2021.geojson.zip'
}
DATASET_SHORTNAMES = list(GEOJSON_DICT.keys())


gdal.UseExceptions()


@lru_cache
def get_tile_data(tile_key: str) -> gpd.GeoDataFrame:
    if tile_key not in DATASET_SHORTNAMES:
        raise TilesetNotSupported
    geojson_name = GEOJSON_DICT[tile_key]
    geojson_path = DATA_DIR / geojson_name
    df_tiles = read_geojson_gzip(geojson_path)
    return df_tiles


def crop_raster_from_bounds(image_path: Path | str, bounds: list[float]) -> tuple:
    """Bounds must be in lon/lat xmin, ymin, xmax, ymax (epsg:4326)"""
    geo = box(*bounds)
    with rasterio.open(image_path) as src:
        cropped_image, cropped_transform = rasterio.mask.mask(src, [geo], crop=True)
        p = src.profile

    p.update({"driver": "GTiff",
              "height": cropped_image.shape[1],
              "width": cropped_image.shape[2],
              "transform": cropped_transform,
              "compress": "lzw"})

    return cropped_image, p


def build_vrt_from_tile_df(extent: list[float],
                           out_vrt_path: Path | str,
                           df_tiles: gpd.GeoDataFrame
                           ) -> Path:
    bbox = box(*extent)
    ind_inter = df_tiles.geometry.intersects(bbox)
    df_subset = df_tiles[ind_inter].reset_index(drop=True)
    ds = gdal.BuildVRT(str(out_vrt_path), df_subset.url.tolist())
    del ds
    return out_vrt_path


def get_raster_from_tiles(extent: list[float],
                          tile_shortname: str = None,
                          df_tiles: gpd.GeoDataFrame = None) -> tuple:

    if (tile_shortname is None) and (df_tiles is None):
        raise ValueError('Either "tile_shortname" or "df_tiles" must be provided')

    if (tile_shortname is not None) and (df_tiles is not None):
        raise ValueError('"tile_shortname" and "df_tiles" cannot both be provided')

    if isinstance(tile_shortname, str):
        df_tiles = get_tile_data(tile_shortname)

    df_tiles = TILE_SCHEMA.validate(df_tiles)

    url_0 = df_tiles.url[0]
    with rasterio.open(url_0) as ds:
        tags = ds.tags()
        cmap = {k+1: ds.colormap(k+1) for k in range(ds.count)}

    with NamedTemporaryFile(suffix='.vrt') as tmp_vrt:
        build_vrt_from_tile_df(extent, tmp_vrt.name, df_tiles)
        X, p = crop_raster_from_bounds(tmp_vrt,
                                       extent)

    # Are stored in the profile for provenance
    p['colormap'] = cmap
    p['tags'] = tags
    return X, p
