# import
import os
from datetime import date

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from wordcloud import WordCloud
from PIL import Image
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from joblib import dump, load
import string

ps = PorterStemmer()

# stopword + stemmer
nltk.download('stopwords')
stopWords = set(stopwords.words('french'))
final_stopwords_list = list(fr_stop)
stemmer = SnowballStemmer('french')

# tfidf
tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words=final_stopwords_list)


# progress bar

def clearData(dfColumn):
    dfColumn["review"] = dfColumn["review"].apply(lambda x: re.sub(r'[^\w\s]', '', x))
    dfColumn["review"] = dfColumn["review"].apply(lambda x: re.sub(r'_', ' ', x))
    dfColumn['clear_review'] = dfColumn['review'].apply(lambda x: x.lower())
    dfColumn["clear_review"] = dfColumn["clear_review"].apply(
        lambda x: ' '.join([word.lower() for word in x.split() if word not in (stopWords)]))
    dfColumn["clear_review"] = dfColumn["clear_review"].apply(
        lambda x: ' '.join([stemmer.stem(y) for y in x.split()]))  # Stem every word.


def wordcloud(df):
    coms = df
    coms.head()
    list_word = ''
    for s in coms['review']:
        for word in s.split():
            if s not in stopWords:
                list_word += s

    wordcloud = WordCloud(background_color='white', max_words=50).generate(list_word)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file('png/' + df['candidat'].max() + '.png')


def create_model(fit: bool = True, save: bool = True,
                 model_name: string = f'model_{date.today().strftime("%d/%m/%Y")}'):
    # Load csv
    df = pd.read_csv("csv/train.csv")

    # remove useless column and rename them
    df = df.drop(['film-url'], axis=1)
    df = df.drop(['Unnamed: 0'], axis=1)
    df = df.rename(columns={"polarity": "label"})
    df.head()

    clearData(df)

    # data split train / test
    X = df['clear_review']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    # dataframe train
    data_train = pd.DataFrame(columns=['clear_review', 'label'])
    data_train['clear_review'] = X_train.values
    data_train['label'] = y_train.values

    # dataframe test
    data_test = pd.DataFrame(columns=['clear_review', 'label'])
    data_test['clear_review'] = X_test.values
    data_test['label'] = y_test.values

    # vectoriz
    vectorized_train = tfidfvectorizer.fit_transform(X_train)
    vectorized_test = tfidfvectorizer.transform(X_test)

    if fit:
        # model fitting
        rfClassifier = RandomForestClassifier(n_estimators=400, criterion="entropy", random_state=0)
        rfClassifier.fit(vectorized_train, y_train)

        # model scoring
        rfPreds = rfClassifier.score(vectorized_test, y_test)
        print('model score : ' + rfPreds)

        if save:
            # save
            dump(rfClassifier, f"models/{model_name}.joblib")


def predict_tweets(model_name: string = "model_nlp_n_estimator_400_criterion_entropy_random_state_0.joblib"):
    # load
    rfClassifier = load(f"models/{model_name}")

    # Preprocessing tweet data
    df_tweet = pd.read_csv("csv/tweets.csv")
    clearData(df_tweet)
    vectorized_tweets = tfidfvectorizer.transform(df_tweet["clear_review"])

    # #model scoring on tweet
    # rfPreds_tweet = rfClassifier.score(vectorized_tweets, df_tweet["label"])
    # print('tweet score : ' + rfPreds_tweet)

    # model prediction on tweet
    rfPreds_tweet = rfClassifier.predict(vectorized_tweets)

    # graph

    df_final = df_tweet
    df_final["predicted"] = rfPreds_tweet
    df_final["candidat"] = ''

    searchList = ["zemmour", "macron", "pécresse", "mélenchon", "jadot", "dupont", "aignan", "arthaud", "hidalgo",
                  "poutou", "pen", "roussel", "lassalle"]
    df_final["candidat"] = df_final["review"].apply(
        lambda x: ' '.join([word.lower() for word in x.split() if word.lower() in searchList]))
    df_final["candidat"] = df_final["candidat"].apply(lambda x: re.sub('([a-zé]* .*)|^$', 'None', x))
    df_final["candidat"] = df_final["candidat"].apply(lambda x: re.sub('dupont|aigan', 'dupont-aigan', x))
    df_final["candidat"] = df_final["candidat"].apply(lambda x: re.sub('pen', 'le pen', x))

    df_final = df_final.sort_values(by=['candidat'])

    df_final.to_csv(r'csv\df_final.csv')

    df_zemmour = df_final.loc[df_final['candidat'] == 'zemmour']
    df_macron = df_final.loc[df_final['candidat'] == 'macron']
    df_pecresse = df_final.loc[df_final['candidat'] == 'pécresse']
    df_melenchon = df_final.loc[df_final['candidat'] == 'mélenchon']
    df_jadot = df_final.loc[df_final['candidat'] == 'jadot']
    df_dupont_aignan = df_final.loc[df_final['candidat'] == 'dupont-aigan']
    df_arthaud = df_final.loc[df_final['candidat'] == 'arthaud']
    df_hidalgo = df_final.loc[df_final['candidat'] == 'hidalgo']
    df_poutou = df_final.loc[df_final['candidat'] == 'poutou']
    df_lepen = df_final.loc[df_final['candidat'] == 'le pen']
    df_roussel = df_final.loc[df_final['candidat'] == 'roussel']
    df_lassalle = df_final.loc[df_final['candidat'] == 'lassalle']
    df_null = df_final.loc[df_final['candidat'] == 'None']

    wordcloud(df_zemmour)
    wordcloud(df_macron)
    wordcloud(df_pecresse)
    wordcloud(df_melenchon)
    wordcloud(df_jadot)
    wordcloud(df_dupont_aignan)
    wordcloud(df_arthaud)
    wordcloud(df_hidalgo)
    wordcloud(df_poutou)
    wordcloud(df_lepen)
    wordcloud(df_roussel)
    wordcloud(df_lassalle)
    wordcloud(df_null)


create_model(fit=False)
predict_tweets()
