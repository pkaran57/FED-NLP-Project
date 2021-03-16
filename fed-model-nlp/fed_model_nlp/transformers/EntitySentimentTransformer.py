from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler


class EntitySentimentTransformer(BaseEstimator, TransformerMixin):
    """
    return pos tags count
    """

    def __init__(self, entity_name):
        self.entity_name = entity_name

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        features = [[feature] for feature in list(map(self.extract_entity_sentiment_score, X))]

        min_max_scaler = MinMaxScaler()
        min_max_scaler.fit(features)
        return min_max_scaler.transform(features)

    def extract_entity_sentiment_score(self, sample):
        if self.entity_name in sample['entity_sentiments']:
            return sample['entity_sentiments'][self.entity_name]['score']
        else:
            return 0
