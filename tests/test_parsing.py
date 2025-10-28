from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from mozzie import parsing

REPO_ROOT = Path(__file__).resolve().parent.parent
TEST_DATA_DIR = REPO_ROOT / "tests" / "test_data"


class TestCastBackData:
    def test_cast_back_data_single_row(self):
        """Test casting back a single row of data."""
        # Create flattened data for one row (6 values)
        flattened_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

        result = parsing.cast_back_data(flattened_data)

        # Check the shape and column names
        assert result.shape == (1, 6)
        expected_columns = ["WW", "WD", "DD", "WR", "RR", "DR"]
        assert list(result.columns) == expected_columns

        # Check the values
        expected_values = [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]]
        pd.testing.assert_frame_equal(
            result, pd.DataFrame(expected_values, columns=expected_columns)
        )

    def test_cast_back_data_multiple_rows(self):
        """Test casting back multiple rows of data."""
        # Create flattened data for three rows (18 values total)
        flattened_data = np.array(
            [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,  # Row 1
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,  # Row 2
                13.0,
                14.0,
                15.0,
                16.0,
                17.0,
                18.0,  # Row 3
            ]
        )

        result = parsing.cast_back_data(flattened_data)

        # Check the shape and column names
        assert result.shape == (3, 6)
        expected_columns = ["WW", "WD", "DD", "WR", "RR", "DR"]
        assert list(result.columns) == expected_columns

        # Check the values
        expected_values = [
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
            [13.0, 14.0, 15.0, 16.0, 17.0, 18.0],
        ]
        pd.testing.assert_frame_equal(
            result, pd.DataFrame(expected_values, columns=expected_columns)
        )


class TestReadTotalData:
    def test_read_total_data_basic_structure(self):
        """Test that the function returns correct structure and dimensions."""
        file_path = TEST_DATA_DIR / "TotalsDataExample.txt"

        result = parsing.read_total_data(file_path)

        # Check return type
        assert isinstance(result, pd.DataFrame)

        # Check columns
        expected_columns = ["WW", "WD", "DD", "WR", "RR", "DR"]
        assert list(result.columns) == expected_columns

        # Check that index is named "Day"
        assert result.index.name == "Day"

        # Check data types - should be numeric
        for col in expected_columns:
            assert pd.api.types.is_numeric_dtype(result[col])

    def test_read_total_data_specific_values(self):
        """Test specific data values from the totals file."""
        file_path = TEST_DATA_DIR / "TotalsDataExample.txt"

        result = parsing.read_total_data(file_path)

        # Test some specific values (these would need to match actual file content)
        # Check that early days have mostly WW mosquitoes
        if 0 in result.index:
            assert result.loc[0, "WW"] > 0  # Should have wild-type mosquitoes
            # Early days should have zero or very low other types
            for col in ["WD", "DD", "WR", "RR", "DR"]:
                assert result.loc[0, col] >= 0  # Non-negative values

    def test_read_total_data_non_negative_values(self):
        """Test that all values are non-negative (population counts)."""
        file_path = TEST_DATA_DIR / "TotalsDataExample.txt"

        result = parsing.read_total_data(file_path)

        # All population counts should be non-negative
        assert (result >= 0).all().all()

    def test_read_total_data_index_sorted(self):
        """Test that the index (days) is sorted."""
        file_path = TEST_DATA_DIR / "TotalsDataExample.txt"

        result = parsing.read_total_data(file_path)

        # Index should be sorted
        assert result.index.is_monotonic_increasing

    def test_read_total_data_file_not_found(self):
        """Test error handling for non-existent file."""
        non_existent_file = TEST_DATA_DIR / "NonExistentTotalsFile.txt"

        with pytest.raises(FileNotFoundError, match="does not exist"):
            parsing.read_total_data(non_existent_file)


class TestReadLocalData:
    def test_read_local_data_basic_structure(self):
        """Test that the function returns correct structure and dimensions."""
        file_path = TEST_DATA_DIR / "LocalDataExample.txt"

        data_3d, timestamps = parsing.read_local_data(file_path)

        # Check return types
        assert isinstance(data_3d, np.ndarray)
        assert isinstance(timestamps, np.ndarray)

        # Check dimensions - should be [time, location, mozzie_type]
        assert data_3d.ndim == 3
        assert data_3d.shape[2] == 6  # 6 mozzie types: WW, WD, DD, WR, RR, DR

        # Check timestamps
        expected_timestamps = np.array(
            [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        )
        np.testing.assert_array_equal(timestamps, expected_timestamps)

        # Check that data shape matches timestamps and sites
        assert data_3d.shape[0] == len(timestamps)  # 11 time points
        assert data_3d.shape[1] == 50  # 50 sites

    def test_read_local_data_specific_values(self):
        """Test specific data values at known positions."""
        file_path = TEST_DATA_DIR / "LocalDataExample.txt"

        data_3d, timestamps = parsing.read_local_data(file_path)

        # Test some specific values from the data
        # Day 0, Site 1: [38583, 0, 0, 0, 0, 0]
        expected_day0_site1 = np.array([38583, 0, 0, 0, 0, 0])
        np.testing.assert_array_equal(data_3d[0, 0, :], expected_day0_site1)

        # Day 0, Site 5: [38710, 0, 0, 0, 0, 0]
        expected_day0_site5 = np.array([38710, 0, 0, 0, 0, 0])
        np.testing.assert_array_equal(data_3d[0, 4, :], expected_day0_site5)

        # Day 200, Site 6: [38102, 883, 0, 0, 0, 0] (first non-zero WD)
        expected_day200_site6 = np.array([38102, 883, 0, 0, 0, 0])
        time_idx = np.where(timestamps == 200)[0][0]
        np.testing.assert_array_equal(data_3d[time_idx, 5, :], expected_day200_site6)

        # Day 300, Site 6: [36677, 1368, 5, 34, 0, 0] (non-zero DD, WR)
        expected_day300_site6 = np.array([36677, 1368, 5, 34, 0, 0])
        time_idx = np.where(timestamps == 300)[0][0]
        np.testing.assert_array_equal(data_3d[time_idx, 5, :], expected_day300_site6)

        # Day 500, Site 6: [6740, 15287, 10976, 459, 16, 709] (all types present)
        expected_day500_site6 = np.array([6740, 15287, 10976, 459, 16, 709])
        time_idx = np.where(timestamps == 500)[0][0]
        np.testing.assert_array_equal(data_3d[time_idx, 5, :], expected_day500_site6)

    def test_read_local_data_all_sites_present(self):
        """Test that all expected sites are present for each timepoint."""
        file_path = TEST_DATA_DIR / "LocalDataExample.txt"

        data_3d, _timestamps = parsing.read_local_data(file_path)

        # All sites 1-50 should be present
        expected_sites = 50
        assert data_3d.shape[1] == expected_sites

        # Check that no data is completely missing (all zeros across time)
        for site_idx in range(expected_sites):
            site_data = data_3d[:, site_idx, :]
            # At least early timepoints should have data
            early_total = np.sum(site_data[0, :])
            assert early_total > 0, f"Site {site_idx + 1} has no data at day 0"

    def test_read_local_data_data_types(self):
        """Test that data has correct numeric types."""
        file_path = TEST_DATA_DIR / "LocalDataExample.txt"

        data_3d, timestamps = parsing.read_local_data(file_path)

        # Data should be numeric (float or int)
        assert np.issubdtype(data_3d.dtype, np.number)
        assert np.issubdtype(timestamps.dtype, np.number)

        # Data should be non-negative (population counts)
        assert np.all(data_3d >= 0)
        assert np.all(timestamps >= 0)

        # Timestamps should be integers
        assert np.all(timestamps == np.round(timestamps))

    def test_read_local_data_file_not_found(self):
        """Test error handling for non-existent file."""
        non_existent_file = TEST_DATA_DIR / "NonExistentFile.txt"

        with pytest.raises(FileNotFoundError, match="does not exist"):
            parsing.read_local_data(non_existent_file)

    def test_read_local_data_timestamps_sorted(self):
        """Test that timestamps are returned in sorted order."""
        file_path = TEST_DATA_DIR / "LocalDataExample.txt"

        _data_3d, timestamps = parsing.read_local_data(file_path)

        # Timestamps should be sorted
        assert np.array_equal(timestamps, np.sort(timestamps))

        # Check specific timestamps from the file
        expected_timestamps = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        np.testing.assert_array_equal(timestamps, expected_timestamps)


class TestAggregateMosquitoData:
    def test_aggregate_2d_total_drive(self):
        """Test total_drive aggregation with 2D data."""
        # Create test data: 3 sites, 6 mozzie types [WW, WD, DD, WR, RR, DR]
        data_2d = np.array(
            [
                [100, 10, 5, 2, 1, 3],  # Site 1: total_drive = 10 + 5*2 + 3 = 23
                [200, 0, 0, 0, 0, 0],  # Site 2: total_drive = 0
                [50, 20, 15, 5, 2, 8],  # Site 3: total_drive = 20 + 15*2 + 8 = 58
            ]
        )

        result = parsing.aggregate_mosquito_data(data_2d, "total_drive")

        expected = np.array([23, 0, 58])
        np.testing.assert_array_equal(result, expected)

    def test_aggregate_2d_total_wild(self):
        """Test total_wild aggregation with 2D data."""
        # Create test data: [WW, WD, DD, WR, RR, DR]
        data_2d = np.array(
            [
                [100, 10, 5, 2, 1, 3],  # Site 1: total_wild = 100*2 + 10 + 2 = 212
                [50, 0, 0, 8, 0, 0],  # Site 2: total_wild = 50*2 + 0 + 8 = 108
            ]
        )

        result = parsing.aggregate_mosquito_data(data_2d, "total_wild")

        expected = np.array([212, 108])
        np.testing.assert_array_equal(result, expected)

    def test_aggregate_2d_total_resistant(self):
        """Test total_resistant aggregation with 2D data."""
        # Create test data: [WW, WD, DD, WR, RR, DR]
        data_2d = np.array(
            [
                [100, 10, 5, 2, 1, 3],  # Site 1: total_resistant = 2 + 1*2 + 3 = 7
                [50, 0, 0, 8, 4, 0],  # Site 2: total_resistant = 8 + 4*2 + 0 = 16
            ]
        )

        result = parsing.aggregate_mosquito_data(data_2d, "total_resistant")

        expected = np.array([7, 16])
        np.testing.assert_array_equal(result, expected)

    def test_aggregate_2d_total_population(self):
        """Test total_population aggregation with 2D data."""
        # Create test data: [WW, WD, DD, WR, RR, DR]
        data_2d = np.array(
            [
                [100, 10, 5, 2, 1, 3],  # Site 1: total = 121
                [50, 0, 0, 8, 4, 0],  # Site 2: total = 62
            ]
        )

        result = parsing.aggregate_mosquito_data(data_2d, "total_population")

        expected = np.array([121, 62])
        np.testing.assert_array_equal(result, expected)

    def test_aggregate_2d_drive_frequency(self):
        """Test drive_frequency aggregation with 2D data."""
        # Create test data: [WW, WD, DD, WR, RR, DR]
        data_2d = np.array(
            [
                [40, 10, 5, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],  # No population, should default to 1
            ]
        )  # Total alleles = 110*2 = 220, drive = 10+10+0 = 20, freq = 20/220 ≈ 0.091

        result = parsing.aggregate_mosquito_data(data_2d, "drive_frequency")

        expected = np.array(
            [20 / 110, 1.0]
        )  # 20 drive alleles / 110 total alleles, default 1
        np.testing.assert_array_almost_equal(result, expected)

    def test_aggregate_2d_wild_frequency_zero_population(self):
        """Test wild_frequency with zero population defaults to 0."""
        # Create test data: [WW, WD, DD, WR, RR, DR]
        data_2d = np.array(
            [
                [40, 10, 5, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],  # No population, should default to 0
            ]
        )  # Total alleles = 110*2 = 220, wild = 80+10+0 = 90, freq = 90/220

        result = parsing.aggregate_mosquito_data(data_2d, "wild_frequency")

        expected = np.array(
            [90 / 110, 0.0]
        )  # 90 wild alleles / 110 total alleles, default 0
        np.testing.assert_array_almost_equal(result, expected)

    def test_aggregate_3d_data(self):
        """Test aggregation with 3D data [time, site, mozzie_type]."""
        # Create test data: 2 time points, 2 sites, 6 mozzie types
        data_3d = np.array(
            [
                # Time 0
                [
                    [100, 10, 5, 2, 1, 3],  # Site 1
                    [50, 0, 0, 8, 4, 0],  # Site 2
                ],
                # Time 1
                [
                    [80, 20, 10, 5, 2, 6],  # Site 1
                    [30, 5, 2, 12, 8, 1],  # Site 2
                ],
            ]
        )

        result = parsing.aggregate_mosquito_data(data_3d, "total_drive")

        # Expected: [time, site]
        expected = np.array(
            [
                [23, 0],  # Time 0: Site 1 = 10+10+3=23, Site 2 = 0+0+0=0
                [46, 10],  # Time 1: Site 1 = 20+20+6=46, Site 2 = 5+4+1=10
            ]
        )
        np.testing.assert_array_equal(result, expected)

    def test_aggregate_invalid_dimensions(self):
        """Test error handling for invalid dimensions."""
        # 1D data should raise error
        data_1d = np.array([100, 10, 5, 2, 1, 3])

        with pytest.raises(ValueError, match="Data must be 2D"):
            parsing.aggregate_mosquito_data(data_1d, "total_drive")

    def test_aggregate_invalid_mozzie_types(self):
        """Test error handling for wrong number of mozzie types."""
        # Wrong number of mozzie types (should be 6)
        data_2d = np.array(
            [
                [100, 10, 5, 2],  # Only 4 types instead of 6
            ]
        )

        with pytest.raises(ValueError, match="Last dimension must be 6"):
            parsing.aggregate_mosquito_data(data_2d, "total_drive")

    def test_aggregate_unknown_type(self):
        """Test error handling for unknown aggregation type."""
        data_2d = np.array(
            [
                [100, 10, 5, 2, 1, 3],
            ]
        )

        with pytest.raises(ValueError, match="Unknown aggregation_type"):
            parsing.aggregate_mosquito_data(data_2d, "unknown_type")

    def test_with_example_local_data(self):
        """Test aggregation functions with actual local data file."""
        file_path = TEST_DATA_DIR / "LocalDataExample.txt"

        data_3d, _timestamps = parsing.read_local_data(file_path)

        # Test total_population aggregation
        result_total_pop = parsing.aggregate_mosquito_data(data_3d, "total_population")
        assert result_total_pop.shape == (data_3d.shape[0], data_3d.shape[1])

        # Test drive_frequency aggregation
        result_drive_freq = parsing.aggregate_mosquito_data(data_3d, "drive_frequency")
        assert result_drive_freq.shape == (data_3d.shape[0], data_3d.shape[1])
