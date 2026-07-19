import datetime
import pandas as pd
from load_data import load_data

end_date = pd.to_datetime(pd.offsets.MonthBegin(0).rollback(pd.Timestamp.today())).date()
print(end_date)

start_date = pd.to_datetime(end_date + pd.DateOffset(years = -8)).date()
print(start_date)


df = load_data(start_date,end_date,"actuals")
print("\nSuccesfully loaded daily weather data\n", df.head(5))

# Creating the full dataset
df.to_csv('weather_data/data/Baseline_data.csv',index = False)
print("\n Data written to destination successfully ")
