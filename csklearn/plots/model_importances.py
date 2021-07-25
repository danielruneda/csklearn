import pandas as pd
import matplotlib.pyplot as plt

def plot_model_importances(model_columns, model_importances, n_top_features=10, 
                           title='Feature Importances', ax = None, **kwargs):
    
    if ax is None:
        ax = plt.gca()
    
    df_aux = pd.DataFrame({'Features':model_columns, 
                           'Importances':model_importances})
    df_aux = df_aux.sort_values('Importances', ascending=True).\
                                                        tail(n_top_features)
    df_aux.set_index('Features').plot(kind='barh', ax = ax, **kwargs)
    ax.set_title(title)
    ax.set_legend = None
    return ax