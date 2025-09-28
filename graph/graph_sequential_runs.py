import pandas as pd
import matplotlib.pyplot as plt

# Average Void Volume
def plot_AVV(data): # combined summaries from all runs
    # AVG VOID VOL PLOT BY DAY
    order = data["run"].unique()
    # data["run"] = pd.Categorical(data["run"], categories=order, ordered=True)
    average_AVV = data.groupby("run", sort=False)["Avg Void Vol (ul)"].mean()

    print(average_AVV)

    condition_colors = {
        cond: color
        for  cond, color in zip(data["condition"].unique(), ["skyblue", "lightgreen", "orange"])
    }
    bar_colors = [condition_colors[r.split("-")[0]] for r in order]

    fig, ax = plt. subplots()
    average_AVV.plot(kind="bar", ax=ax, color=bar_colors, edgecolor="black", zorder=0)

    pos_map = {run: i for i, run in enumerate(order)}
    for mouse, subdf in data.groupby("Mouse"):
        xs = [pos_map[r] for r in subdf["run"]]
        ys = subdf["Avg Void Vol (ul)"].values
        ax.plot(xs, ys, marker="o", linestyle="-", color="black", alpha=0.6, zorder=2)

    ax.set_ylabel("Average Void Volume (ul)")
    ax.set_title("Average Void Volume per Run")
    # ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=0)

    plt.tight_layout()
    plt.show()

def plot_void_count(data):
    # AVG VOID VOL PLOT BY DAY
    order = data["run"].unique()
    # data["run"] = pd.Categorical(data["run"], categories=order, ordered=True)
    average_void_count = data.groupby("run", sort=False)["void"].mean()

    print(average_void_count)

    condition_colors = {
        cond: color
        for  cond, color in zip(data["condition"].unique(), ["skyblue", "lightgreen", "orange"])
    }
    bar_colors = [condition_colors[r.split("-")[0]] for r in order]

    fig, ax = plt. subplots()
    average_void_count.plot(kind="bar", ax=ax, color=bar_colors, edgecolor="black", zorder=0)

    pos_map = {run: i for i, run in enumerate(order)}
    for mouse, subdf in data.groupby("Mouse"):
        xs = [pos_map[r] for r in subdf["run"]]
        ys = subdf["void"].values
        ax.plot(xs, ys, marker="o", linestyle="-", color="black", alpha=0.6, zorder=2)

    ax.set_ylabel("Number of Voids")
    ax.set_title("Number of Voids per Run")
    # ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=0)

    plt.tight_layout()
    plt.show()

def plot_leak_count(data):
    # LEAK COUNT BY DAY
    order = data["run"].unique()
    # data["run"] = pd.Categorical(data["run"], categories=order, ordered=True)
    average_leak_count = data.groupby("run", sort=False)["leak"].mean()

    print(average_leak_count)

    condition_colors = {
        cond: color
        for  cond, color in zip(data["condition"].unique(), ["skyblue", "lightgreen", "orange"])
    }
    bar_colors = [condition_colors[r.split("-")[0]] for r in order]

    fig, ax = plt. subplots()
    average_leak_count.plot(kind="bar", ax=ax, color=bar_colors, edgecolor="black", zorder=0)

    pos_map = {run: i for i, run in enumerate(order)}
    for mouse, subdf in data.groupby("Mouse"):
        xs = [pos_map[r] for r in subdf["run"]]
        ys = subdf["leak"].values
        ax.plot(xs, ys, marker="o", linestyle="-", color="black", alpha=0.6, zorder=2)

    ax.set_ylabel("Number of Leaks")
    ax.set_title("Number of Leaks per Run")
    # ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=0)

    plt.tight_layout()
    plt.show()