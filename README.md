# mossie

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

This is a surragate modeling package for GDSiMS.

## Installation

### Installing Python Package

```bash
python -m pip install mossie
```

From source:
```bash
git clone https://github.com/alexeatscake/mossie
cd mossie
python -m pip install .
```


### Installing GDSiMS

GDSiMS is in a submodule of this git repo.

There is a bash script `bash_script/install_metapop.sh` which will do the installation steps for Linux.
In order to do so, you need to have `cmake` installed.

To install GDSiMS you can run:
```bash
bash bash_script/install_metapop.sh
```

If not, you can follow the instructions in the GeneralMetapop Read Me.

To run

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute.

## License

Distributed under the terms of the [MIT license](LICENSE).


<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/alexeatscake/mossie/workflows/CI/badge.svg
[actions-link]:             https://github.com/alexeatscake/mossie/actions
[pypi-link]:                https://pypi.org/project/mossie/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/mossie
[pypi-version]:             https://img.shields.io/pypi/v/mossie
<!-- prettier-ignore-end -->
