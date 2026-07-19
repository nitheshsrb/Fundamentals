###################################
#ALL WEATHER DATA EXECUTIONS
####################################

import pandas as pd
import os
from delta_load import delta_load
from data_prep import data_prep
from feature_engineering import feature_engineering
from train_pipeline import train_baseline_pipeline
from model_metric import evaluation
from predict import predict

delta_df = delta_load()
delta_df.to_csv("weather_data/data/Delta_load.csv",index = False)
print("\n Successfully loaded the newest data")

df = data_prep()
df = df.drop(columns=['Unnamed: 0'], errors='ignore')
df.to_csv('weather_data/data/full_data.csv',index = False)

df = feature_engineering(df)
df = df.drop(columns=['Unnamed: 0'], errors='ignore')
print("Successfully loaded the data ")
df.to_csv('weather_data/data/Feature_engineered_data.csv',index = False)

train_baseline_pipeline(df)
evaluation(df)

predictions = predict(14)

if os.path.exists('weather_data/data/Historic_predictions.csv'):
    hist_preds = pd.read_csv('weather_data/data/Historic_predictions.csv')
    hist_preds['Timestamp Key'] = pd.to_datetime(hist_preds['Timestamp Key'])
    
    if hist_preds['Timestamp Key'].dt.date.max() != pd.Timestamp.today().date():
        hist_preds = pd.concat([hist_preds,predictions])
        hist_preds.to_csv('weather_data/data/Historic_predictions.csv',index = False)

else:
    predictions.to_csv('weather_data/data/Historic_predictions.csv',index = False)

print("Predictions for next 2 weeks \n", predictions)