import pandas as pd
from config import filepath,output_path
from src.load_data import load_data
from src.clean_data import clean_data
from src.analysis import customer_summary, top_customers
def main():
    df = pd.read_csv(filepath)
    df = load_data(filepath)
    print(df.head())

    df = clean_data(df)
    print("Cleaned data : ",df.head())

    summary = customer_summary(df)
    output = top_customers(summary,3)

    output.to_csv(output_path + 'top_customers.csv')

if __name__ == '__main__':
    main()
