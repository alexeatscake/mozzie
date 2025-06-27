import matplotlib.pyplot as plt
import pandas as pd


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
