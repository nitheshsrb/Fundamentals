import pandas as pd
import numpy as np
import joblib
import pandas as pd
import numpy as np
import joblib

def prediction(df, days):
    model = joblib.load('weather_data/models/test_models/Baseline_Regression_Model_v1')
    delta_df = pd.read_csv('weather_data/data/Delta_load.csv')
    

    last_known_lag = delta_df['temperature_2m_max'].iloc[-1].astype('float')
    print(type(last_known_lag))
    

    prediction_data = df.copy().reset_index(drop=True)
    prediction_data['max_temp_lag1'] = prediction_data['max_temp_lag1'].astype('float') 
    
    predictions = []
    
    for i in range(days):
        
        prediction_data.loc[i, 'max_temp_lag1'] = last_known_lag
        

        row = prediction_data.iloc[[i]]
        y = model.predict(row).iloc[0]
        
        predictions.append(y)
        last_known_lag = y  
    

    results = prediction_data.copy().reset_index(drop=True)
    results['Prediction'] = predictions
    
    return results

fake_df = pd.DataFrame({'max_temp_lag1': range(5,9)
                        , 'cloud_cover_mean' : range(5,9)
                        , 'dew_point_mean_2m' : range(5,9)})

print(fake_df)
results = prediction(fake_df,days = 4)
print(results)




