import pandas as pd
from pathlib import Path

import matplotlib.pyplot as plt
# import seaborn as sns

# parent_dir = Path("../Crh_Gq/runs/")
parent_dir = Path("../TeenF_onedrivecopy2/runs/")

all_summaries = []

for run_dir in parent_dir.iterdir():
    if run_dir.is_dir():
        summary_file = run_dir / "run_summary.csv"
        if summary_file.exists():
            df = pd.read_csv(summary_file)
            all_summaries.append(df)

combined = pd.concat(all_summaries, ignore_index = True)
combined["Condition"] = combined["Run"].str.split("-").str[0]

print(combined)

# # AVG VOID VOL PLOT BY DAYimport pandas as pd


# order = combined["Run"].unique()
# # combined["Run"] = pd.Categorical(combined["Run"], categories=order, ordered=True)
# average_AVV = combined.groupby("Run", sort=False)["Avg Void Vol (ul)"].mean()
# average_void_count = combined.groupby("Run", sort=False)["void"].mean()
# average_leak_count = combined.groupby("Run", sort=False)["leak"].mean()

# # combined.to_csv("all_runs_combined.csv", index=False)

# # print(average_AVV, average_void_count, average_leak_count)

# condition_colors = {
#     cond: color
#     for  cond, color in zip(combined["Condition"].unique(), ["skyblue", "lightgreen", "orange"])
# }
# bar_colors = [condition_colors[r.split("-")[0]] for r in order]

# fig, ax = plt. subplots()
# average_AVV.plot(kind="bar", ax=ax, color=bar_colors, edgecolor="black", zorder=0)

# pos_map = {run: i for i, run in enumerate(order)}
# for mouse, subdf in combined.groupby("Mouse"):
#     xs = [pos_map[r] for r in subdf["Run"]]
#     ys = subdf["Avg Void Vol (ul)"].values
#     ax.plot(xs, ys, marker="o", linestyle="-", color="black", alpha=0.6, zorder=2)

# ax.set_ylabel("Average Void Volume (ul)")
# ax.set_title("Average Void Volume per Run")
# # ax.set_xticks(range(len(order)))
# ax.set_xticklabels(order, rotation=0)

# plt.tight_layout()
# # plt.show()
# # 