import warnings

from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = None
    warnings.warn(
        'package is not installed!\n'
        'Install in editable/develop mode via (from the top of this repo):\n'
        '   python -m pip install -e .\n',
        RuntimeWarning,
    )


from .stitcher import DATASET_SHORTNAMES, get_raster_from_tiles

__all__ = ['get_raster_from_tiles', 'DATASET_SHORTNAMES']
