from sklearn.base import *
from sklearn.pipeline import *
import numpy as np
import pandas as pd


class ModelTransformer(TransformerMixin):
    """[summary]

    Args:
        TransformerMixin ([type]): [description]

    Raises:
        Exception: [description]

    Example of usage:

        # Feature Union 1 ######################################################
        > ls_clf_tf = [<PredictorsToClasifier>]
        > clf_tf = Pipeline(steps=[
                        ('clf', ModelTransformer(
                                    model = RandomForestClassifier(random_state = 0),
                                    probs = False,
                                    df_y = df[<AnyVarToPredict>],
                                )),
                    ])
        > prep1 =   ColumnTransformer(
                        transformers=[
                            ('clf', clf_tf, ls_clf_tf),
                        ]
                    ) 

        # Feature Union 2 ######################################################            
        > ls_num_tf = [<PredictorsToPreprocessor>]
        > num_tf = Pipeline(steps=[
                        ('imputer', SimpleImputer(strategy='median')),
                        ('scaler', StandardScaler()),
                    ])
        > prep2 = ColumnTransformer(
                        transformers=[
                            ('num_tf', num_tf, ls_num_tf),
                        ])

        # Union ################################################################
        > fu = Pipeline([
                    ('union', FeatureUnion(transformer_list=[
                                                            ('f1', prep1), 
                                                            ('f2', prep2)
                                                            ])
                    ),
                ])
        fu.fit(X_train, y_train)


        # Feature Names ########################################################
        > get_pipe_feature_names(fu) # Remember to import function from csklearn
    """



    ''' Use model predictions as transformed data. '''
    def __init__(self, model, df_y, 
                        predict_labels=True, 
                        predict_probs=False, drop_first_prob = True, 
                        prefix_output = 'mt'):
        self.model = model
        self.predict_labels = predict_labels
        self.predict_probs = predict_probs
        self.drop_first_prob = drop_first_prob # Eliminar la primera columna de predict_proba
        self.prefix_output = prefix_output
        self._feature_names_out = None
        self.df_y = df_y
        
        # Important check
        if self.df_y is not None:
            if isinstance(df_y, pd.Series) | isinstance(df_y, pd.DataFrame):
                self.df_y = df_y
            else:
                raise Exception('y argument must be pd.Series or pd.DataFrame\
with same indexes than X.')


    def get_params(self, deep=True):
        return dict(model=self.model, predict_probs=self.predict_probs, 
                    drop_first_prob = self.drop_first_prob,
                    df_y=self.df_y, prefix_output=self.prefix_output)


    def fit(self, *args, **kwargs):

        # Get indexes from X
        X_ = args[0] # usually is a matrix
        y_ = args[1] # we need to be a pd.series

        # Print to check if is working (SKLEARN 1.0.1 - 16/12/2021 works):
        # print('Indices not used to fit:')
        # print([x for x in self.df_y.index if x not in y_.index])

        # sanity check
        if not (isinstance(y_, pd.Series) | isinstance(y_, pd.DataFrame)):
            raise Exception('We need pd.Series or pd.DataFrame indexes')

        # In args, we have X_test, so we can get indexes      
        if self.df_y is None:
            self.model.fit(*args, **kwargs)
        else:
            # Sanity Check. All indexes should be in df_y
            if len([x for x in y_.index if x not in self.df_y.index]) > 0:
                raise Exception('ModelTransformer Error: df_y indexes does not\
 match with X indexes. df_y should have all y indexes.')
            self.model.fit(X_, self.df_y.loc[y_.index], **kwargs)

        # Get feature names!
        _ = self.transform(X_) # doesn't return anything!
        
        return self


    def _predict_probs(self, X):
        Xtrf = self.model.predict_proba(X)
        arr = np.asarray(Xtrf).reshape((len(X), -1))
        cols = [self.prefix_output+'p_'+str(x) for x in self.model.classes_]

        if self.drop_first_prob:
            arr = arr[:,1:] # From 1st column to the rest (avoid colineality)
            cols = cols[1:]
        return arr, cols
    

    def _predict_labels(self, X):
        Xtrf = self.model.predict(X)
        arr = np.asarray(Xtrf).reshape((len(X),1))
        cols = [self.prefix_output+'l_'+'_y']
        return arr, cols


    def transform(self, X, **transform_params):

        if (self.predict_probs) & (self.predict_labels):
            arrp, colsp = self._predict_probs(X)
            arrl, colsl = self._predict_labels(X)
            arr = np.hstack([arrp, arrl])
            cols = np.hstack([colsp, colsl]).tolist()

        elif (self.predict_probs):
            arr, cols = self._predict_probs(X)

        elif self.predict_labels:
            arr, cols = self._predict_labels(X)
        
        else:
            raise Exception('predict_probs or predict_labels methods must be at least one True')

        self._feature_names_out = cols
        return pd.DataFrame(arr, columns = cols)


    def get_feature_names_out(self, features_in=None):
        """[summary]

        Args:
            features_in (array, optional): Dummy Argument for compatibility. 
                Defaults to None.
        """
        return self._feature_names_out