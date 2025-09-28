import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Average Void Volume
def plot_AVV(data): #-combined_runs_average
    mean_AVV = data["weighted_avg_void_vol"].mean()
    # print(data, mean_AVV, len(data))

    plt.figure(figsize=(6,5))

    plt.bar(0, mean_AVV, width=0.3, color="skyblue", alpha=0.7)

    colors = plt.cm.tab10.colors
    mouse_colors = {mouse: colors[i % len(colors)] for i, mouse in enumerate(data["Mouse"])}

    marker_list = ["o", "s", "D", "^"]  
    unique_cohorts = data["cohort"].unique()
    cohort_markers = {cohort: marker_list[i % len(marker_list)] for i, cohort in enumerate(unique_cohorts)}

    for i, row in data.iterrows():
        mouse = row["Mouse"]
        cohort = row["cohort"]
        plt.scatter(
            0, row["weighted_avg_void_vol"],
            color=mouse_colors[mouse],
            s=50,
            marker=cohort_markers[cohort], 
            label=f"{mouse} ({cohort})"
        )


    plt.xlim(-0.5, 0.5)
    plt.xticks([0], [data['group'][0]])
    plt.ylabel("Average Void Volume (ul)")
    plt.title("Weighted Average Void Volume per Mouse")
    plt.legend(loc="upper right", fontsize=8)
    plt.show()

def plot_void_count(data): 
    mean_void_count = data["void"].mean()
    # print(data, mean_void_count, len(data))

    plt.figure(figsize=(6,5))

    plt.bar(0, mean_void_count, width=0.3, color="skyblue", alpha=0.7)

    colors = plt.cm.tab10.colors
    mouse_colors = {mouse: colors[i % len(colors)] for i, mouse in enumerate(data["Mouse"])}

    marker_list = ["o", "s", "D", "^"]  
    unique_cohorts = data["cohort"].unique()
    cohort_markers = {cohort: marker_list[i % len(marker_list)] for i, cohort in enumerate(unique_cohorts)}

    for i, row in data.iterrows():
        mouse = row["Mouse"]
        cohort = row["cohort"]
        plt.scatter(
            0, row["void"],
            color=mouse_colors[mouse],
            s=50,
            marker=cohort_markers[cohort], 
            label=f"{mouse} ({cohort})"
        )


    plt.xlim(-0.5, 0.5)
    plt.xticks([0], [data['group'][0]])
    plt.ylabel("Average Void Count")
    plt.title("Average Void Count per Mouse")
    plt.legend(loc="upper right", fontsize=8)
    plt.show()

def plot_leak_count(data): 
    mean_leak_count = data["leak"].mean()
    # print(data, mean_leak_count, len(data))

    plt.figure(figsize=(6,5))

    plt.bar(0, mean_leak_count, width=0.3, color="skyblue", alpha=0.7)

    colors = plt.cm.tab10.colors
    mouse_colors = {mouse: colors[i % len(colors)] for i, mouse in enumerate(data["Mouse"])}

    marker_list = ["o", "s", "D", "^"]  
    unique_cohorts = data["cohort"].unique()
    cohort_markers = {cohort: marker_list[i % len(marker_list)] for i, cohort in enumerate(unique_cohorts)}

    for i, row in data.iterrows():
        mouse = row["Mouse"]
        cohort = row["cohort"]
        plt.scatter(
            0, row["leak"],
            color=mouse_colors[mouse],
            s=50,
            marker=cohort_markers[cohort], 
            label=f"{mouse} ({cohort})"
        )


    plt.xlim(-0.5, 0.5)
    plt.ylim(0)
    plt.xticks([0], [data['group'][0]])
    plt.ylabel("Average Leak Count")
    plt.title("Average Leak Count per Mouse")
    plt.legend(loc="upper right", fontsize=8)
    plt.show()