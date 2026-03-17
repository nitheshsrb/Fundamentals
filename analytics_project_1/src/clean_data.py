import pandas as pd

def clean_data(df):

    df.columns = df.iloc[0]
    df = df[['customer_id','clinic','purchase_date','amount']]
    df = df.iloc[1:]

    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    df['amount'] = df['amount'].astype('int')
    df.sort_values('purchase_date', ascending = True)
    
    return df

