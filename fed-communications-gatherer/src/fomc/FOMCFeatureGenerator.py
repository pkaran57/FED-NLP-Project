import os

import requests
from typing import Tuple, List

from google.cloud.language_v1 import Entity

from src.definitions import FEATURES_OUTPUT_DIR
from src.fomc.FOMCDoc import FOMCDoc
from src.fomc.FOMCDocSample import FOMCDocSample


class FOMCFeatureGenerator:

    def __init__(self):
        pass

    def generate_and_output_features(self, entity_sentiment_result: List[Tuple[FOMCDoc, Entity]]):

        for fomc_doc, entity in entity_sentiment_result:
            meeting_date = fomc_doc.meeting_date
            entity_sentiments = self._get_entity_sentiments_dict(entity)
            sample = FOMCDocSample(fomc_doc=fomc_doc, entity_sentiments=entity_sentiments, change_in_vix=self.find_perct_change(meeting_date, 'VXX'), change_in_s_n_p_500=self.find_perct_change(meeting_date, 'SPY'))
            sample.export_to_disk(os.path.join(FEATURES_OUTPUT_DIR))

    @staticmethod
    def find_perct_change(meeting_date, ticker):
        response_s_and_p = requests.get(
            f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{str(meeting_date)}/{str(meeting_date)}?unadjusted=false&sort=asc&limit=120&apiKey=').json()
        perct_change = None
        if 'results' in response_s_and_p:
            result = response_s_and_p['results'][0]
            perct_change = ((result['c'] - result['o']) / result['c']) * 100

        return perct_change

    @staticmethod
    def _get_entity_sentiments_dict(entity):
        entity_sentiments = dict()
        for ent in entity:
            if ent.sentiment.score and ent.name not in entity_sentiments:
                entity_sentiments[ent.name] = {
                    'score': ent.sentiment.score,
                    'magnitude': ent.sentiment.magnitude,
                    'salience': ent.salience
                }
        return entity_sentiments
