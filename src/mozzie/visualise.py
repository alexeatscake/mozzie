import colorcet as cc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
from scipy.interpolate import griddata


def plot_total_data(total_data: pd.DataFrame, title: str = "Total Data") -> None:
    """
    Plot the total data for different mosquito populations.

    Args:
        total_data (pd.DataFrame): DataFrame containing the total data with columns for
            different mosquito populations.
        title (str): Title of the plot.
    """
    columns_names = {
        "WW": "Wild Type",
        "WD": "Wild + Drive",
        "DD": "Both Drive",
        "WR": "Wild + Resistance",
        "RR": "Both Resistance",
        "DR": "Drive + Resistance",
    }

    fig = plt.figure(figsize=(7, 5), tight_layout=True, dpi=200)
    ax = fig.add_subplot(111)

    for col, col_name in columns_names.items():
        if col in total_data.columns:
            ax.plot(total_data[col], label=col_name)

    ax.set_title(title)
    ax.set_xlabel("Days")
    ax.set_ylabel("Mosquito Population")

    ax.tick_params(
        axis="both",
        direction="in",
        which="both",
        top=True,
        bottom=True,
        left=True,
        right=True,
    )
    ax.minorticks_on()
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    ax.legend()
    ax.grid(True)
    fig.show()


def plot_map_scatter(
    population_data: np.ndarray,
    coord_information: np.ndarray,
    title: str = "Mosquito Population Map",
    max_population: float | None = None,
) -> None:
    """
    Generate a scatter plot of the mosquito population distribution.

    Args:
        population_data (np.ndarray): 1D array representing mosquito populations at
            different coordinates at the various sites.
        coord_information (np.ndarray): 2D array with coordinate information for the
            population data.
        title (str): Title of the heat map.
        max_population (float, optional): Maximum population value for color scaling.
            Defaults to None, which uses the maximum value from population_data.
    """
    x_coords = coord_information[:, 0]
    y_coords = coord_information[:, 1]

    if max_population is None:
        max_population = np.max(population_data)

    # Create the heat map
    fig = plt.figure(figsize=(8, 6), tight_layout=True, dpi=200)
    ax = fig.add_subplot(111)

    scatter = ax.scatter(
        x_coords,
        y_coords,
        c=population_data,
        s=50,
        cmap=cc.cm.bmw,
        vmin=0,
        vmax=np.max(population_data),
    )

    # Add colorbar
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Mosquito Population", rotation=270, labelpad=20)

    # Formatting
    ax.set_title(title)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_aspect("equal")

    fig.show()


def plot_map_contour(
    population_data: np.ndarray,
    coord_information: np.ndarray,
    title: str = "Mosquito Population Map",
    max_population: float | None = None,
) -> None:
    """
    Generate a heat map of the mosquito population distribution.

    Args:
        population_data (np.ndarray): 1D array representing mosquito populations at
            different coordinates at the various sites.
        coord_information (np.ndarray): 2D array with coordinate information for the
            population data.
        title (str): Title of the heat map.
        max_population (float, optional): Maximum population value for color scaling.
            Defaults to None, which uses the maximum value from population_data.
    """
    x_coords = coord_information[:, 0]
    y_coords = coord_information[:, 1]

    if max_population is None:
        max_population = np.max(population_data)

    # Create mesh grid for contour
    x_min, x_max = x_coords.min(), x_coords.max()
    y_min, y_max = y_coords.min(), y_coords.max()

    xi = np.linspace(x_min, x_max, 100)
    yi = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(xi, yi)

    Z = griddata((x_coords, y_coords), population_data, (X, Y), method="nearest")

    # Create the heat map
    fig = plt.figure(figsize=(8, 6), tight_layout=True, dpi=200)
    ax = fig.add_subplot(111)

    contour = ax.contourf(
        X, Y, Z, levels=np.linspace(0, max_population, 100), cmap=cc.cm.bmw
    )

    # Add colour bar
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label("Mosquito Population", rotation=270, labelpad=20)

    # Formatting
    ax.set_title(title)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_aspect("equal")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    fig.show()


def plot_map_animation(
    population_data_2d: np.ndarray,
    coord_information: np.ndarray,
    title: str = "Mosquito Population Animation",
    max_population: float | None = None,
    interval: int = 200,
) -> FuncAnimation:
    """
    Generate an animated heat map of the mosquito population distribution over time.

    Args:
        population_data_2d (np.ndarray): 2D array where each row represents populations
            at different time steps and each column represents a site.
        coord_information (np.ndarray): 2D array with coordinate information for the
            population data.
        title (str): Title of the animation.
        max_population (float, optional): Maximum population value for color scaling.
            Defaults to None, which uses the maximum value from population_data_2d.
        interval (int): Interval between frames in milliseconds.

    Returns:
        FuncAnimation: The animation object.
            This can be displayed in a Jupyter notebook using
            `IPython.display.HTML(animation.to_jshtml())`.
            It can also be saved to a file using `animation.save()`.
    """
    x_coords = coord_information[:, 0]
    y_coords = coord_information[:, 1]

    if max_population is None:
        max_population = np.max(population_data_2d)

    # Create mesh grid for contour
    x_min, x_max = x_coords.min(), x_coords.max()
    y_min, y_max = y_coords.min(), y_coords.max()

    xi = np.linspace(x_min, x_max, 100)
    yi = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(xi, yi)

    # Set up the figure and axis
    fig = plt.figure(figsize=(8, 6), tight_layout=True, dpi=200)
    ax = fig.add_subplot(111)

    # Initialize the contour plot
    Z_init = griddata(
        (x_coords, y_coords), population_data_2d[0], (X, Y), method="nearest"
    )
    contour = ax.contourf(
        X, Y, Z_init, levels=np.linspace(0, max_population, 100), cmap=cc.cm.bmw
    )

    # Add colorbar
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label("Mosquito Population", rotation=270, labelpad=20)

    # Formatting
    ax.set_title(f"{title} - Day 0")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_aspect("equal")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    def animate(frame):
        ax.clear()

        # Interpolate data for current frame
        Z = griddata(
            (x_coords, y_coords), population_data_2d[frame], (X, Y), method="nearest"
        )

        # Create new contour plot
        ax.contourf(X, Y, Z, levels=np.linspace(0, max_population, 100), cmap=cc.cm.bmw)

        # Update formatting
        ax.set_title(f"{title} - Day {frame}")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_aspect("equal")
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        return ax

    # Create animation
    return FuncAnimation(
        fig,
        animate,
        frames=population_data_2d.shape[0],
        interval=interval,
        blit=False,
        repeat=True,
    )
