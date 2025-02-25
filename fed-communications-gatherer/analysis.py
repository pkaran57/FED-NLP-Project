# Created 3/5/2021
# This file takes fed speeches as data and performs entity analysis (entity recognition included) on them.
# The goal is to find out which terms relate to money and economics
#
# Sources:
# https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/
# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
#
# Goal: Analyze the sentiment of the speeches to find

# Import statements

# Nltk - for POS tagging and enti
import nltk
import pandas as pd
import os

# Counter import - find out how many entities of each type are in the speeches
from collections import Counter

# Spacy - alternative for entity recognition and analysis
import spacy

nlp = spacy.load("en_core_web_sm")

# # Google cloud
# from google.cloud import language_v1


# Sci-kit learn imports
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

# Required modules to do entity analysis
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("treebank")
nltk.download("words")
nltk.download("vader_lexicon")

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Sample speech to read
speech = [
    "The Federal Reserve is committed to using its full range of tools to support the U.S. economy in this challenging time, thereby promoting its maximum employment and price stability goals.",
    "The COVID-19 pandemic is causing tremendous human and economic hardship across the United States and around the world. The pace of the recovery in economic activity and employment has moderated in recent months, with weakness concentrated in the sectors most adversely affected by the pandemic. Weaker demand and earlier declines in oil prices have been holding down consumer price inflation. Overall financial conditions remain accommodative, in part reflecting policy measures to support the economy and the flow of credit to U.S. households and businesses.",
    "The path of the economy will depend significantly on the course of the virus, including progress on vaccinations. The ongoing public health crisis continues to weigh on economic activity, employment, and inflation, and poses considerable risks to the economic outlook.",
    "The Committee seeks to achieve maximum employment and inflation at the rate of 2 percent over the longer run. With inflation running persistently below this longer-run goal, the Committee will aim to achieve inflation moderately above 2 percent for some time so that inflation averages 2 percent over time and longer‑term inflation expectations remain well anchored at 2 percent. The Committee expects to maintain an accommodative stance of monetary policy until these outcomes are achieved. The Committee decided to keep the target range for the federal funds rate at 0 to 1/4 percent and expects it will be appropriate to maintain this target range until labor market conditions have reached levels consistent with the Committee's assessments of maximum employment and inflation has risen to 2 percent and is on track to moderately exceed 2 percent for some time. In addition, the Federal Reserve will continue to increase its holdings of Treasury securities by at least $80 billion per month and of agency mortgage‑backed securities by at least $40 billion per month until substantial further progress has been made toward the Committee's maximum employment and price stability goals. These asset purchases help foster smooth market functioning and accommodative financial conditions, thereby supporting the flow of credit to households and businesses.",
    "In assessing the appropriate stance of monetary policy, the Committee will continue to monitor the implications of incoming information for the economic outlook. The Committee would be prepared to adjust the stance of monetary policy as appropriate if risks emerge that could impede the attainment of the Committee's goals. The Committee's assessments will take into account a wide range of information, including readings on public health, labor market conditions, inflation pressures and inflation expectations, and financial and international developments.",
    "Voting for the monetary policy action were Jerome H. Powell, Chair; John C. Williams, Vice Chair; Thomas I. Barkin; Raphael W. Bostic; Michelle W. Bowman; Lael Brainard; Richard H. Clarida; Mary C. Daly; Charles L. Evans; Randal K. Quarles; and Christopher J. Waller.",
    "Implementation Note issued January 27, 2021",
]


# Make the speech a single string
text = " ".join(speech)
# text = speech[0]


# Create a transformer to add number of words as a feature
class NumOfWordsTransformer(BaseEstimator, TransformerMixin):
    """
    return word count for a given headline
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        word_counter = lambda input: len(re.findall(r"\w+", input))
        return [[feature] for feature in list(map(word_counter, X))]


# Read the speeches from the JSON files gathered by the fed-comms gatherer
def read_speeches():
    # Right now, the directory containing the speeches is in another module.
    # Find a way to make this code work or move all code in this file to the fed-communications-gatherer module
    speech_dir = "/Fed-NLP-Project/fed-communications-gatherer/output/policy_statements"
    all_data = []

    # For each json file, read the speech and add it.
    for speech in os.listdir(speech_dir):
        if speech.endswith(".json"):
            # Read the data
            data = pd.read_json(speech_dir + "/" + speech)

            print(data["paragraphs"])

            # Convert the
            paragraphs = data["paragraphs"].tolist()

            all_data.append(paragraphs)

    print(all_data)
    return all_data


# Main function for the code
# Use data pulled by the fed-communications-gatherer module
def main():

    # # Placeholder code to read from a csv file
    # fed_speeches = pd.read_csv("path to fed speeches.csv")

    # Set up the transformer to do sentiment analysis
    text_clf_pipeline = Pipeline(
        [
            ("num-words", NumOfWordsTransformer()),
        ]
    )

    # text_clf_pipeline.fit(speech)

    text = speech
    # for sample in text:
    text2 = " ".join(speech)

    # The next section is based on code from the source below
    # https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
    print("Here is the spacy code for entity recognition")
    doc = nlp(text2)
    print([(X.text, X.label_) for X in doc.ents])

    print("\n")

    # 41 entities exist in the example article
    # There may be more or less in other articles.
    print("Number of entities in the article")
    print(len(doc.ents))

    # Find out how many of each entity is in the article
    print("Entity types and counts")
    labels = [x.label_ for x in doc.ents]
    print(Counter(labels))

    print("\n")

    # Sentiment Analysis
    print("Sentiment Analysis")
    analyzer = SentimentIntensityAnalyzer()
    for text in speech:
        print(text)
        print(analyzer.polarity_scores(text))
        print("\n")

    # # Analyze the speech token by token
    # # Most of the words are not capitalized, leading to only a few entities
    # print("Token by token analysis")
    # print([(X, X.ent_iob_, X.ent_type_) for X in doc])


# Call the main function to start the code
main()
# read_speeches()
