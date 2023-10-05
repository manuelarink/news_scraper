import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


def drop_duplicates(df: pd.DataFrame, dupl_cols: list) -> pd.DataFrame:
    """
    Removes duplicates in dupl_cols from df.
    :param df:
    :param dupl_cols:
    :return:
    """
    df_copy = df.copy()
    df_copy.drop_duplicates(subset=dupl_cols, inplace=True)
    return df_copy


class MultiReferenceImputer(BaseEstimator, TransformerMixin):
    """
    Fills missing values of a column by values from a list of referenced column.
    """

    def __init__(self, col, ref_col_list):
        self.col = col
        self.ref_col_list = ref_col_list

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        X = X.copy()

        # copies missing values in col from ref_col_list
        # (the columns in ref_col_list can contain na as well, so we try to
        # fill from more than one column)
        for c in self.ref_col_list:
            X[self.col] = X[self.col].fillna(X[c])

        return X


class ConcatStringFeatureEncoder(BaseEstimator, TransformerMixin):
    """
    Creates a new feature as a concatenation of the String values of other features.
    """

    def __init__(self, new_col, ref_col_list):
        self.new_col = new_col
        self.ref_col_list = ref_col_list

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        X = X.copy()

        X[self.new_col] = \
            X[self.ref_col_list].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)

        return X








