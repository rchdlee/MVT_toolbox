import os
import pandas as pd
import json
import numpy as np

import utils

## Folder Structure ##
# parent_folder
# |=> Run1_folder
#    |=> screenshots folder
#    |=> MVT_data.csv* (from MVT helper)
#    |=> squares.csv* (from square screenshot + ImageJ)
#    |=> metadata.json* (from MVT helper - future version)
#    |=> MVT_video.mp4 
# |=> Run2_folder
#    |=> etc
# |=> etc

# * = required for script

def single_run_summary(folder_path: str, run: str, date: int):
    MVT_data_file = os.path.join(folder_path, "MVT_data.csv")
    squares_data_file = os.path.join(folder_path, "squares.csv")

    MVT_data = pd.read_csv(MVT_data_file)
    squares_data = pd.read_csv(squares_data_file)

    # JSON METADATA
    with open(f"{folder_path}/metadata.json", "r") as file:
        metadata = json.load(file)
    first_mouse_enter_time = metadata["first_mouse_enter_time"]
    
    #

    square_area_cm2 = 10
    ul_per_cm2 = 25 # area in cm^2 * 25 => volume (ul)
    cutoff_time = "02:05:00"

    avg_square_area_pixels = squares_data["Area"].mean()
    pixels_per_cm2 = avg_square_area_pixels / square_area_cm2

    MVT_data_clean = MVT_data[MVT_data["Mouse"] != "stats"].copy() # without "stats"
    MVT_data_clean["Measure Delay"] = MVT_data_clean.apply(lambda row: utils.subtract_times(row["Actual Event Time (s)"], row["Actual Measure Time (s)"]), axis=1)
    MVT_data_clean["Event Latency"] = MVT_data_clean.apply(lambda row: utils.subtract_times(first_mouse_enter_time, row["Actual Event Time (s)"]), axis=1)

    all_mice = MVT_data_clean["Mouse"].unique()

    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)

    bool_mask = MVT_data_clean.apply(lambda row: utils.is_time_less_than(row["Event Latency"], cutoff_time), axis=1)
    MVT_data_clean_filtered = MVT_data_clean[bool_mask].copy() # without "stats" and without events that occur after cutoff time
    MVT_data_clean_filtered["Area cm2"] = MVT_data_clean_filtered.apply(lambda row: row["Pixel Area"] / pixels_per_cm2, axis=1) # pixels / pixels_per_cm2
    MVT_data_clean_filtered["Volume ul raw"] = MVT_data_clean_filtered.apply(lambda row: row["Area cm2"] * ul_per_cm2, axis=1) # area_cm2 * ul_per_cm2
    MVT_data_clean_filtered["Volume ul adjusted"] = MVT_data_clean_filtered.apply(lambda row: utils.adjust_volume(row["Volume ul raw"], row["Measure Delay"]), axis=1) # adjust volume for evaporation, according to Excel sheet

    # print(MVT_data_clean_filtered)

    ##############################################################

    # event_counts = MVT_data_clean_filtered.groupby(["Mouse", "Type"]).size().unstack(fill_value=0).reindex(all_mice, fill_value=0)
    event_counts = ( # to account for when there are zero leak events, still create a summary row with all 0's for leaks
        MVT_data_clean_filtered.pivot_table(
            index="Mouse",
            columns="Type",
            values="Location", # any column, doesn’t matter
            aggfunc="count",
            fill_value=0
        )
        .reindex(columns=["void", "leak"], fill_value=0)
    )
    avg_void_vol_ul = (MVT_data_clean_filtered[MVT_data_clean_filtered["Type"] == "void"].groupby("Mouse")["Volume ul adjusted"].mean())

    summary = event_counts.join(avg_void_vol_ul.rename("Avg Void Vol (ul)"))
    summary["Run"] = run
    summary["Date"] = date
    # print(event_counts, avg_void_vol_ul)
    # print(summary)


    output_file_data = os.path.join(folder_path, "clean_filtered_data.csv")
    output_file_summary = os.path.join(folder_path, "run_summary.csv")

    MVT_data_clean_filtered.to_csv(output_file_data, index=False)
    summary.to_csv(output_file_summary, index=True)

def single_run_summary_v2(folder_path: str):
    MVT_data_file = os.path.join(folder_path, "MVT_data.csv")
    squares_data_file = os.path.join(folder_path, "squares.csv")

    MVT_data = pd.read_csv(MVT_data_file)
    squares_data = pd.read_csv(squares_data_file)

    # JSON METADATA
    with open(f"{folder_path}/metadata.json", "r") as file:
        metadata = json.load(file)
    first_mouse_enter_time = metadata["first_mouse_enter_time"]
    group = metadata["group"]
    cohort = metadata["cohort"]
    date = metadata["date"]
    run = metadata["run"]
    #

    square_area_cm2 = 10
    ul_per_cm2 = 25 # area in cm^2 * 25 => volume (ul)
    cutoff_time = "02:05:00"

    avg_square_area_pixels = squares_data["Area"].mean()
    pixels_per_cm2 = avg_square_area_pixels / square_area_cm2

    MVT_data_clean = MVT_data[MVT_data["Mouse"] != "stats"].copy() # without "stats"
    MVT_data_clean["Measure Delay"] = MVT_data_clean.apply(lambda row: utils.subtract_times(row["Actual Event Time (s)"], row["Actual Measure Time (s)"]), axis=1)
    MVT_data_clean["Event Latency"] = MVT_data_clean.apply(lambda row: utils.subtract_times(first_mouse_enter_time, row["Actual Event Time (s)"]), axis=1)

    all_mice = MVT_data_clean["Mouse"].unique()

    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)

    bool_mask = MVT_data_clean.apply(lambda row: utils.is_time_less_than(row["Event Latency"], cutoff_time), axis=1)
    MVT_data_clean_filtered = MVT_data_clean[bool_mask].copy() # without "stats" and without events that occur after cutoff time
    MVT_data_clean_filtered["Area cm2"] = MVT_data_clean_filtered.apply(lambda row: row["Pixel Area"] / pixels_per_cm2, axis=1) # pixels / pixels_per_cm2
    MVT_data_clean_filtered["Volume ul raw"] = MVT_data_clean_filtered.apply(lambda row: row["Area cm2"] * ul_per_cm2, axis=1) # area_cm2 * ul_per_cm2
    MVT_data_clean_filtered["Volume ul adjusted"] = MVT_data_clean_filtered.apply(lambda row: utils.adjust_volume(row["Volume ul raw"], row["Measure Delay"]), axis=1) # adjust volume for evaporation, according to Excel sheet

    # print(MVT_data_clean_filtered)

    ##############################################################

    # event_counts = MVT_data_clean_filtered.groupby(["Mouse", "Type"]).size().unstack(fill_value=0).reindex(all_mice, fill_value=0)
    event_counts = ( # to account for when there are zero leak events, still create a summary row with all 0's for leaks
        MVT_data_clean_filtered.pivot_table(
            index="Mouse",
            columns="Type",
            values="Location", # any column, doesn’t matter
            aggfunc="count",
            fill_value=0
        )
        .reindex(columns=["void", "leak"], fill_value=0)
    )
    avg_void_vol_ul = (MVT_data_clean_filtered[MVT_data_clean_filtered["Type"] == "void"].groupby("Mouse")["Volume ul adjusted"].mean())

    summary = event_counts.join(avg_void_vol_ul.rename("Avg Void Vol (ul)"))
    summary["run"] = run
    summary["date"] = date
    summary["group"] = group
    summary["cohort"] = cohort
    # print(event_counts, avg_void_vol_ul)
    # print(summary)


    output_file_data = os.path.join(folder_path, "clean_filtered_data.csv")
    output_file_summary = os.path.join(folder_path, "run_summary.csv")

    MVT_data_clean_filtered.to_csv(output_file_data, index=False)
    summary.to_csv(output_file_summary, index=True)

def summarize_all_runs_from_parent(parent_folder: str):
    for item in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, item)

        # print(folder_path, item)
        # print(folder_path, item.split("_")[1], item.split("_")[2])

        if os.path.isdir(folder_path):
            # single_run_summary(folder_path, item.split("_")[1], item.split("_")[2]) # temp parsing folder name to get run and date. Should be part of the metadata file in the future
            # single_run_summary(folder_path, item.split("_")[1], item.split("_")[0]) # temp parsing folder name to get run and date. Should be part of the metadata file in the future

            single_run_summary_v2(folder_path) # only need folder path with complete metadata.json file