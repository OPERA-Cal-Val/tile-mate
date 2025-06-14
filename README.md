# tile-mate

[![PyPI license](https://img.shields.io/pypi/l/tile-mate.svg)](https://pypi.python.org/pypi/tile-mate/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/tile-mate.svg)](https://pypi.python.org/pypi/tile-mate/)
[![PyPI version](https://img.shields.io/pypi/v/tile-mate.svg)](https://pypi.python.org/pypi/tile-mate/)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/tile_mate)](https://anaconda.org/conda-forge/tile_mate)
[![Conda platforms](https://img.shields.io/conda/pn/conda-forge/tile_mate)](https://anaconda.org/conda-forge/tile_mate)

This library provides a tool to create continuous rasters of publicly available, global tile sets (in lat/lon) such as Pekel Occurence and ESA 10 m land cover. This is a simpler cousin of [`dem-stitcher`](https://github.com/ACCESS-Cloud-Based-InSAR/dem-stitcher) without the need for basic post-processing (e.g. fractional pixel translation and vertical datum transformations).


The API can be summarized as
```
from tile_mate import get_raster_from_tiles

bounds = [-120.55, 34.85, -120.25, 35.15]
X, p = get_raster_from_tiles(bounds, tile_shortname='esa_world_cover_2021')

# X is an c x m x n numpy array, where c is the number of channels specified by rasterio `count` metadata
# p is a dictionary (or a rasterio profile) including relevant GIS metadata; CRS is assumed to be epsg:4326
```

The rasters are returned in the global lat/lon projection `epsg:4326` and the API assumes that bounds are supplied in this format.

```
import rasterio

with rasterio.open('esa_world_cover_2021_subset.tif', 'w', **p) as ds:
   ds.write(X)
```

# Installation

In order to easily manage dependencies, we recommend using dedicated project environments
via [Anaconda/Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
or [Python virtual environments](https://docs.python.org/3/tutorial/venv.html).

You can install the package with `conda`/`mamba` using:
```
mamba install tile_mate
```
or
```
pip install tile-mate
```
Alternatively, you can clone the repository and manage the environment using the `environment.yml` file provided.

1. `mamba env update -f environment.yml`
2. Activate the environment `conda activate tile-mate`
3. Install the library with `pip` via `pip install tile-mate`.

For development, use `pip` with `-e` (editable) mode:
```
python -m pip install -e .
```

Python 3.9+ is supported.

# Notebooks

We have notebooks to demonstrate common usage:

+ [Basic Demo](notebooks/Basic_Demo.ipynb)


# Datasets Supported 

There are numerous tile sets. There are keyword arguments for many of the tiles. For example, for `hansen_annual_mosaic` the years 2013-2022 can be specified. The easiest way to see what is possible is to look at the [Basic Demo](notebooks/Basic_Demo.ipynb). The datasets supported are:

```
In [1]: from tile_mate.stitcher import DATASET_SHORTNAMES

In [2]: DATASET_SHORTNAMES
Out[2]: 'pekel_water_occ_2021',
 'esa_world_cover_2020',
 'esa_world_cover_2021',
 'hansen_annual_mosaic',
 'hansen_lossyear',
 'hansen_gain',
 'hansen_treecover_2000',
 's1_coherence_2020',
 'cop_100_lulc_discrete',
 'radd_deforestation_alerts_2022',
 'hand',
 'glad_landcover',
 'glad_change'
```
More information about these datasets can be found below
+ Pekel water occurence: https://global-surface-water.appspot.com/download
+ ESA World Cover (10 m) for 2020 and 2021: https://aws.amazon.com/marketplace/pp/prodview-7oorylcamixxc
+ Hansen annual mosaic, treecover 2000, gain, and loss year: https://data.globalforestwatch.org/documents/941f17325a494ed78c4817f9bb20f33a/explore
+ S1 Coherence from December 2019 - Nov 2020: https://aws.amazon.com/marketplace/pp/prodview-iz6lnjbdlgcwa#resources
  + Include all temporal baselines and seasons for VV coherence
  + Include `rho`, `tau` and `rmse` seasonal decay modeling parameters 
+ The copernicus 100 m LULC dataset from 2015 - 2019: https://land.copernicus.eu/global/content/annual-100m-global-land-cover-maps-available
+ Height above nearest drainage (distributed and generated by ASF) in 2021 derived from Copernicus Global DEM: https://github.com/asjohnston-asf/agu-2022-notebooks/blob/main/hand-notebook.ipynb (and their [tool](https://github.com/HydroSAR/HydroSAR/blob/develop/src/hydrosar/hand/prepare.py) to do the exact same thing)
+ RADD Deforestation alerts (ongoing): https://data.globalforestwatch.org/datasets/gfw::deforestation-alerts-radd/about
+ Glad landcover maps (2000, 2005, 2010, 2015, 2020) and change map (2020 changes when compared to 2000): https://storage.googleapis.com/earthenginepartners-hansen/GLCLU2000-2020/v2/download.html

See these [notebooks](notebooks/tile_creation) to see how these tiles are generated and organized. Feel free to open a issue ticket or PR if there are modifications or new tilesets you would like to see.

# Dateline support

None curently.

# Contributing

We welcome contributions to this open-source package. To do so:

1. Create an GitHub issue ticket desrcribing what changes you need (e.g. issue-1)
2. Fork this repo
3. Make your modifications in your own fork
4. Make a pull-request (PR) in this repo with the code in your fork and tag the repo owner or a relevant contributor.

We use `flake8` and associated linting packages to ensure some basic code quality (see the `environment.yml`). These will be checked for each commit in a PR. Try to write tests wherever possible.

# Support

1. Create an GitHub issue ticket desrcribing what changes you would like to see or to report a bug.
2. We will work on solving this issue (hopefully with you).

# Acknowledgements

This tool was developed to support [OPERA](https://www.jpl.nasa.gov/go/opera).
