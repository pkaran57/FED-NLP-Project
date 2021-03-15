import json
import os
from datetime import datetime

import numpy as np
from sklearn import metrics
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline, FeatureUnion

from fed_model_nlp.definitions import FOMC_SPEECH_SAMPLES_DIR
from fed_model_nlp.transformers.NumOfWordsTransformer import NumOfWordsTransformer

json_file_paths = [os.path.join(FOMC_SPEECH_SAMPLES_DIR, sample_json) for sample_json in os.listdir(FOMC_SPEECH_SAMPLES_DIR) if sample_json.endswith('.json')]

samples = []
for json_file_path in json_file_paths:
    with open(json_file_path) as json_file:
        sample = json.load(json_file)
        if sample['change_in_s_n_p_500']:
            samples.append(sample)

print(f'Found {len(samples)}. samples')

samples = sorted(samples, key=lambda item: datetime.strptime(item["fomc_doc"]['meeting_date'], "%Y-%m-%d").date())
labels = ['UP' if sample["change_in_s_n_p_500"] >= 0 else 'DOWN' for sample in samples]

train_ratio = 0.80
validation_ratio = 0.10
test_ratio = 0.10

x_train, x_test, y_train, y_test = train_test_split(samples, labels, test_size=1 - train_ratio, stratify=labels)
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=test_ratio / (test_ratio + validation_ratio), stratify=y_test)

print('Samples in training set = {}, validation set = {}, test set = {}'.format(len(x_train), len(x_val), len(x_test)))

union = FeatureUnion([("num-words", NumOfWordsTransformer())
                      # ('vect', CountVectorizer(ngram_range=(1, 2))),
                      # ("repeating-punctuations", RepeatingPunctuationsTransformer()),
                      # ("emo-features-transformer", EmoFeaturesTransformer(add_intensity=True))
                      ])

text_clf_pipeline = Pipeline([
    ('union', union),
    # ('tfidf', TfidfTransformer(use_idf=False)),
    ('clf', MultinomialNB(alpha=0.01)),
])

text_clf_pipeline.fit(x_train, y_train)

predicted = text_clf_pipeline.predict(x_test)
print('Test accuracy = ', np.mean(predicted == y_test))

print('\nF-score:\n', metrics.classification_report(y_test, predicted))

scores = cross_val_score(text_clf_pipeline, x_val, y_val, scoring='f1_macro')
print('cross-validation scores = ', scores)
print('Average cross-validation score = ', sum(scores) / len(scores))