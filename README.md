# mozzie

This is a surrogate modelling package for GDSiMS.

## Installation

### Installing Python Package

```bash
python -m pip install mozzie
```

From source:
```bash
git clone https://github.com/alexeatscake/mozzie
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
