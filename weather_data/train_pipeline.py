from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import pandas as pd
import statsmodels.api as sm

def train_pipeline(df,new_start_date):
    selected_features = ['dew_point_2m_mean (°C)','et0_fao_evapotranspiration (mm)',
                         'max_temp_lag1','max_temp_lag1week','max_temp_lag52weeks',
                         'soil_moisture_0_to_100cm_mean (m³/m³)',
                         'wet_bulb_temperature_2m_mean (°C)']
    
    
    X_train = df[selected_features][df['time'] < new_start_date + pd.Timedelta(days = -30)]
    X_test = df[selected_features][df['time'] >= new_start_date + pd.Timedelta(days = -30)]

    y_train = df[['temperature_2m_max (°C)'][df['time'] < new_start_date + pd.Timedelta(days = -30)]]
    y_test = df['temperature_2m_max (°C)'][df['time'] >= new_start_date + pd.Timedelta(days = -30)]]

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)

    model = sm.OLS(y_train,X_train).fit()

