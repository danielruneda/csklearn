import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class perturbate_and_validate:
    """Valid for Regression
    """

    def __init__(self):
        self.predictor_p = None
        self.sigma = None
        self.mu = None
        self.df_p = None

    def fit_predictor(self, X_train, predictor_p):
        """
        Introducir del conjunto de entrenamiento el predictor a perturbar
        para conocer sus medidas estadísticas.
        """
        self.predictor_p = predictor_p
        # self.sigma = np.std(X_train[predictor_p])
        # self.mu = np.mean(X_train[predictor_p])
        self.min = min(X_train[predictor_p])
        self.max = max(X_train[predictor_p])
        self.step = None


    def perturbate(self, model, pdseries_row, target_name='y', n_iter=500):
        """
        - model: modelo a estudiar
        - pdseries_row: fila con el tipo pandas series
        - n_iter: número de perturbaciones a realizar
        """
        row = pdseries_row.copy()
        self.step = (self.max - self.min)/n_iter
        perturbations = []
        for perturbation in np.arange(self.min, self.max, self.step):
            row[self.predictor_p] = perturbation
            y = model.predict(row.to_frame().transpose())
            perturbations.append(np.hstack([row, y]))


        df_p = pd.DataFrame(perturbations,
                              columns = list(row.keys())+[target_name])
        cols_order = [target_name, self.predictor_p]+\
                list(set(df_p.columns) - set([target_name, self.predictor_p]))
        self.df_p = df_p[[target_name, self.predictor_p]].sort_values(self.predictor_p)

        return df_p[cols_order]


    def plot(self, title=None, ax = None, **kwargs):
        
        if ax is None:
            ax = plt.gca()
        target = list(set(self.df_p.columns) - set([self.predictor_p]))[0]
        self.df_p.plot.scatter(self.predictor_p, target, ax = ax, **kwargs)
        ax.set_title(title)
        return ax


    