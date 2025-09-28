import os
import pandas as pd
# from summary.combine_single_runs_from_parent_dir import combine_single_runs_from_parent_dir
from summary import single_run, combine_runs, final_summary
from graph import graph_sequential_runs, graph_averaged_runs


# Generate summary and graphs for sequential MVT runs (e.g., DREADDS, POD experiments)
# single cohort
def process_sequential_run_data(parent_dir):
    # create clean_filtered_data.csv and run_summary.csv inside each video folder in parent_folder_path
    single_run.summarize_all_runs_from_parent(parent_dir)
    #

    # generate all_runs_summary_combined.csv file and save into parent_dir
    combined_runs = combine_runs.combine_sequential_runs(parent_dir)
    all_runs_summary_output_filepath = os.path.join(parent_dir, "all_runs_summary_combined.csv")
    combined_runs.to_csv(all_runs_summary_output_filepath, index=False)
    #

    # # if you want to save to the directory one up from parent_dir
    # grandparent_dir = os.path.dirname(parent_dir)
    # all_runs_summary_output_filepath = os.path.join(grandparent_dir, "all_runs_summary_combined.csv")
    # combined_runs.to_csv(all_runs_summary_output_filepath, index=False)
    # #

    # # Generate overall summary files
    summary_by_run = final_summary.sequential_summary_by_run(all_runs_summary_output_filepath)
    final_summary_by_run_output_filepath = os.path.join(parent_dir, "FINAL_SUMMARY_BY_RUN.csv")
    # HV wants summary by mouse as well
    summary_by_run.to_csv(final_summary_by_run_output_filepath, index=False)

    # # Generate graphs
    graph_sequential_runs.plot_AVV(combined_runs)
    graph_sequential_runs.plot_void_count(combined_runs)
    graph_sequential_runs.plot_leak_count(combined_runs)



# Generate summary and graphs for averaged MVT runs
# single cohort
def process_averaged_run_data(parent_dir):
    # create clean_filtered_data.csv and run_summary.csv inside each video folder in parent_folder_path
    single_run.summarize_all_runs_from_parent(parent_dir)

    # generate all_runs_summary_combined_unaveraged.csv and all_runs_summary_combined_averaged.csv file and save into parent_dir
    combined_runs_unaveraged, combined_runs_averaged = combine_runs.combine_averaged_runs(parent_dir)
    all_runs_summary_unaveraged_output_filepath = os.path.join(parent_dir, "all_runs_summary_combined_unaveraged.csv")
    all_runs_summary_averaged_output_filepath = os.path.join(parent_dir, "all_runs_summary_combined_averaged.csv")
    combined_runs_unaveraged.to_csv(all_runs_summary_unaveraged_output_filepath, index=False) # concatenated run_summary files from each run
    combined_runs_averaged.to_csv(all_runs_summary_averaged_output_filepath, index=False) # averages values between runs for each mouse. averaged values only in this file

    # Generate overall summary files
    summary_by_mouse = final_summary.averaged_summary(all_runs_summary_unaveraged_output_filepath)
    final_summary_by_mouse_output_filepath = os.path.join(parent_dir, "FINAL_SUMMARY_BY_MOUSE.csv")

    summary_by_mouse.to_csv(final_summary_by_mouse_output_filepath, index=False)

    # Generate graphs
    graph_averaged_runs.plot_AVV(combined_runs_averaged)
    graph_averaged_runs.plot_void_count(combined_runs_averaged)
    graph_averaged_runs.plot_leak_count(combined_runs_averaged)

#################################################################

# parent_folder_path = "../Crh_Gq_testcopy2/runs"
# process_sequential_run_data(parent_folder_path)

parent_folder_path = "../TeenF_onedrivecopy3/runs"
process_averaged_run_data(parent_folder_path)