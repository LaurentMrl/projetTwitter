from dis import disassemble
import tweepy
import re
import csv
import os

consumer_key = "WSzBqxpYLncmrQ16XdB1r8hR9"

consumer_secret = "o3TDZW11YFfnhQN6OPTMt7u0bdeuE3lQWj1TMBhaTAnMJtjsnE"

access_token = "1488132313934405634-eh70phke8cguE3apiiuZWBHZD7cvdj"

access_token_secret = "Lx9bBDHz6JF4dUcfGTc7T2K7pWr1Vs1I6TFYt50xGUqKm"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

search_word = "Zemmour"

tweet_file = "csv/candidats/tweets.csv"

searchList = ["Zemmour", "Macron", "Pécresse", "Mélenchon", "Jadot", "Dupont-Aignan", "Arthaud", "Hidalgo", "Poutou",
              "Le Pen", "Roussel", "Lassalle"]

# remove csv if exists
if os.path.exists(tweet_file):
    os.remove(tweet_file)

# create csv and column
with open(tweet_file, "a", encoding="utf-8-sig") as f:
    write = csv.writer(f)
    write.writerow(['review'])


# add tweets to csv
def appendToCSV(bigList):
    with open(tweet_file, "a", encoding="utf-8-sig") as f:
        write = csv.writer(f)
        write.writerows(bigList)
    print("Tweet appened to CSV")


# scrapping method with n as nb of  tweets/candidat
def scraping(n):
    for candidt in searchList:
        tweets = tweepy.Cursor(api.search_tweets, q=candidt, lang="fr", tweet_mode='extended').items(n)
        for tweet in tweets:
            tweetList = []
            if 'retweeted_status' in tweet._json:
                full_text = tweet._json['retweeted_status']['full_text']
                line = re.sub(r"RT @.*: ", "", full_text)
                line = re.sub(r"\n", "", line)
                tweetList.append(line)
                print("retweet : ")
                print(line)
                print("Fin du tweet")
                bigList = [tweetList]
                appendToCSV(bigList)
            else:
                line = re.sub(r"RT @.*: ", "", tweet.full_text)
                line = re.sub(r"\n", "", line)
                tweetList.append(line)
                print(line)
                bigList = [tweetList]
                appendToCSV(bigList)


if __name__ == "__scrapWithKeywird__":
    scraping(150)
