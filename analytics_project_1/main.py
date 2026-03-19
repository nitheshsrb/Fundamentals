import pandas as pd
from config import filepath,output_path
from src.load_data import load_data
from src.clean_data import clean_data
from src.analysis import customer_summary, top_customers
from src.features import create_features


def main():
    df = pd.read_csv(filepath)
    df = load_data(filepath)
    df = clean_data(df)
    
    summary = customer_summary(df)
    summary = create_features(summary)
    output = top_customers(summary,3)

    output.to_csv(output_path + 'top_customers.csv')

if __name__ == '__main__':
    main()
