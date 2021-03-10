import logging
import os
import pandas as pd

from src.definitions import POLICY_STATEMENTS_OUTPUT_DIR, OUTPUT_DIR
from src.features.EntitySentimentAnalyzer import EntitySentimentAnalyzer
from src.fomc.FOMCCommunicationDocsService import FOMCCommunicationDocsService
from src.fomc.FOMCFeatureGenerator import FOMCFeatureGenerator
from src.fomc.client.domain.FOMCDocType import FOMCDocType
from src.plot.PlotterUtil import PlotterUtil

logging.basicConfig(format="'%(asctime)s' %(name)s : %(message)s'", level=logging.INFO)
logger = logging.getLogger("main")


def get_entity_doc_counts(entity_sentiment_result):
    entity_to_count_dict = dict()
    for fomc_doc, entities in entity_sentiment_result:
        entity_names_in_doc = {
            entity.name.lower() for entity in entities if entity.sentiment.score
        }
        for entity_name in entity_names_in_doc:
            if entity_name in entity_to_count_dict:
                entity_to_count_dict[entity_name] = (
                    entity_to_count_dict[entity_name] + 1
                )
            else:
                entity_to_count_dict[entity_name] = 1
    return entity_to_count_dict


def plot_entity_sentiments_over_time(entity_sentiment_result):
    sentiment_over_time_dfs = []
    for entity in [
        "inflation",
        "risks",
        "growth"
        "employment",
        "price stability",
        "unemployment rate",
        "inflation expectations",
        "job gain",
        "oil prices",
        "economy",
        "monetary policy",
        "labor market",
        "housing",
    ]:
        date_to_entity_sentiment = (
            EntitySentimentAnalyzer.get_entity_sentiment_overtime(
                entity, entity_sentiment_result
            )
        )
        if date_to_entity_sentiment is not None:
            sentiment_over_time_dfs.append(date_to_entity_sentiment)
    PlotterUtil.plot_entity_sentiments_over_time(sentiment_over_time_dfs)


if __name__ == "__main__":
    fomc_communication_docs_service = FOMCCommunicationDocsService()

    # Note: only run this code once to download all the FOMC documents to your local disk
    # fomc_communication_docs_service.export_fomc_docs(
    #     FOMCDocType.POLICY_STATEMENTS, POLICY_STATEMENTS_OUTPUT_DIR
    # )

    # load FOMC docs from disk
    fomc_docs = fomc_communication_docs_service.read_fomc_docs(
        POLICY_STATEMENTS_OUTPUT_DIR
    )

    # perform entity sentiment analysis
    entity_sentiment_analyzer = EntitySentimentAnalyzer()
    entity_sentiment_result = (
        entity_sentiment_analyzer.perform_entity_sentiment_analysis(fomc_docs)
    )
    entity_sentiment_result = sorted(
        entity_sentiment_result, key=lambda item: item[0].meeting_date
    )

    # generate and output samples for every doc
    # FOMCFeatureGenerator().generate_and_output_features(entity_sentiment_result)

    # get sentiment values for a given entity over time
    plot_entity_sentiments_over_time(entity_sentiment_result)

    # identify most common entities for which sentiment exists
    entity_to_count_dict = get_entity_doc_counts(entity_sentiment_result)
    pd.DataFrame.from_dict(entity_to_count_dict, orient="index").to_csv(
        os.path.join(OUTPUT_DIR, "entity-count.csv")
    )
