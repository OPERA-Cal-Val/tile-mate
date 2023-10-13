# tile-stitcher

This tool provides a tool to create continuous rasters of global publicly available tiles such as Pekel Occurence and ESA 10 m land cover. This is a simpler cousin of [`dem-stitcher`](https://github.com/ACCESS-Cloud-Based-InSAR/dem-stitcher) without the need for basic post-processing (e.g. fractional pixel translation and vertical datum transformations).


The API can be summarized as
```
```
The rasters are returned in the global lat/lon projection `epsg:4326` and the API assumes that bounds are supplied in this format.

# Installation

In order to easily manage dependencies, we recommend using dedicated project environments
via [Anaconda/Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).
or [Python virtual environments](https://docs.python.org/3/tutorial/venv.html).

1. Clone the repository and navigate to it in the ternmal.
2. Install the environment with `mamba env update -f environment.yaml`
3. Activate the environment `conda activate tile-stitcher`
4. Install the library with `pip`

```
python -m pip install dem_stitcher
```

Python 3.10+ is supported.

# Notebooks

We have notebooks to demonstrate common usage:

+ [Basic Demo](notebooks/Basic_Demo.ipynb)


# Datasets Supported 

The datasets supported are:

1. Pekel
2. ESA World Cover (10 m) 2020 and 2021

# Dateline support

None curently.

# For Development

This is almost identical to normal installation:

1. Clone this repo `git clone https://github.com/ACCESS-Cloud-Based-InSAR/dem-stitcher.git`
2. Navigate with your terminal to the repo.
3. Create a new environment and install requirements using `conda env update --file environment.yml` (or use [`mamba`](https://github.com/mamba-org/mamba) to speed the install up)
4. Install the package from cloned repo using `python -m pip install -e .`

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
