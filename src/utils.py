"""
regressions functions from stats model 
"""
import statsmodels.api as sm
import statsmodels.formula.api as smf

def weighted_regression(formula, data, weight_column):
    model = smf.wls(formula, data=data, weights=data[weight_column]).fit()
    return model

def unweighted_regression(formula, data):
    model = smf.ols(formula, data=data).fit()
    return model
