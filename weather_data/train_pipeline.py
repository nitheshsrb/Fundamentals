from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_absolute_error,root_mean_squared_error
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
import joblib
import statsmodels.api as sm
import os

def split_data(df,selected_features):

    df['date'] = pd.to_datetime(df['date'],format = '%Y-%m-%d')
    max_date = df['date'].max()
    cutoff_date = max_date - pd.DateOffset(years = 1) 

    print("The training cutoff date is : ",cutoff_date)
    #print("After cutoff dataframe is : ",df[df['date']>= cutoff_date])
    
    X_train = df[selected_features][df['date'] < cutoff_date]
    X_test = df[selected_features][df['date'] >= cutoff_date]

    y_train = pd.to_numeric(df['temperature_2m_max'][df['date'] < cutoff_date],errors='coerce')
    y_test = df['temperature_2m_max'][df['date'] >= cutoff_date]

    return X_train,y_train,X_test,y_test,cutoff_date

def train_baseline_pipeline(df):
    
    selected_features = ['max_temp_lag1',
                         'cloud_cover_mean (%)',
                         'dew_point_2m_mean']
    
    X_train,y_train,X_test,y_test,cutoff_date = split_data(df,selected_features)
    #if os.path.exists('weather_data/models/Linear_Model_v1') == False:
    res = sm.OLS(y_train,X_train)#.fit()
    res = res.fit_regularized(alpha = 0.5,L1_wt=1,method = 'elastic_net')
    joblib.dump(res,'weather_data/models/test_models/Baseline_Regression_Model_v1')
    print("Model successfully written")

    y_train_pred = res.predict(X_train)
    print("Training R2 : ",r2_score(y_train,y_train_pred))
    #print(res.summary())
    #else:
    #    pass