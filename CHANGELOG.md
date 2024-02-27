# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440/)
and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.9]

### Added
* Hansen datasets including `treecover_2000`, `gain`, `lossyear` (these are the tile shortnames). Information on these tiles can be found here: https://data.globalforestwatch.org/documents/941f17325a494ed78c4817f9bb20f33a/explore
* RADD Deforestation Alerts from 2022 (with shortname `radd_deforestation_alerts_2022`): https://data.globalforestwatch.org/datasets/gfw::deforestation-alerts-radd/about

### Fixed
* Test (and fix bugs) in exception handling related to tile coverage, tile sets available, and keyword arguments for certain tiles (e.g. year and season).

## [0.0.8]
* Fix typo in `pekel_water_occ_2021` and other instances of misspelled name: `peckel` --> `pekel`

## [0.0.7]
* Add python 3.12 support

## [0.0.6]
* Add python 3.9 support

## [0.0.5]
* Add height above nearest drainage from ASF Tiles: https://github.com/asjohnston-asf/agu-2022-notebooks/blob/main/hand-notebook.ipynb

## [0.0.4]
* `tile-mate` is new name of the project - old name `tile-stitcher` was too similar to existing projects on PyPI
* Uses `src` layout per: https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
* Hopefully on PyPI

## [0.0.3]
* Fixes PyPI workflow by removing unrecognized `License :: OSI Approved :: Apache 2.0' is not a valid classifier.`
* Fixes dependencies in pyproject.toml
* Updates readme installation instruction.
* Still not on PyPI due to similarity of the name

## [0.0.2]
* Fixes automated workflows
* Still not on PyPI

## [0.0.1]
(not on PyPI)

* First release of `tile_mate` with following datasets (See readme for links):
    - ESA 10m worldcover 2020 and 2021; 
    - Pekel 30m water occurence 2021; 
    - S1 coherence from 2020;  
    - Hansen annual mosaics 2000, 2013 - present
    - Cop 100m Landcover 2015-2019
* Includes CI/CD workflows (via github actions) for static analysis (ruff/flake8), release to PyPI, release to github, and integration testing.
