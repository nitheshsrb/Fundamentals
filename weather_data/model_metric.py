from sklearn.metrics import r2_score,mean_absolute_error,root_mean_squared_error

import pandas as pd
import joblib

model = joblib.load('weather_data/models/test_models/Baseline_Regression_Model_v1')
#print(model.summary())
X_test = pd.read_csv('weather_data/data/Holdout_independent_data.csv')
X_test = X_test.iloc[:,1:]
for c in X_test.columns:
    X_test[c] = X_test[c].astype('float')
print('Datatypes of X_test are :',X_test.dtypes)
y_test = pd.read_csv('weather_data/data/Holdout_dependent_data.csv')
y_test = y_test.iloc[:,1:]
print(y_test.head())
y_test['temperature_2m_max'] = pd.to_numeric(y_test['temperature_2m_max'],errors='coerce')
y_pred = model.predict(X_test)

dates_df = pd.read_csv('weather_data/data/Feature_Engineered_data.csv')
dates_df['date'] = pd.to_datetime(dates_df['date'],format = '%Y-%m-%d')

max_date = dates_df['date'].max()
cutoff_date = max_date - pd.DateOffset(years = 1)

print(dates_df.head(5))

dates_df_shrunk = pd.DataFrame(dates_df['date'][dates_df['date'] >= cutoff_date]).reset_index()
print(dates_df_shrunk.head())

Results = pd.DataFrame()
Results['date'] = dates_df_shrunk['date']
Results['Actuals'] = y_test['temperature_2m_max']
Results['Predictions'] = y_pred


print("The number of generated predictions are", len(y_pred))
print("R2 score is : ",r2_score(y_test,y_pred))
print("Mean absolute error is : ", mean_absolute_error(y_test,y_pred))

print('Results are : ',Results)





