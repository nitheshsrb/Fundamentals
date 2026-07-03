from sklearn.metrics import r2_score,mean_absolute_error,root_mean_squared_error

import pandas as pd
import joblib
from train_pipeline import split_data

def evaluation(df):
    model = joblib.load('weather_data/models/test_models/Baseline_Regression_Model_v1')
    #print(model.summary())
    selected_features = model.params.index
    X_train,y_train,X_test,y_test,cutoff_date = split_data(df,selected_features)
    for c in X_test.columns:
        X_test[c] = X_test[c].astype('float')

    y_test = pd.to_numeric(y_test,errors='coerce')
    y_pred = model.predict(X_test)

    print(y_test,y_pred)

    dates_df = df
    dates_df['date'] = pd.to_datetime(dates_df['date'],format = '%Y-%m-%d')

    max_date = dates_df['date'].max()
    cutoff_date = max_date - pd.DateOffset(years = 1)

    print(dates_df.head(5))

    dates_df_shrunk = pd.DataFrame(dates_df['date'][dates_df['date'] >= cutoff_date]).reset_index()
    print(dates_df_shrunk.head())

    Results = pd.DataFrame()
    Results['date'] = dates_df_shrunk['date']
    Results['Actuals'] = y_test.reset_index(drop=True)
    Results['Predictions'] = y_pred.reset_index(drop=True)


    print("The number of generated predictions are", len(y_pred))
    print("R2 score is : ",r2_score(y_test,y_pred))
    print("Mean absolute error is : ", mean_absolute_error(y_test,y_pred))

    print('Results are : ',Results)


if __name__ == "__main__":

    df = pd.read_csv('weather_data/data/Feature_engineered_data.csv')
    evaluation(df)



