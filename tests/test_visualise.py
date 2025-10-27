import warnings

import matplotlib as mpl
import numpy as np
import pandas as pd

mpl.use("Agg")  # Use non-interactive backend for testing

from mozzie import visualise


class TestPlotTotalData:
    def test_plot_total_data_runs_without_error(self):
        """Test that plot_total_data runs without throwing errors."""
        # Create sample data
        data = {
            "WW": [100, 95, 90, 85, 80],
            "WD": [0, 5, 10, 15, 20],
            "DD": [0, 0, 0, 0, 0],
            "WR": [0, 0, 0, 0, 0],
            "RR": [0, 0, 0, 0, 0],
            "DR": [0, 0, 0, 0, 0],
        }
        df = pd.DataFrame(data)

        # Suppress matplotlib warnings in testing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Should not raise any exceptions
            visualise.plot_total_data(df, "Test Plot")


class TestPlotMapScatter:
    def test_plot_map_scatter_runs_without_error(self):
        """Test that plot_map_scatter runs without throwing errors."""
        # Create sample data
        population_data = np.array([10, 20, 30, 15, 25])
        coord_information = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])

        # Suppress matplotlib warnings in testing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Should not raise any exceptions
            visualise.plot_map_scatter(
                population_data, coord_information, "Test Scatter"
            )

    def test_plot_map_scatter_with_max_population(self):
        """Test that plot_map_scatter runs with custom max_population."""
        population_data = np.array([10, 20, 30, 15, 25])
        coord_information = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])

        # Suppress matplotlib warnings in testing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Should not raise any exceptions
            visualise.plot_map_scatter(
                population_data, coord_information, "Test Scatter", max_population=50
            )


class TestPlotMapContour:
    def test_plot_map_contour_runs_without_error(self):
        """Test that plot_map_contour runs without throwing errors."""
        # Create sample data
        population_data = np.array([10, 20, 30, 15, 25])
        coord_information = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])

        # Suppress matplotlib warnings in testing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Should not raise any exceptions
            visualise.plot_map_contour(
                population_data, coord_information, "Test Contour"
            )

    def test_plot_map_contour_with_max_population(self):
        """Test that plot_map_contour runs with custom max_population."""
        population_data = np.array([10, 20, 30, 15, 25])
        coord_information = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])

        # Suppress matplotlib warnings in testing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Should not raise any exceptions
            visualise.plot_map_contour(
                population_data, coord_information, "Test Contour", max_population=50
            )


class TestPlotMapAnimation:
    def test_plot_map_animation_runs_without_error(self):
        """Test that plot_map_animation runs without throwing errors."""
        # Create sample time series data
        population_data_2d = np.array(
            [
                [10, 20, 30, 15, 25],  # Time step 0
                [15, 25, 35, 20, 30],  # Time step 1
                [20, 30, 40, 25, 35],  # Time step 2
            ]
        )
        coord_information = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])

        # Suppress matplotlib warnings in testing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Should not raise any exceptions and return animation object
            anim = visualise.plot_map_animation(
                population_data_2d, coord_information, "Test Animation"
            )
            assert anim is not None
            # Keep reference to prevent deletion warning
            del anim

    def test_plot_map_animation_with_parameters(self):
        """Test that plot_map_animation runs with custom parameters."""
        population_data_2d = np.array([[10, 20, 30, 15, 25], [15, 25, 35, 20, 30]])
        coord_information = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])

        # Suppress matplotlib warnings in testing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Should not raise any exceptions
            anim = visualise.plot_map_animation(
                population_data_2d,
                coord_information,
                "Test Animation",
                max_population=50,
                interval=100,
            )
            assert anim is not None
            # Keep reference to prevent deletion warning
            del anim
