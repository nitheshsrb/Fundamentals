import os
import pandas as pd
from datetime import datetime
from load_data import load_data

def delta_load():
    
    path = "weather_data/data/"
    #Setting end date as today
    temp_df = pd.read_csv(path + "Baseline_data.csv")
    
    temp_df['date'] = pd.to_datetime(temp_df['date'])
    start_date = pd.to_datetime(temp_df['date'].max() + pd.DateOffset(days = 1)).date()
    end_date = pd.Timestamp.today().date()
    # Calling the load function for delta time period
    delta_df = load_data(start_date,end_date,"actuals")
    delta_df.sort_values(by='date',ascending = False)

    return delta_df
