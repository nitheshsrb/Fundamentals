from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_absolute_error,root_mean_squared_error
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
import joblib
import statsmodels.api as sm
import os

def train_pipeline(df):
    selected_features = ['max_temp_lag1',
                         'cloud_cover_mean (%)']
    
    df['date'] = pd.to_datetime(df['date'],format = '%Y-%m-%d')

    max_date = df['date'].max()
    cutoff_date = max_date - pd.DateOffset(years = 1) 

    print("The cutoff date is : ",cutoff_date)
    print("After cutoff dataframe is : ",df[df['date']>= cutoff_date])
    
    X_train = df[selected_features][df['date'] < cutoff_date]
    X_test = df[selected_features][df['date'] >= cutoff_date]

    y_train = pd.to_numeric(df['temperature_2m_max'][df['date'] < cutoff_date],errors='coerce')
    y_test = df['temperature_2m_max'][df['date'] >= cutoff_date]

   # scaler = StandardScaler()
    #X_train = scaler.fit_transform(X_train)
    #X_test = scaler.fit_transform(X_test)

    #joblib.dump(scaler,'weather_data/models/Linear_Standard_Scaler_v1')

    #if os.path.exists('weather_data/models/Linear_Model_v1') == False:
    res = sm.OLS(y_train,X_train)#.fit()
    res = res.fit_regularized(alpha = 1,L1_wt=1,method = 'elastic_net')
    joblib.dump(res,'weather_data/models/test_models/Baseline_Regression_Model_v1')
    print("Model successfully written")
    #else:
    #    pass
    for c in X_train.columns:
        X_train[c] = pd.to_numeric(X_train[c],errors = 'coerce')
    training_preds = res.predict(X_train)
    print("Training R2 is : ",r2_score(y_train,training_preds))

    X_test.to_csv('weather_data/data/Holdout_independent_data.csv')
    y_test.to_csv('weather_data/data/Holdout_dependent_data.csv')

    VIF = pd.DataFrame()
    VIF["feature"] = X_train.columns
    VIF["VIF"] = [variance_inflation_factor(X_train.values,i) for i in range(len(X_train.columns))]
    print(VIF)

if __name__ == "__main__":

    df = pd.read_csv('weather_data/data/Feature_engineered_data.csv')
    model = train_pipeline(df)