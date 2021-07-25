import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import scipy

# UDFs
from csklearn_.preprocessing.get_pipe_feature_names import \
    get_feature_out

class twcn(BaseEstimator, TransformerMixin):
    """Transform With Column Names: Tranformer Wrapper que devuelve pandas 
            dataframe en vez de numpy array.

    Args:
        transformer (sklearn.preprocessing): Un transformer de sklearn
    """
    def __init__(self, transformer):
        #super().__init__()
        self.transformer = transformer

    def fit(self, X, y=None, **kwargs):
        try:
            self.transformer.fit(X, y)
        except:
            self.transformer.fit(X)
        return self

    def transform(self, X, y=None, **kwargs):
        try:
            tfm = self.transformer.transform(X, y)
        except:
            tfm = self.transformer.transform(X)
        
        # Si sklearn devuelve csr_matrix, entonces transformamos a np array
        if isinstance(tfm, scipy.sparse.csr.csr_matrix):
            tfm = tfm.toarray()

        colnames = get_feature_out(self.transformer, X.columns)
        X = pd.DataFrame(tfm)
        X.columns = colnames
        return X