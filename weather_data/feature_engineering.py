import pandas as pd
from sklearn.preprocessing import StandardScaler

def feature_engineering(df):
    
    df['max_temp_lag1'] = df['temperature_2m_max (°C)'].shift(1).fillna(df['temperature_2m_max (°C)'])
    df['max_temp_lag1week'] = df['temperature_2m_max (°C)'].shift(7).fillna(df['temperature_2m_max (°C)'])
    df['max_temp_lag52weeks'] = df['temperature_2m_max (°C)'].shift(365).fillna(df['temperature_2m_max (°C)'])

    return df

if __name__ == "__main__":

    final_df = feature_engineering(final_df)