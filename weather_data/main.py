###################################
#ALL WEATHER DATA EXECUTIONS
####################################

import pandas as pd
from delta_load import delta_load
from data_prep import data_prep
from feature_engineering import feature_engineering
from train_pipeline import train_baseline_pipeline
from model_metric import evaluation
from predict import predict

delta_df = delta_load()
delta_df.to_csv("weather_data/data/Delta_load.csv")
print("\n Successfully loaded the newest data")

df = data_prep()
df.to_csv('weather_data/data/full_data.csv')

df = feature_engineering(df)
print("Successfully loaded the data ")
df.to_csv('weather_data/data/Feature_engineered_data.csv')

train_baseline_pipeline(df)
evaluation(df)

predictions = predict(14)

print("Predictions for next 2 weeks \n", predictions)