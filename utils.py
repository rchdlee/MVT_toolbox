from datetime import datetime
import pandas as pd
import numpy as np

def subtract_times(t1: str, t2: str) -> str: # t1 -> earlier time, t2 -> later time
    if pd.isna(t1) or pd.isna(t2):
        return np.nan
    if str(t1).lower() == "nan" or str(t2).lower() == "nan":
        return np.nan
  
    fmt = "%H:%M:%S"
    dt1 = datetime.strptime(t1, fmt)
    dt2 = datetime.strptime(t2, fmt)

    diff = dt2 - dt1

    total_sec = int(diff.total_seconds())
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    seconds = total_sec % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"

def format_time_to_sec(t:str) -> int:
    h, m, s = map(int, t.split(":"))
    t_seconds = h * 3600 + m * 60 + s

    return t_seconds

def is_time_less_than(t: str, cutoff: str) -> bool: # returns true if time is less than cutoff time
    # h, m, s = map(int, t.split(":"))
    # cutoff_h, cutoff_m, cutoff_s = map(int, cutoff.split(":"))

    # t_seconds = h * 3600 + m * 60 + s
    # cutoff_seconds = cutoff_h * 3600 + cutoff_m * 60 + cutoff_s

    t_seconds = format_time_to_sec(t)
    cutoff_seconds = format_time_to_sec(cutoff)

    return t_seconds < cutoff_seconds

def adjust_volume(vol: float, delay_t: str) -> float:
    if pd.isna(delay_t):
        return np.nan
    if str(delay_t).lower() == "nan":
        return np.nan

    delay_t_sec = format_time_to_sec(delay_t)

    if delay_t_sec < 3600:
        return vol

    if vol < 250:
        if delay_t_sec >= 6300: # 01:45:00
            return vol * 1.25
        if delay_t_sec >= 5400: # 01:30:00
            return vol * 1.2
        if delay_t_sec >= 4500: # 01:15:00
            return vol * 1.1
        if delay_t_sec >= 3600: # 01:00:00
            return vol * 1.08
        
    if vol >= 250:
        if delay_t_sec >= 6300: # 01:45:00
            return vol * 1.15
        if delay_t_sec >= 5400: # 01:30:00
            return vol * 1.1
        if delay_t_sec >= 4500: # 01:15:00
            return vol * 1.07
        if delay_t_sec >= 3600: # 01:00:00
            return vol * 1.05

def weighted_avg_void_vol(df):
    return (df["Avg Void Vol (ul)"] * df["void"]).sum() / df["void"].sum()