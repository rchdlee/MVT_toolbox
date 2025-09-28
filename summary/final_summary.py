import os
import pandas as pd
import utils

# path_to_csv = "all_runs_combined.csv"

def sequential_summary_by_run(csv_path):
    combined_runs = pd.read_csv(csv_path) # combined.to_csv("all_runs_combined.csv", index=False)

    print(combined_runs)

    summary_rows = (
        combined_runs.groupby("run").agg({
            "leak": "mean",
            "void": "mean",
            "Avg Void Vol (ul)": "mean",
            "date": "first",
            "condition": "first",
            "cohort": "first", 
            "group": "first"
        }).reset_index()
    )

    summary_rows["Mouse"] = "AVERAGE"

    summary_rows = summary_rows[combined_runs.columns]

    summary_result_cramped = pd.concat([combined_runs, summary_rows]).sort_values(
        by=["run", "Mouse"],
        key=lambda col: col.where(col != "AVERAGE", "zzz")).reset_index(drop=True)

    blank_row = pd.DataFrame([[""] * len(summary_result_cramped.columns)],
                            columns=summary_result_cramped.columns)

    final_rows = []
    for _, group in summary_result_cramped.groupby("run", sort=False):
        final_rows.append(group)
        if group.iloc[-1]["Mouse"] == "AVERAGE":
            final_rows.append(blank_row)

    summary_result_final = pd.concat(final_rows, ignore_index=True)

    cols = list(summary_result_final.columns)
    new_order = ["run"] + [c for c in cols if c != "run"]
    summary_result_final = summary_result_final[new_order]

    print(summary_result_cramped, summary_result_final)
    # summary_result_final.to_csv("SUMMARY_FINAL.csv", index=False) # csv saved in toolbox.py
    return summary_result_final

def averaged_summary(csv_path): # combined_runs_unaveraged
    combined_unaveraged_runs = pd.read_csv(csv_path)
    print(combined_unaveraged_runs)

    summary_rows = combined_unaveraged_runs.groupby("Mouse", group_keys=False).apply(lambda d: pd.Series({
        "void": d["void"].mean(),
        "leak": d["leak"].mean(),
        "Avg Void Vol (ul)": utils.weighted_avg_void_vol(d),
        "group": d["group"].unique()[0],
        "cohort": d["cohort"].unique()[0], 
        "date": "n/a", 
    })).reset_index()

    summary_rows["run"] = "AVERAGE"

    summary_rows = summary_rows[combined_unaveraged_runs.columns]

    summary_result_cramped = pd.concat([combined_unaveraged_runs, summary_rows]).sort_values(
        by=["Mouse", "run"], 
        key=lambda col: col.where(col != "AVERAGE", "zzz")).reset_index(drop=True)

    print(summary_result_cramped)

    blank_row = pd.DataFrame([[""] * len(summary_result_cramped.columns)], 
                             columns=summary_result_cramped.columns)
    
    final_rows = []
    for _, group in summary_result_cramped.groupby("Mouse", sort=False):
        final_rows.append(group)
        if group.iloc[-1]["run"] == "AVERAGE":
            final_rows.append(blank_row)

    summary_result_final = pd.concat(final_rows, ignore_index = True)

    cols = list(summary_result_final.columns)
    new_order = ["Mouse", "run"] + [c for c in cols if c not in ("Mouse", "run")]
    summary_result_final = summary_result_final[new_order]

    print(summary_result_final)
    return summary_result_final