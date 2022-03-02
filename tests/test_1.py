# %% ###########################################################################
# Import modules
################################################################################
import sys, os
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.pipeline import *
from sklearn import set_config
set_config(display='diagram')

# Preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# Metrics
from sklearn.metrics import *

# From csklearn
sys.path.append(os.path.abspath(os.getcwd()))
from csklearn.transformers.VariableSelection import VariableSelection
from csklearn.wrappers.wrapper_feature_names_out import *
from csklearn.metrics.get_scores import *


# %% ###########################################################################
# Load and split data
################################################################################
X, y = load_wine(return_X_y = True, as_frame = True)
X['Color'] = 'Blanco'
X.loc[X['color_intensity'].between(6, 14), 'Color'] = 'Tinto'
X.drop('color_intensity', axis= 1, inplace=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, 
                        shuffle = True, stratify = y, random_state = 0)

# Select predictor types
# Conviene definir listas con el tipo de variables. Cada variable va a tener distintas transformaciones:
ls_num = X.drop('Color', axis= 1).columns.tolist()
ls_cat = ['Color']


# %% ###########################################################################
# DEFINE ARCHITECTURE
################################################################################

# Numerical variables
pipe_num = Pipeline(steps = [
                ('varsel', VariableSelection(ls_num)),
                ('sc', StandardScaler()),
                ('pca', wPCA(n_components = 2, random_state = 0)),
            ])

# Categorical variables
pipe_cat = Pipeline(steps = [
                ('varsel', VariableSelection(ls_cat)),
                ('ohe', OneHotEncoder(sparse = False, drop = 'first')),
            ])

# Union of pipelines
fu = FeatureUnion(transformer_list = [
            ('pipe_num', pipe_num),
            ('pipe_cat', pipe_cat)
        ]
    )

# Add algorithm
estimator = rf = RandomForestClassifier(n_estimators = 40, random_state = 0)
pipe_final = Pipeline(steps = [
    ('fu', fu),
    ('estimator', estimator)
])


# %% ###########################################################################
# Return Preprocessed matrix
################################################################################
X_train_tf = fu.fit_transform(X_train, y_train)
X_test_tf = fu.transform(X_test) # CUIDADO! SOLO QUEREMOS TRANSFORMAR

# Give names
X_train_tf = pd.DataFrame(X_train_tf, columns = fu.get_feature_names_out())
X_test_tf = pd.DataFrame(X_test_tf, columns = fu.get_feature_names_out())


# %% ###########################################################################
# Fit and predict Pipeline
################################################################################
pipe_final.fit(X_train, y_train)
y_pred = pipe_final.predict(X_test)


# %% ###########################################################################
# Return many metrics
################################################################################
d_scorer = {
            'recall':make_scorer(recall_score, average='weighted'),
            'bacc':make_scorer(balanced_accuracy_score),
            'f1_score': make_scorer(f1_score, average='weighted'),
            'precision':make_scorer(precision_score, average='weighted'),
            
            } 
get_scores(y_test, y_pred, d_scorer = d_scorer)


# %% ###########################################################################
# Final Prints
################################################################################
print('TEST_1 PASSED SUCCESSFULLY!!!')
print(aasdfasdf)