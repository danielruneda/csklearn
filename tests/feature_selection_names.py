# %%
import pandas as pd
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.utils.validation import _check_feature_names_in

# %%
X = pd.DataFrame(
    [[ 0.87, -1.34,  0.31 ],
     [-2.79, -0.02, -0.85 ],
     [-1.34, -0.48, -2.55 ],
     [ 1.92,  1.48,  0.65 ]],
     columns = ['A', 'B', 'C']

    )
y = pd.Series([0, 1, 0, 1])


# %%
class wSelectFromModel(SelectFromModel):
    """
    Wrapper SimpleImputer to get feature names out
    """
        
    def get_feature_names_out(self, input_features=None):

        return _check_feature_names_in(self, input_features)


# %%
selector = SelectFromModel(estimator=LogisticRegression()).fit(X, y)
selector.estimator_.coef_

# %%
selector.get_feature_names_out()

# %%
selector.ranking_

# %%
selector.threshold_

# %%
selector.get_support()

# %%
selector.transform(X)
# %%
