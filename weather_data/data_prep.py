import pandas as pd

def data_prep():
    df = pd.read_csv("weather_data/data/Baseline_data.csv")
    delta_df = pd.read_csv("weather_data/data/Delta_load.csv")
    full_data = pd.concat([df,delta_df])
    return full_data


