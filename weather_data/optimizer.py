import pandas as pd
import numpy as np
from scipy.stats import kstest,norm
from sklearn.linear_model import LinearRegression
from model_metric import evaluation
from train_pipeline import train_baseline_pipeline

def optimization(Results):

    Results['Residual'] = Results['Actuals'] - Results['Predictions']
    rv = norm(Results['Residual'].mean(),Results['Residual'].std())
    statistic_test  = kstest(Results['Residual'],rv.cdf)
    
    if statistic_test.pvalue > 0.05:
        print('The residual distribution is normal with mean',statistic_test.statistic_location)
    
    Results['Binned Actuals'], bin_edges = pd.qcut(Results['Actuals'],q = [0.05,0.4,0.75,0.95],retbins = True)

    error_model = LinearRegression()
    error_model.fit(Results['Predictions'].values.reshape(-1,1),Results['Residual'])

    beta0 = error_model.intercept_
    beta1 = error_model.coef_[0]


    return Results,beta0,beta1,bin_edges





    


    
    
    



