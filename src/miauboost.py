#!/usr/bin/env python
# coding: utf-8

from catboost import CatBoostRegressor

import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import sys

from sklearn.compose import ColumnTransformer

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import mean_squared_error, make_scorer, r2_score

# ## Error analysis:
def error_analysis(y_test, y_pred):
    """Generated true vs. predicted values and residual scatter plot for models

    Args:
        y_test (array): true values for y_test
        y_pred_test (array): predicted values of model for y_test
    """     

    y_test = pd.DataFrame(y_test)
    y_pred = pd.DataFrame(y_pred)
    # Calculate residuals
    residuals = y_test["capture_number"] - y_pred[0]
    residuals = pd.DataFrame(residuals)
    
    # Plot real vs. predicted values 
    fig, ax = plt.subplots(1,2, figsize=(15, 5))
    plt.subplots_adjust(right=1)
    plt.suptitle('Error Analysis')
    
    ax[0].scatter(y_pred, y_test, color="#FF5A36", alpha=0.7)
    ax[0].plot([-400, 350], [-400, 350], color="#193251")
    ax[0].set_title("True vs. predicted values", fontsize=16)
    ax[0].set_xlabel("predicted values")
    ax[0].set_ylabel("true values")
    #ax[0].set_xlim((y_pred.min()-10), (y_pred.max()+10))
    #ax[0].set_ylim((y_test.min()-40), (y_test.max()+40))
    
    ax[1].scatter(y_pred, residuals, color="#FF5A36", alpha=0.7)
    ax[1].plot([-400, 350], [0,0], color="#193251")
    ax[1].set_title("Residual Scatter Plot", fontsize=16)
    ax[1].set_xlabel("predicted values")
    ax[1].set_ylabel("residuals")
    #ax[1].set_xlim((y_pred.min()-10), (y_pred.max()+10))
    #ax[1].set_ylim((residuals.min()-10), (residuals.max()+10));

def evaluate_rmse(y_true, y_pred, ndigits=3):
    """ Prints the RMSE (root mean squared error) of y_pred in relation to y_true"""
    rmse = mean_squared_error(y_true, y_pred, squared=False )
    print("Number of predictions: ", len(y_pred))
    print("RMSE: ", round(rmse, ndigits))
    return rmse

X_test = pd.read_csv("data/X_test.csv")
y_test = pd.read_csv("data/y_test.csv")
X_train = pd.read_csv("data/X_train.csv")
y_train = pd.read_csv("data/y_train.csv")

# Check the shape of the data sets
print("X_train:", X_train.shape)  
print("y_train:", y_train.shape)  
print("X_test:", X_test.shape) 
print("y_test:", y_test.shape)  

# Initialize the CatBoostRegressor
catboost_model = CatBoostRegressor(iterations=10000,  # Number of boosting iterations
                                   depth=6,          # Depth of the trees
                                   learning_rate=0.1,  # Learning rate
                                   loss_function='RMSE',  # Loss function for regression
                                   verbose=100)     # Print progress every 100 iterations


# Fit the model to the training data
catboost_model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = catboost_model.predict(X_test)  

# evaluate
error = evaluate_rmse(y_test, y_pred)

#r2_score(y_test, y_pred) 

error_analysis(y_test, y_pred)

# saving the model 
filename = 'models/cat_boost_model.sav'
pickle.dump(catboost_model, open(filename, 'wb'))



# Since
# 
# Residual = Observed – Predicted
# 
# …positive values for the residual (on the y-axis) mean the prediction was too low, and negative values mean the prediction was too high; 0 means the guess was exactly correct.
# 
# Optimally the residuals,
# - (1) are pretty symmetrically distributed, tending to cluster towards the middle of the plot.
# - (2) they’re clustered around the lower single digits of the y-axis (e.g., 0.5 or 1.5, not 30 or 150).
# - (3) in general, there aren’t any clear patterns.
# 
# 
# -> This looks pretty good
# 
# 
# 




