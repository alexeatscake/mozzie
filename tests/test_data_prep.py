from pathlib import Path

import pytest
import yaml

from mozzie import data_prep
from mozzie.generate import parameter_order

REPO_ROOT = Path(__file__).resolve().parent.parent
METAPOP_LOC = REPO_ROOT / "GeneralMetapop" / "build" / "gdsimsapp"
TEST_DATA_DIR = REPO_ROOT / "tests" / "test_data"


class TestReadConfig:
    def test_read_example_config(self):
        config_path = TEST_DATA_DIR / "test_config.yaml"
        config_data = yaml.safe_load(config_path.read_text())
        (set_values, to_sample, num_samples, start_index, analysis_range) = (
            data_prep.read_config(config_data)
        )

        for param in parameter_order:
            if param == "set_label":
                continue
            assert param in set_values
            assert isinstance(set_values[param], int | float)

        assert isinstance(to_sample, dict)
        for range_key in ["min", "max", "type"]:
            for param_info in to_sample.values():
                assert range_key in param_info

        assert isinstance(num_samples, int)

        assert isinstance(start_index, int)

        assert isinstance(analysis_range, dict)
        for key in ["start", "end", "step"]:
            assert key in analysis_range
            assert isinstance(analysis_range[key], int | float)

    def test_wrong_set_values(self):
        config_path = TEST_DATA_DIR / "test_config.yaml"
        config_data = yaml.safe_load(config_path.read_text())
        config_data.pop("set_values")
        with pytest.raises(ValueError, match=r"set_values"):
            data_prep.read_config(config_data)

        config_data["set_values"] = "not_a_dict"
        with pytest.raises(ValueError, match=r"dictionary"):
            data_prep.read_config(config_data)

    def test_wrong_to_sample(self):
        config_path = TEST_DATA_DIR / "test_config.yaml"
        config_data = yaml.safe_load(config_path.read_text())
        config_data.pop("to_sample")
        with pytest.raises(ValueError, match=r"to_sample"):
            data_prep.read_config(config_data)

        config_data["to_sample"] = "not_a_dict"
        with pytest.raises(ValueError, match=r"dictionary"):
            data_prep.read_config(config_data)

        config_data["to_sample"] = {
            "unknown_param": {"min": 0, "max": 1, "type": "int"}
        }
        with pytest.raises(ValueError, match=r"not recognized"):
            data_prep.read_config(config_data)

        config_data["to_sample"] = {"mu_j": "not_a_dict"}
        with pytest.raises(ValueError, match=r"dictionary"):
            data_prep.read_config(config_data)

    def test_wrong_num_samples(self):
        config_path = TEST_DATA_DIR / "test_config.yaml"
        config_data = yaml.safe_load(config_path.read_text())
        config_data["num_samples"] = -5
        with pytest.raises(ValueError, match=r"positive integer"):
            data_prep.read_config(config_data)

        config_data["num_samples"] = "not_an_int"
        with pytest.raises(ValueError, match=r"positive integer"):
            data_prep.read_config(config_data)

    def test_wrong_start_index(self):
        config_path = TEST_DATA_DIR / "test_config.yaml"
        config_data = yaml.safe_load(config_path.read_text())
        config_data["start_index"] = -1
        with pytest.raises(ValueError, match=r"non-negative integer"):
            data_prep.read_config(config_data)

        config_data["start_index"] = "not_an_int"
        with pytest.raises(ValueError, match=r"non-negative integer"):
            data_prep.read_config(config_data)

    def test_wrong_analysis_range(self):
        config_path = TEST_DATA_DIR / "test_config.yaml"
        config_data = yaml.safe_load(config_path.read_text())
        config_data.pop("analysis_range")
        with pytest.raises(ValueError, match=r"analysis_range"):
            data_prep.read_config(config_data)

        config_data["analysis_range"] = "not_a_dict"
        with pytest.raises(ValueError, match=r"dictionary"):
            data_prep.read_config(config_data)

        config_data["analysis_range"] = {"start": 0, "end": 10}
        with pytest.raises(ValueError, match=r"step"):
            data_prep.read_config(config_data)

        config_data["analysis_range"] = {
            "start": "not_a_number",
            "end": 10,
            "step": 1,
        }
        with pytest.raises(ValueError, match=r"start.+integer"):
            data_prep.read_config(config_data)


class TestLoadTestTrain:
    def test_load_test_train(self):
        config_path = TEST_DATA_DIR / "test_config.yaml"
        train_set, test_set = data_prep.load_test_train(config_path)
        assert isinstance(train_set, dict)
        assert isinstance(test_set, dict)


class TestReadValuesFromParams:
    def test_read_values_from_params(self):
        param_path = TEST_DATA_DIR / "test_params.txt"
        to_sample = ["mu_j", "mu_a"]

        sample_values = data_prep.read_values_from_params(param_path, to_sample)
        assert isinstance(sample_values, dict)
        assert sample_values["mu_j"] == 0.05
        assert sample_values["mu_a"] == 0.125
