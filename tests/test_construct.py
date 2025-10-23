import numpy as np
import pytest

from mozzie.construct import generate_parameter_samples


class TestGenerateParameterSamples:
    def test_run_with_two_parameters(self):
        to_sample = {
            "param1": {"type": "float", "min": 0.0, "max": 1.0},
            "param2": {"type": "float", "min": 10.0, "max": 20.0},
        }
        num_samples = 5
        samples = generate_parameter_samples(to_sample, num_samples, seed=42)
        assert samples.shape == (num_samples, 2)
        assert np.issubdtype(samples.dtype, np.floating)
        assert np.all(samples[:, 0] >= 0.0)
        assert np.all(samples[:, 0] <= 1.0)
        assert np.all(samples[:, 1] >= 10.0)
        assert np.all(samples[:, 1] <= 20.0)

    def test_raises_run_with_integer_parameter(self):
        to_sample = {
            "param1": {"type": "int", "min": 1, "max": 5},
        }
        num_samples = 10
        with pytest.raises(ValueError, match="Unsupported type int"):
            generate_parameter_samples(to_sample, num_samples)

    def test_raises_with_invalid_range(self):
        to_sample = {
            "param1": {"type": "float", "min": 5.0, "max": 2.0},
        }
        num_samples = 10
        with pytest.raises(ValueError, match="Invalid range for"):
            generate_parameter_samples(to_sample, num_samples)
