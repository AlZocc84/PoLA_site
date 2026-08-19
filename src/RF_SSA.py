#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:27:11 2024

@author: alberto

Adapted for SSA on Jul 2026
"""
import glob
#import matplotlib.pyplot as plt
# Use numpy to convert to arrays
import numpy as np
import pandas as pd
import argparse
import joblib
import pathlib

#%%
def ssa_rf(test_cumulative):
    
   vol = test_cumulative[-1] # get the total porous volume, as the last entry in file
      
   test_features = test_cumulative / vol

   test_features = test_features.reshape(1, -1)
   
   # Import the model we are using
   from sklearn.ensemble import RandomForestRegressor
   
   # Instantiate model with 1000 decision trees
   rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
   
   # Import the optimized parameters
   scrpath = pathlib.Path(__file__).parent.resolve()
   
   rf_path = scrpath / pathlib.Path("SSA_RF_param.joblib")
   rf = joblib.load(rf_path)
   
   # Predict SSA for the given sample
   predictions = rf.predict(test_features)
   SSA = predictions[0] * vol
   print(f"Specific Surface Area = {SSA:.1f} m\u00b2/g")
   
   return SSA
#%%

gTest = False

if __name__ == "__main__" and not gTest:

    # =================================
    # Import the cumulative VMinD file
    # =================================
    
    parser = argparse.ArgumentParser(
        description=""
    )
    
    parser.add_argument(
        "filename",
        help="Cumulative VMinD file to be analyzed"
    )
    
    args = parser.parse_args()
       
    file=args.filename
       
    test=np.loadtxt(file)
       
    test_cumulative = test[:60,-1]
    
    
    ssa_rf(test_cumulative)

