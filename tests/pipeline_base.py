# %%
import unittest
import imp # Para recargar un MÓDULO
import pandas as pd

# SKLearn
from sklearn.pipeline import *
from sklearn.compose import ColumnTransformer
from sklearn.impute import *
from sklearn.preprocessing import *
from sklearn.decomposition import *
from sklearn.ensemble import *
from sklearn.linear_model import *
from sklearn.datasets import fetch_openml
from sklearn.model_selection import *
from sklearn.metrics import *

from sktools import GradientBoostingFeatureGenerator
from sktools.quantilegroups import MeanGroupFeaturizer

# SKLearn Displays
from sklearn import set_config
set_config(display='diagram')

# UDFs
from csklearn_.pipeline import pipeline_base
from csklearn_.transformers.VariableSelection import VariableSelection

from sklearn_pandas import DataFrameMapper



# if __name__ == '__main__':

# Load trial data
X, y = fetch_openml("titanic", version=1, as_frame=True, return_X_y=True)
X.drop(['boat', 'body', 'home.dest'], axis=1, inplace=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                stratify=y, test_size=0.2,
                                                random_state=0)  

# Define a pipeline object
cat_tf_vars = ['pclass', 'sex', 'ticket', 'cabin', 'embarked']
cat_tf = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False)),
])

num_tf_vars = ['age', 'fare']
num_tf = Pipeline(steps=[
    ('imputer', SimpleImputer()),
    ('scaler', RobustScaler())
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_tf, num_tf_vars),
        ('cat', cat_tf, cat_tf_vars)
    ])

pipe = Pipeline(steps=[
                        #('VariableSelection', VariableSelection(num_tf_vars+cat_tf_vars)),
                        ('preprocessor', preprocessor),
                        ('estimator', LogisticRegression(random_state=0))])

pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
print(classification_report(y_test, y_pred))
print('Validation Score: {}'.format(accuracy_score(y_test, y_pred)))

pipe

# %%
