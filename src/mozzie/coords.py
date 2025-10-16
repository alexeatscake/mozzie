import numpy as np


def make_grid_coords(coords_set: dict) -> list[tuple[float, float]]:
    """Generate a grid of coordinates based on the x_set and y_set."""

    # Validate x_set
    if "x_set" not in coords_set or not isinstance(coords_set["x_set"], dict):
        msg = "coords_set must contain an x_set mapping."
        raise ValueError(msg)
    x_set = coords_set["x_set"]
    for k in ("min_x", "max_x", "num_x"):
        if k not in x_set:
            msg = f"x_set missing required key: {k}"
            raise ValueError(msg)

    # Validate y_set
    if "y_set" not in coords_set or not isinstance(coords_set["y_set"], dict):
        msg = "coords_set must contain a y_set mapping."
        raise ValueError(msg)
    y_set = coords_set["y_set"]
    for k in ("min_y", "max_y", "num_y"):
        if k not in y_set:
            msg = f"y_set missing required key: {k}"
            raise ValueError(msg)

    x_values = np.linspace(x_set["min_x"], x_set["max_x"], x_set["num_x"])
    y_values = np.linspace(y_set["min_y"], y_set["max_y"], y_set["num_y"])

    return [(x, y) for x in x_values for y in y_values]
