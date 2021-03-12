import logging
import os
import pandas as pd

from src.definitions import POLICY_STATEMENTS_OUTPUT_DIR, OUTPUT_DIR
from src.features.EntitySentimentAnalyzer import EntitySentimentAnalyzer
from src.fomc.FOMCCommunicationDocsService import FOMCCommunicationDocsService
from src.fomc.FOMCFeatureGenerator import FOMCFeatureGenerator
from src.fomc.client.domain.FOMCDocType import FOMCDocType
from src.plot.PlotterUtil import PlotterUtil


# NLTK for bigram counts
import nltk
nltk.download('averaged_perceptron_tagger')

logging.basicConfig(format="'%(asctime)s' %(name)s : %(message)s'", level=logging.INFO)
logger = logging.getLogger("main")


# Feature extraction functions
# The ultimate goal is to pass the following input to the DNN:
# - Every speech is an array of features. The features include paragraph count, word count, POS tags, etc.

# Feature extraction: Get number of paragraphs per speech.
# Return a list of paragraph counts where each entry is for one speech.
def get_number_of_paragraphs(docs):
	paragraph_count = []
	for fomc_doc in docs:
		#print("Document")
		#print(len(fomc_doc.paragraphs))
		#print("\n")
		paragraph_count.append(len(fomc_doc.paragraphs))
	return paragraph_count

# Feature extraction: Get number of words per speech.
# Return a list of word counts where each entry is for one speech.
# This also happens to be the unigram count.
def get_word_count(docs):
	word_count = []
	for fomc_doc in docs:
		speech = " ".join(fomc_doc.paragraphs)
		word_list = speech.split()
		#print(len(word_list))
		word_count.append(len(word_list))
	return word_count

# Feature extraction: Get number of words per speech.
# Return a list of word counts where each entry is for one speech.
# This also happens to be the unigram count.
# n=1 for unigram
# n=2 for bigram
# n=3 for trigram
def get_ngram_count(docs, n=1):
	ngram_count = []
	for fomc_doc in docs:
		speech = " ".join(fomc_doc.paragraphs)
		word_list = speech.split()
		#print(list(nltk.ngrams(word_list, n)))
		#print(len(list(nltk.ngrams(word_list, n))))
		ngram_count.append(len(list(nltk.ngrams(word_list, n))))
	return ngram_count

# Feature extraction: Get the number of nouns, verbs, and adjectives per speech
def get_pos_tags(docs):
	noun_count = []
	verb_count = []
	adjective_count = []
	
	# For each speech, split it, tokenize it, pos tag it, and find out how many are nouns/verbs/adjectives
	# NN = noun
	# VB = verb
	# JJ = adjective
	for fomc_doc in docs:
		speech = " ".join(fomc_doc.paragraphs)
		#word_list = speech.split()
		tags = nltk.pos_tag(nltk.word_tokenize(speech))
		print(tags)

	return noun_count, verb_count, adjective_count




# Extract features from the FOMC docs
def get_features(docs):
	# 3/8/2021 - Perform feature extraction on the FOMC speeches.
    p_count = get_number_of_paragraphs(fomc_docs)
    word_count = get_word_count(fomc_docs)
    unigram_count = get_ngram_count(fomc_docs, 1)
    bigram_count = get_ngram_count(fomc_docs, 2)
    trigram_count = get_ngram_count(fomc_docs, 3)
    nouns, verbs, adjs = get_pos_tags(fomc_docs)

    # Create the dataframe storing the features.
    # This will be used as the input to the DNN.
    # Each row represents one speech and its features.
    data = {"paragraph count": p_count, "word count": word_count, "unigram count": unigram_count, "bigram count": bigram_count, "trigram count": trigram_count}
    features = pd.DataFrame.from_dict(data).to_csv(os.path.join(OUTPUT_DIR, 'features_DEBUG.csv'), index=False)


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


# Call the main function
if __name__ == "__main__":
    fomc_communication_docs_service = FOMCCommunicationDocsService()


    # #Note: only run this code once to download all the FOMC documents to your local disk
    # fomc_communication_docs_service.export_fomc_docs(
    #     FOMCDocType.POLICY_STATEMENTS, POLICY_STATEMENTS_OUTPUT_DIR
    # )



    # load FOMC docs from disk
    fomc_docs = fomc_communication_docs_service.read_fomc_docs(
        POLICY_STATEMENTS_OUTPUT_DIR
    )

    # # 3/8/2021 - Perform feature extraction on the FOMC speeches.
    # Save the results to a file
    get_features(fomc_docs)
    # p_count = get_number_of_paragraphs(fomc_docs)
    # word_count = get_word_count(fomc_docs)
    # unigram_count = get_ngram_count(fomc_docs, 1)
    # bigram_count = get_ngram_count(fomc_docs, 2)
    # trigram_count = get_ngram_count(fomc_docs, 3)

    # # Create the dataframe storing the features.
    # # This will be used as the input to the DNN.
    # # Each row represents one speech and its features.
    # data = {"paragraph count": p_count, "word count": word_count, "unigram count": unigram_count, "bigram count": bigram_count, "trigram count": trigram_count}
    # features = pd.DataFrame.from_dict(data).to_csv(os.path.join(OUTPUT_DIR, 'features_DEBUG.csv'), index=False)


    # perform entity sentiment analysis
    entity_sentiment_analyzer = EntitySentimentAnalyzer()
    entity_sentiment_result = (
        entity_sentiment_analyzer.perform_entity_sentiment_analysis(fomc_docs)
    )
    entity_sentiment_result = sorted(
        entity_sentiment_result, key=lambda item: item[0].meeting_date
    )

    # get sentiment values for a given entity over time
    plot_entity_sentiments_over_time(entity_sentiment_result)

    # identify most common entities for which sentiment exists
    entity_to_count_dict = get_entity_doc_counts(entity_sentiment_result)
    pd.DataFrame.from_dict(entity_to_count_dict, orient="index").to_csv(
        os.path.join(OUTPUT_DIR, "entity-count.csv")
    )

