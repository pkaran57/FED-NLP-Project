import logging
import pandas as pd
from typing import List, Tuple, Union

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

    @classmethod
    def get_entity_sentiment_overtime(cls, entity_name:str, entity_sentiment_result:  List[Tuple[FOMCDoc, Entity]]) -> Union[pd.DataFrame, None]:
        date_to_entity_sentiment = []
        # TODO: aggregate lower and upper case entity names, aggregate by buckets
        for fomc_doc, entities in entity_sentiment_result:
            matching_entities = [entity for entity in entities if entity_name.lower() == entity.name.lower() and entity.sentiment.score]
            if matching_entities:
                if len(matching_entities) > 1:
                    cls._logger.info("Found {} entity {} times in the same doc".format(entity_name, len(matching_entities)))
                date_to_entity_sentiment.append((fomc_doc.meeting_date, matching_entities[0].sentiment.score))
        date_to_entity_sentiment = sorted(date_to_entity_sentiment, key=lambda item: item[0])

        if date_to_entity_sentiment:
            dataframe = pd.DataFrame.from_records(date_to_entity_sentiment)
            # dataframe.to_excel(os.path.join(OUTPUT_DIR, 'sentiment-for-{}-entity-overtime.xlsx'.format(entity_name)))

            dataframe.set_index(dataframe[0], drop=True, inplace=True)
            dataframe.drop(columns=[0], inplace=True)
            dataframe.rename(columns={1: entity_name}, inplace=True)

            return dataframe
        else:
            return None

    @staticmethod
    def pretty_print_entity(entity: Entity):
        print('Name = {}, type = {}, magnitude = {}, score = {}, salience = {}'.format(entity.name, entity.type_, entity.sentiment.magnitude, entity.sentiment.score,
                                                                                       entity.salience))
