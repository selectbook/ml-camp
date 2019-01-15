#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.ensemble import GradientBoostingRegressor
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

gbdt_regressor = GradientBoostingRegressor(random_state=2018)
start = time() # Get start time
cv_sets_gbdt = ShuffleSplit(random_state = 10) # shuffling our data for cross-validation
parameters_gbdt = {'n_estimators':[50, 100, 200, 500], 
             'learning_rate':[0.05, 0.07, 0.1], 
             'max_depth':[5, 6, 7],
             'subsample':[0.6,0.8,0.9,1.0]}
scorer_gbdt = make_scorer(r2_score)
print('grid search start!')
grid_obj_gbdt = GridSearchCV(gbdt_regressor, parameters_gbdt, scoring = scorer_gbdt, cv = cv_sets_gbdt)
grid_fit_gbdt = grid_obj_gbdt.fit(X_train, y_train)
print('grid search end!')
gbdt_opt = grid_fit_gbdt.best_estimator_

end = time() # Get end time
gbdt_time = (end-start)/60 # Calculate training time
print(grid_fit_gbdt.best_params_)
print(grid_fit_gbdt.best_score_)
print('It took {0:.2f} minutes for GridCV to converge to optimised parameters for the XGBoost model'.format(gbdt_time))
y_pred = np.expm1(gbdt_opt.predict(X_test))
submission_df = pd.DataFrame(data= {'Id' : X_test.index, 'SalePrice': y_pred})
submission_df.to_csv('submission-gbdt-v0.2.csv', index=False)