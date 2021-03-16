from sklearn.base import BaseEstimator, TransformerMixin


class POSTagsCountTransformer(BaseEstimator, TransformerMixin):
    """
    return pos tags count
    """

    def __init__(self, pos_tag_key):
        self.pos_tag_key = pos_tag_key

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        extract_pos_tag_count = lambda input: input['pos_tags_count'][self.pos_tag_key]
        return [[feature] for feature in list(map(extract_pos_tag_count, X))]
