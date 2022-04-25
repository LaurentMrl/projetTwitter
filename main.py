import os

os.chdir("scrapping")

from scrapping.scrapWithKeywird import scraping
from nlp.main import create_model, predict_tweets_candidats

# scrap some data
scraping(150)
# create the model
create_model()
# generate data
predict_tweets_candidats()
