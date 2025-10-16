from itertools import product

import pytest

from mozzie import coords


class TestMakeGridCoords:
    def test_valid_input(self):
        coords_set = {
            "x_set": {"min_x": 0, "max_x": 2, "num_x": 3},
            "y_set": {"min_y": 0, "max_y": 2, "num_y": 3},
        }
        result = coords.make_grid_coords(coords_set)
        expected = list(product([0.0, 1.0, 2.0], [0.0, 1.0, 2.0]))
        assert result == expected

    def test_rectangular_grid(self):
        coords_set = {
            "x_set": {"min_x": 1, "max_x": 3, "num_x": 3},
            "y_set": {"min_y": 3, "max_y": 6, "num_y": 4},
        }
        result = coords.make_grid_coords(coords_set)
        expected = list(product([1.0, 2.0, 3.0], [3.0, 4.0, 5.0, 6.0]))
        assert result == expected

    def test_missing_x_set(self):
        coords_set = {
            "y_set": {"min_y": 0, "max_y": 2, "num_y": 3},
        }
        with pytest.raises(ValueError, match=r"^coords_set must contain"):
            coords.make_grid_coords(coords_set)

    def test_missing_y_set(self):
        coords_set = {
            "x_set": {"min_x": 0, "max_x": 2, "num_x": 3},
        }
        with pytest.raises(ValueError, match=r"^coords_set must contain"):
            coords.make_grid_coords(coords_set)
