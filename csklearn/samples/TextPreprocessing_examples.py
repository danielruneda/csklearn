# %% Import modules ------------------------------------------------------------
from ..utils.get_pipe_feature_names import get_pipe_feature_names
import pandas as pd
from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import Pipeline
from sklearn.compose import *


# SKLearn Displays
from sklearn import set_config
set_config(display='diagram')


# %% UDFs
from ..preprocessing.as_type import *
from ..preprocessing.TextPreprocessing import *
from sklearn.feature_extraction.text import *
from ..transformers.VariableSelection import *
from ..utils.get_pipe_feature_names import *

import category_encoders as ce




# %% Read data examples
categories = ['alt.atheism','soc.religion.christian','comp.graphics','sci.med']

# Train
d_train = fetch_20newsgroups(subset='train',
                    categories=categories, 
                    shuffle=True, 
                    random_state=42)
df_train = pd.DataFrame({'txt':d_train['data'], 'target':d_train['target']})
print('Train targets:')
print(df_train['target'].value_counts())

# Test
d_test = fetch_20newsgroups(subset='test',
                    categories=categories, 
                    shuffle=True, 
                    random_state=42)
df_test = pd.DataFrame({'txt':d_test['data'], 'target':d_test['target']})
print('\nTest targets')
print(df_test['target'].value_counts())

# Add dummy columns
df_train['A'] = 'A'
df_train['B'] = 'B'
df_test['A'] = 'A'
df_test['B'] = 'B'


# Split
X_train = df_train.drop('target', axis=1)
y_train = df_train['target']
X_test = df_test.drop('target', axis=1)
y_test = df_test['target']


# %% Plot topics with keywords
txt_tf_vars = ['txt']
ls_avoid_tokens = ['while', 'the']
ls_regexp = ['\s(?i)OK\s', '\snan\s', '[—°]', '(?i)\$ICS\$'] +\
            ['\s'+x+'\s' for x in ls_avoid_tokens]
txt_tf = Pipeline(steps=[
                    ('tostr', as_str()),
                    ('tc', TextCleaning(
                                ls_rmregex = ls_regexp,
                                len_threshold = 2,
                                onlywords = True,
                                stopwords=True,
                                lowercase = True,
                                normalize_method = 'stemming'
                                )),
                    ('tte', TextEncoding(
                                nwords_threshold = 4,
                                nrows_threshold = 20,
                                label_topk=7,
                                label_unique_threshold = .6,
                                avoid_words = ['nan', 'aac']
                                )),
                    ('ohew', OneHotEncodingWords(prefix='txt'))
                    #('tfidf', TfidfVectorizer()),#HashingVectorizer(n_features=50)),
                    # ('tonp', as_np()),
                    # ('binarize', Binarizer(threshold = 0))
                ])


# Fijarse que en las categóricas las debe eliminar al ser invariantes
cat_tf_vars = ['A', 'B']
cat_tf = Pipeline(steps=[
                    ('tostr', as_str()),
                    ('ohe', ce.OneHotEncoder(handle_unknown='value',
                                drop_invariant=True))
                ])

predictors = ['txt', 'A', 'B']
preprocessor = ColumnTransformer(
                    transformers=[
                        ('txt_tf', txt_tf, txt_tf_vars),
                        ('cat_tf', cat_tf, cat_tf_vars)
                    ])

pipe = Pipeline(steps=[
                ('varsel', VariableSelection(predictors)),
                ('preprocessor', preprocessor)
                ])
pipe


# %%
xx = pipe.fit_transform(X_train, y_train)
colnames = get_pipe_feature_names(pipe)



# %%

X_train_ = pd.DataFrame(xx, columns=colnames)
X_train_


# %%

# %%
