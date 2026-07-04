import pandas as pd
from sklearn.preprocessing import StandardScaler

def feature_engineering(df):
    
    df['max_temp_lag1'] = df['temperature_2m_max'].shift(1).fillna(df['temperature_2m_max'])
    df['max_temp_lag1week'] = df['temperature_2m_max'].shift(7).fillna(df['temperature_2m_max'])
    df['max_temp_lag52weeks'] = df['temperature_2m_max'].shift(365).fillna(df['temperature_2m_max'])

    return df


