#! /usr/bin/env python
# -*- coding: utf-8 -*-
import xgboost as xgb
import pandas as pd
import numpy as np
from time import time
from sklearn.model_selection import GridSearchCV 
from sklearn.model_selection import ShuffleSplit 
from sklearn.metrics import r2_score, make_scorer, mean_squared_error
import os

X_train = pd.read_csv('./input/X_train.csv')
y_train = pd.read_csv('./input/y_train.csv',header=None)
X_test = pd.read_csv('./input/X_test.csv',index_col=0)
os.environ["OMP_NUM_THREADS"] = "16"  #并行训练
xgb_regressor = xgb.XGBRegressor(seed=2018,nthread=16)
start = time() # Get start time
cv_sets_xgb = ShuffleSplit(random_state = 10) # shuffling our data for cross-validation
parameters_xgb = {'n_estimators':[500, 1000, 2000, 5000], 
             'learning_rate':[0.01, 0.05,0.07], 
             'max_depth':[5, 6, 7],
             'min_child_weight':[1, 1.5, 2]}
scorer_xgb = make_scorer(r2_score)
print('grid search start!')
grid_obj_xgb = GridSearchCV(xgb_regressor, parameters_xgb, scoring = scorer_xgb, cv = cv_sets_xgb)
grid_fit_xgb = grid_obj_xgb.fit(X_train, y_train)
print('grid search end!')
xgb_opt = grid_fit_xgb.best_estimator_

end = time() # Get end time
xgb_time = (end-start)/60 # Calculate training time
print(grid_fit_xgb.best_params_)
print(grid_fit_xgb.best_score_)
print('It took {0:.2f} minutes for GridCV to converge to optimised parameters for the XGBoost model'.format(xgb_time))
y_pred = np.expm1(xgb_opt.predict(X_test))
submission_df = pd.DataFrame(data= {'Id' : X_test.index, 'SalePrice': y_pred})
submission_df.to_csv('submission-xgb-v0.2.csv', index=False)