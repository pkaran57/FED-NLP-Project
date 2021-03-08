import logging
from typing import List, Tuple

from google.cloud.language_v1 import LanguageServiceClient, Entity, Document
from tqdm import tqdm

from src.fomc.FOMCDoc import FOMCDoc


class EntitySentimentAnalyzer:
    _logger = logging.getLogger("EntitySentimentAnalyzer")

    def __init__(self):
        self._gcp_client = LanguageServiceClient()

    def perform_entity_sentiment_analysis(self, docs: List[FOMCDoc]) -> List[Tuple[FOMCDoc, Entity]]:
        self._logger.info('Performing entity sentiment analysis on {} FOMC documents ...'.format(len(docs)))

        doc_to_sentiment_list = []
        for fomc_doc in tqdm(docs):
            document = Document(content=fomc_doc.get_content(), type_=Document.Type.PLAIN_TEXT)
            response = self._gcp_client.analyze_entity_sentiment(document=document)

            doc_to_sentiment_list.append((fomc_doc, response.entities))
        return doc_to_sentiment_list

    @staticmethod
    def pretty_print_entity(entity: Entity):
        print('Name = {}, type = {}, magnitude = {}, score = {}, salience = {}'.format(entity.name, entity.type_, entity.sentiment.magnitude, entity.sentiment.score,
                                                                                       entity.salience))
