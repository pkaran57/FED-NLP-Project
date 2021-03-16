import json
import os
from datetime import datetime

import numpy as np
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import LinearSVC

from fed_model_nlp.definitions import FOMC_SPEECH_SAMPLES_DIR
from fed_model_nlp.transformers.EntitySentimentTransformer import EntitySentimentTransformer
from fed_model_nlp.transformers.NumOfParagraphsTransformer import NumOfParagraphsTransformer
from fed_model_nlp.transformers.NumOfWordsTransformer import NumOfWordsTransformer
from fed_model_nlp.transformers.POSTagsCountTransformer import POSTagsCountTransformer

json_file_paths = [os.path.join(FOMC_SPEECH_SAMPLES_DIR, sample_json) for sample_json in os.listdir(FOMC_SPEECH_SAMPLES_DIR) if sample_json.endswith('.json')]

samples = []
for json_file_path in json_file_paths:
    with open(json_file_path) as json_file:
        sample = json.load(json_file)
        if sample['change_in_s_n_p_500']:
            samples.append(sample)

print(f'Found {len(samples)} samples')

samples = sorted(samples, key=lambda item: datetime.strptime(item["fomc_doc"]['meeting_date'], "%Y-%m-%d").date())
labels = ['UP' if sample["change_in_s_n_p_500"] >= 0 else 'DOWN' for sample in samples]

train_ratio = 0.80
validation_ratio = 0.10
test_ratio = 0.10

x_train, x_test, y_train, y_test = train_test_split(samples, labels, test_size=1 - train_ratio, stratify=labels)
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=test_ratio / (test_ratio + validation_ratio), stratify=y_test)

print('Samples in training set = {}, validation set = {}, test set = {}'.format(len(x_train), len(x_val), len(x_test)))

feature_transformers = [("num-words", NumOfWordsTransformer()),
                        ("num-paragraphs", NumOfParagraphsTransformer())
                        ]

for pos_tag_key in ["noun_count", "verb_count", "adjective_count"]:
    feature_transformers.append((f"pos-tags-{pos_tag_key}", POSTagsCountTransformer(pos_tag_key)))

for entity_name in ["committee", "employment", "price stability", "mandate", "inflation", "investment", "growth", "household spending", "stance", "business"]:
    feature_transformers.append((f"entity-sentiment-{entity_name}", EntitySentimentTransformer(entity_name)))


def preprocessor_func(sample):
    return " ".join(sample['fomc_doc']['paragraphs'])


feature_transformers.append(('tfidf', TfidfVectorizer(preprocessor=preprocessor_func, ngram_range=(1, 3))))

union = FeatureUnion(feature_transformers)

text_clf_pipeline = Pipeline([
    ('union', union),
    ('clf', LinearSVC(loss='squared_hinge'))
])

text_clf_pipeline.fit(x_train, y_train)

predicted = text_clf_pipeline.predict(x_test)
print('Test accuracy = ', np.mean(predicted == y_test))

print('\nF-score:\n', metrics.classification_report(y_test, predicted))

scores = cross_val_score(text_clf_pipeline, x_val, y_val, scoring='f1_macro')
print('cross-validation scores = ', scores)
print('Average cross-validation score = ', sum(scores) / len(scores))
