import pandas as pd
from pathlib import Path
import utils

## Folder Structure ##
# parent_folder (parent_dir)
# |=> Run1_folder
#    |=> screenshots folder
#    |=> MVT_data.csv (from MVT helper)
#    |=> squares.csv (from square screenshot + ImageJ)
#    |=> metadata.json (from MVT helper - future version)
#    |=> run_summary.csv* 
#    |=> clean_filtered_data.csv 
#    |=> MVT_video.mp4 
# |=> Run2_folder
#    |=> run_summary.csv*
# |=> etc

# * = required for script

def combine_sequential_runs(parent_dir: str):
    
    # parent_dir = Path("../../Crh_Gq/runs/")
    # parent_dir = Path("../../TeenF_onedrivecopy2/runs/")
    parent_dir = Path(parent_dir)

    all_summaries = []

    for run_dir in parent_dir.iterdir():
        if run_dir.is_dir():
            summary_file = run_dir / "run_summary.csv" # name of single run summary file from summary_single_run.py
            if summary_file.exists():
                df = pd.read_csv(summary_file)
                all_summaries.append(df)

    combined = pd.concat(all_summaries, ignore_index = True)
    combined["condition"] = combined["run"].str.split("-").str[0] # "condition column from "Run" column. specific for this sequential data wrangling, and it's a necessary column in final_summary and graphing (to have each condition be the same color)

    # print(combined)
    return combined

# simply concatenate all run_summary.csv files in all nested directories of parent_dir
def combine_averaged_runs(parent_dir: str): 
    parent_dir = Path(parent_dir)

    all_summaries = []

    for run_dir in parent_dir.iterdir():
        if run_dir.is_dir():
            summary_file = run_dir / "run_summary.csv" # name of single run summary file from summary_single_run.py
            if summary_file.exists():
                df = pd.read_csv(summary_file)
                all_summaries.append(df)

    combined_unaveraged = pd.concat(all_summaries, ignore_index = True)

    combined_averaged = combined_unaveraged.groupby("Mouse", group_keys=False).apply(lambda d: pd.Series({
        "void": d["void"].mean(),
        "leak": d["leak"].mean(),
        "weighted_avg_void_vol": utils.weighted_avg_void_vol(d),
        "group": d["group"].unique()[0],
        "cohort": d["cohort"].unique()[0]
    })).reset_index()


    # print(combined_unaveraged, "\n", combined_averaged)

    return combined_unaveraged, combined_averaged

