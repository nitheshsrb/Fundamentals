import pandas as pd
import joblib
from load_data import load_data
from feature_engineering import feature_engineering

def predict(days):

    forecast_start = pd.to_datetime('today').date()
    
    forecast_end = pd.to_datetime(forecast_start + pd.Timedelta(days=days)).date()

    forecast_df = load_data(forecast_start,forecast_end,"forecast")

    model = joblib.load('weather_data/models/test_models/Baseline_Regression_Model_v1')

    selected_features = [
                        'max_temp_lag1',
                         'cloud_cover_mean',
                         'dew_point_2m_mean']
    
    forecast_df = feature_engineering(forecast_df)

    prediction_data = forecast_df[selected_features]

    print("Data for prediction : ",prediction_data.head(5))

    results = model.predict(prediction_data)

    prediction_data['Predictions'] = results.reset_index(drop=True).round()

    prediction_data['Forecasts'] = forecast_df['temperature_2m_max'].reset_index(drop=True).round()

    prediction_data['date'] = forecast_df['date'].reset_index(drop = True)

    prediction_data['Error in prediction and forecast'] = (prediction_data['Forecasts'] - prediction_data['Predictions']).round(0)

    prediction_data['Timestamp Key'] = pd.Timestamp.today()

    #WRITING
    prediction_data.to_csv('weather_data/data/Predictions.csv',index = False)

    return prediction_data


    




