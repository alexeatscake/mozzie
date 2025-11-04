# Mozzie

This is a surrogate modelling package for [GDSiMS](https://github.com/AceRNorth/gdsims) (the Gene Drive Simulator of Mosquito Spread).
This uses [AutoEmulate](https://www.autoemulate.com/) for the emulation functionality.

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

### With Coordinates

It is also possible to generate parameters using a custom set of coordinates or to generate different release sites to study spatial effects.
You can find an example configuration file in `data/generated/example_grid/example_grid_config.yaml`.
It is also possible to provide just one coordinate file and use this for every experiment.

To generate the coordinates, you can use the `build_coord_files.py` script.

```bash
python py_script/generate/build_coord_files.py data/generated/example_grid/example_grid_config.yaml
```

This will generate the coordinates in the `coords_path` specified in the configuration file.
These can then be used to generate the parameter files as before.

```bash
python py_script/generate/build_param_files.py data/generated/example_grid/example_grid_config.yaml
```

### Running the GDSiMS Model

Once you have generated the parameter files, you can run the GDSiMS model for all the experiments.
You can use the `run_full_set.py` script to run all the experiments in the contained `params` directory.
These will be then be saved in the corresponding `output_files` directory.

```bash
python py_script/generate/run_full_set.py data/generated/example/example_config.yaml
```

It is also possible to run these experiments in parallel using the `pl_run_full_set.py` script.
This defaults to 4 processes, but you can change this by setting the `WORKERS_FOR_MOZZIE` environment variable.
For example, to use 12 processes, you can run:

```bash
export WORKERS_FOR_MOZZIE=12
python py_script/generate/pl_run_full_set.py data/generated/example/example_config.yaml
```

## Surrogate Modelling

To do the modelling, you will need a lot of data.
There exists a configuration file for a fitness study in `data/generated/fitness_study/fitness_config.yaml`.

You can run the following command to generate the data for the fitness study:

```bash
export WORKERS_FOR_MOZZIE=12
python py_script/generate/build_param_files.py data/generated/fitness_study/fitness_config.yaml
python py_script/generate/pl_run_full_set.py data/generated/fitness_study/fitness_config.yaml
python py_script/data_prep/load_total_data.py data/generated/fitness_study/fitness_config.yaml
```

### Using AutoEmulate

To see the functionality of AutoEmulate, it is best to run the notebook `notebooks/fitness_autoemulate.ipynb`.

## Centre Release

An example study examining the spread of the drive gene across a spatial area is provided as an illustration.

### Centre Data Generation

An example config file already exists at `data/generated/centre_release/centre_release_config.yaml`, and an example coordinate file exists at `data/generated/centre_release/coords.csv`.
The example config file only requests 25 runs of the simulation defined on line 44 by `num_samples: 25`, which is sufficient for an example.
However, to train a usable emulator, this number should be increased.
I ran the example with 1000 runs of the simulation, which took 80 CPU-core hours to complete.

```bash
export WORKERS_FOR_MOZZIE=12
python py_script/generate/build_param_files.py data/generated/centre_release/centre_release_config.yaml
python py_script/generate/pl_run_full_set.py data/generated/centre_release/centre_release_config.yaml
python py_script/data_prep/load_total_data.py data/generated/centre_release/centre_release_config.yaml
python py_script/data_prep/load_state_data.py data/generated/centre_release/centre_release_config.yaml 460
```

This script generates the state files at a timestamp of 460, which is 360 days after the release on day 100.
This can be changed to that value, but it was chosen so that it corresponds to approximately one year after the release date.

### Building the Emulator

This is given as an example in the `notebooks/centre_release_ae.ipynb` file.

## Visualisation of the Spread

There are some tools for visualising the spread of the gene drive.
This allows the generation of an animation of the mosquito population over time.
It is also possible for it to show the prevalence of the drive gene in the population.

```py
local_data, timestamps = mozzie.parsing.read_local_data(
    "data/generated/centre_release/output_files/LocalData2000run1.txt"
)

coords = pd.read_csv(
    "data/generated/centre_release/coords.csv",
    sep="\t",
    header=0,
)[['x', 'y']].to_numpy()

pop_data = mozzie.parsing.aggregate_mosquito_data(
    local_data, "total_wild"
)
```

Once the data is prepared, the animation can be created using the following command:

```py
animation = mozzie.visualise.plot_map_animation(
    pop_data,
    coords,
    title="Wild Type Mosquito Population",
    timestamps=timestamps
)
```

It can then be visualised in a Jupyter Notebook using `HTML(animation.to_html5_video())`.
It can also be saved as a GIF file using `animation.save("wild_type_population.gif", writer="pillow", fps=5)`.

## License

Distributed under the terms of the [MIT license](LICENSE).
