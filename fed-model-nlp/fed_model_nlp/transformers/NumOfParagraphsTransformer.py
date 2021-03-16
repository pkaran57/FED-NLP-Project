from sklearn.base import BaseEstimator, TransformerMixin


class NumOfParagraphsTransformer(BaseEstimator, TransformerMixin):
    """
    return paragraphs count
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        extract_paragraphs_count = lambda input: input['paragraph_count']
        return [[feature] for feature in list(map(extract_paragraphs_count, X))]
