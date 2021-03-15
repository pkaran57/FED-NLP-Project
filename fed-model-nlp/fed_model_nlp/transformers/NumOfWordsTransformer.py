from sklearn.base import BaseEstimator, TransformerMixin


class NumOfWordsTransformer(BaseEstimator, TransformerMixin):
    """
    return words count
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        extract_words_count = lambda input: input['word_count']
        return [[feature] for feature in list(map(extract_words_count, X))]
