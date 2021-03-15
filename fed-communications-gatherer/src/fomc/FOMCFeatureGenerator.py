import logging

import os

import nltk
import requests
from typing import Tuple, List, Dict

from google.cloud.language_v1 import Entity

from src.definitions import FEATURES_OUTPUT_DIR, POLYGON_API_KEY
from src.fomc.FOMCDoc import FOMCDoc
from src.fomc.FOMCDocSample import FOMCDocSample


class FOMCFeatureGenerator:
    _logger = logging.getLogger("FOMCFeatureGenerator")

    def __init__(self):
        pass

    def generate_and_output_features(
        self, entity_sentiment_result: List[Tuple[FOMCDoc, Entity]]
    ):
        s_and_p_exist_counter = 0
        vix_exist_counter = 0

        for fomc_doc, entity in entity_sentiment_result:
            meeting_date = fomc_doc.meeting_date
            entity_sentiments = self._get_entity_sentiments_dict(entity)

            change_in_vix = self.find_percent_change(meeting_date, "VXX")
            if change_in_vix:
                vix_exist_counter += 1
            change_in_s_n_p_500 = self.find_percent_change(meeting_date, "SPY")
            if change_in_s_n_p_500:
                s_and_p_exist_counter += 1

            sample = FOMCDocSample(
                fomc_doc=fomc_doc,
                entity_sentiments=entity_sentiments,
                paragraph_count=len(fomc_doc.paragraphs),
                word_count=self._get_word_count(fomc_doc),
                n_gram_count={
                    1: self._get_ngram_count(fomc_doc, 1),
                    2: self._get_ngram_count(fomc_doc, 2),
                    3: self._get_ngram_count(fomc_doc, 3),
                },
                pos_tags_count=self._get_pos_tags_count(fomc_doc),
                change_in_vix=change_in_vix,
                change_in_s_n_p_500=change_in_s_n_p_500,
            )
            sample.export_to_disk(os.path.join(FEATURES_OUTPUT_DIR))

        self._logger.info(
            "Samples for which VIX label found = {}, S & P 500 label found = {}".format(
                vix_exist_counter, s_and_p_exist_counter
            )
        )

    @staticmethod
    def find_percent_change(meeting_date, ticker):
        response_s_and_p = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{str(meeting_date)}/{str(meeting_date)}?unadjusted=false&sort=asc&limit=120&apiKey={POLYGON_API_KEY}"
        ).json()
        perct_change = None
        if "results" in response_s_and_p:
            result = response_s_and_p["results"][0]
            perct_change = ((result["c"] - result["o"]) / result["c"]) * 100

        return perct_change

    @staticmethod
    def _get_entity_sentiments_dict(entity):
        entity_sentiments = dict()
        for ent in entity:
            if ent.sentiment.score and ent.name not in entity_sentiments:
                entity_sentiments[ent.name] = {
                    "score": ent.sentiment.score,
                    "magnitude": ent.sentiment.magnitude,
                    "salience": ent.salience,
                }
        return entity_sentiments

    # Feature extraction: Get number of words per speech.
    # Return a list of word counts where each entry is for one speech.
    # This also happens to be the unigram count.
    @staticmethod
    def _get_word_count(fomc_doc):
        speech = " ".join(fomc_doc.paragraphs)
        word_list = speech.split()
        return len(word_list)

    # Feature extraction: Get number of words per speech.
    # Return a list of word counts where each entry is for one speech.
    # This also happens to be the unigram count.
    # n=1 for unigram
    # n=2 for bigram
    # n=3 for trigram
    @staticmethod
    def _get_ngram_count(fomc_doc, n=1):
        speech = " ".join(fomc_doc.paragraphs)
        word_list = speech.split()
        return len(list(nltk.ngrams(word_list, n)))

    # Feature extraction: Get the number of nouns, verbs, and adjectives per speech
    @staticmethod
    def _get_pos_tags_count(fomc_doc: FOMCDoc) -> Dict:

        # For each speech, split it, tokenize it, pos tag it, and find out how many are nouns/verbs/adjectives
        # NN = noun
        # VB = verb
        # JJ = adjective
        noun_count = 0
        verb_count = 0
        adjective_count = 0

        speech = " ".join(fomc_doc.paragraphs)
        tags = nltk.pos_tag(nltk.word_tokenize(speech))

        # For each tag, find out if it is a noun, verb, or adjective
        for (word, tag) in tags:
            if tag == "NN":
                noun_count += 1
            elif tag == "JJ":
                adjective_count += 1
            elif tag == "VB":
                verb_count += 1

        return {
            "noun_count": noun_count,
            "verb_count": verb_count,
            "adjective_count": adjective_count,
        }
