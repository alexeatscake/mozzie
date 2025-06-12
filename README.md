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

## Data Generation

To generate data from the GDSiMS model, you can use the scripts in `py_script/generate`.

### Example of Data Generation

To check the installation and generate some data, you can run the following command:

```bash
python py_script/generate/run_default.py
```

This will run the default configuration and generate data in the `data/generated/example` directory.

### Example with Custom Parameters

It is also possible to run a custom configuration by providing a parameter file.
You can find an example parameter file in `data/generated/example/params/example_params_1.txt`.
To run the custom configuration, you can use the following command:

```bash
python py_script/generate/run_one_experiment.py data/generated/example/params/example_params_1.txt
```

### Producing Parameters for Multiple Experiments

To train a surrogate model, you will need to generate many example experimental runs.
To produce a set of parameters for multiple experiments, you can use the `build_param_files.py` script.
This script will read a configuration file and generate parameter files for multiple experiments.
You can find an example configuration file in `data/generated/example/example_config.yaml`.
This uses Latin Hypercube Sampling to generate the parameters.

```bash
python py_script/generate/build_param_files.py data/generated/example/example_config.yaml
```

### Running the GDSiMS Model

Once you have generated the parameter files, you can run the GDSiMS model for all the experiments.
You can use the `run_full_set.py` script to run all the experiments in the contained `params` directory.
These will be then be saved in the corresponding `output_files` directory.

```bash
python py_script/generate/run_full_set.py data/generated/example
```

It is also possible to run these experiments in parallel using the `pl_run_full_set.py` script.
This as default uses 4 processes, but you can change this by setting the `WORKERS_FOR_MOZZIE` environment variable.

```bash
python py_script/generate/pl_run_full_set.py data/generated/example
```


## License

Distributed under the terms of the [MIT license](LICENSE).
