import pandas as pd

def create_features(df):
    df['high_value_order'] = df['total_spend'].apply(lambda x: 1 if x > 100 else 0)
    return df