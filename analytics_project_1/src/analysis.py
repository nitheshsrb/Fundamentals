import pandas as pd

def customer_summary(df):
    summary = df.groupby('customer_id').agg(
        total_spend = ('amount','sum'),
        number_of_purchases = ('customer_id','count'),
        avg_order_value = ('amount','mean'))
    return summary

def top_customers(summary,n):
    return summary.sort_values('total_spend',ascending = False).head(n)
