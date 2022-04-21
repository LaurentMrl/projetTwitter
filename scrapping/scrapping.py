import csv
import os
import re
import string

import tweepy

consumer_key = "WSzBqxpYLncmrQ16XdB1r8hR9"

consumer_secret = "o3TDZW11YFfnhQN6OPTMt7u0bdeuE3lQWj1TMBhaTAnMJtjsnE"

access_token = "1488132313934405634-eh70phke8cguE3apiiuZWBHZD7cvdj"

access_token_secret = "Lx9bBDHz6JF4dUcfGTc7T2K7pWr1Vs1I6TFYt50xGUqKm"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# Get your timeline tweets
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)


# user = api.get_user(screen_name=account)


# print(user.screen_name)
# print(user.followers_count)
# get description
# print(user.description)


# Get user tweets
# tweets = api.user_timeline(screen_name=account, count=500, include_rts=False, tweet_mode='extended')
# for info in tweets:
#     print("ID: {}".format(info.id))
#     print(info.created_at)
#     print(info.full_text)
#     print("\n")

# for friend in user.friends():
#    print(friend.screen_name)

csv_users_dir = f'{os.getcwd()}/../scrapping/csv/users/'

def create_csv(account: str):
    # create directory for the user
    if not os.path.exists(f'{csv_users_dir}{account}'):
        os.mkdir(f'{csv_users_dir}{account}')
    # remove csv if exists
    if os.path.exists(f'{csv_users_dir}{account}/tweets_{account}.csv'):
        os.remove(f'{csv_users_dir}{account}/tweets_{account}.csv')

    # create csv and column
    with open(f'{csv_users_dir}{account}/tweets_{account}.csv', "a", encoding="utf-8-sig") as f:
        write = csv.writer(f)
        write.writerow(['review'])


# add tweets to csv
def appendToCSV(bigList, account: str):
    with open(f'{csv_users_dir}{account}/tweets_{account}.csv', "a", encoding="utf-8-sig") as f:
        write = csv.writer(f)
        write.writerows(bigList)
    print("Tweet appened to CSV")


def scraping_user(account: str, n: int = 500):
    create_csv(account)
    tweets = api.user_timeline(screen_name=account, count=n, include_rts=False, tweet_mode='extended')
    for tweet in tweets:
        tweetList = []
        line = re.sub(r"RT @.*: ", "", tweet.full_text)
        line = re.sub(r"\n", "", line)
        tweetList.append(line)
        print(line)
        bigList = [tweetList]
        appendToCSV(bigList, account=account)



