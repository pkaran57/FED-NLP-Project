import logging

from src.definitions import POLICY_STATEMENTS_OUTPUT_DIR
from src.features.EntitySentimentAnalyzer import EntitySentimentAnalyzer
from src.fomc.FOMCCommunicationDocsService import FOMCCommunicationDocsService

logging.basicConfig(format="'%(asctime)s' %(name)s : %(message)s'", level=logging.INFO)
logger = logging.getLogger("main")


def get_date_to_entity_sentiment(entity_name, entity_sentiment_result):
    date_to_entity_sentiment = []
    for fomc_doc, entities in entity_sentiment_result:
        matching_entities = [entity for entity in entities if entity.name.lower() == entity_name and entity.sentiment.score]
        if matching_entities:
            if len(matching_entities) > 1:
                logger.info("Found {} entity {} times in the same doc".format(entity_name, len(matching_entities)))
            date_to_entity_sentiment.append((fomc_doc.meeting_date, matching_entities[0].sentiment.score))
    return sorted(date_to_entity_sentiment, key=lambda item: item[0])


if __name__ == "__main__":
    fomc_communication_docs_service = FOMCCommunicationDocsService()

    # Note: only run this code once to download all the FOMC documents to your local disk
    # fomc_communication_docs_service.export_fomc_docs(
    #     FOMCDocType.POLICY_STATEMENTS, POLICY_STATEMENTS_OUTPUT_DIR
    # )

    # load FOMC docs from disk
    fomc_docs = fomc_communication_docs_service.read_fomc_docs(POLICY_STATEMENTS_OUTPUT_DIR)

    # perform entity sentiment analysis
    entity_sentiment_analyzer = EntitySentimentAnalyzer()
    entity_sentiment_result = entity_sentiment_analyzer.perform_entity_sentiment_analysis(fomc_docs[100:125])
    entity_sentiment_result = sorted(entity_sentiment_result, key=lambda item: item[0].meeting_date)

    # get sentiment values for a given entity over time
    date_to_entity_sentiment = get_date_to_entity_sentiment('employment', entity_sentiment_result)
    print(date_to_entity_sentiment)
