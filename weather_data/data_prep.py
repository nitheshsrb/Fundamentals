import pandas as pd

def data_prep():
    df = pd.read_csv("weather_data/data/Baseline_data.csv")
    delta_df = pd.read_csv("weather_data/data/Delta_load.csv")
    full_data = pd.concat([df,delta_df])
    return full_data

if __name__ == "__main__":

    final_df = data_prep()
    final_df.to_csv('weather_data/data/full_data.csv')
