import time
import tweepy
import csv

consumer_key = "WSzBqxpYLncmrQ16XdB1r8hR9"

consumer_secret = "o3TDZW11YFfnhQN6OPTMt7u0bdeuE3lQWj1TMBhaTAnMJtjsnE"

access_token = "1488132313934405634-eh70phke8cguE3apiiuZWBHZD7cvdj"

access_token_secret = "Lx9bBDHz6JF4dUcfGTc7T2K7pWr1Vs1I6TFYt50xGUqKm"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
  
# the screen_name of the targeted user
account = "Filou_La_malice"
  
# getting all the friends
c = tweepy.Cursor(api.get_followers, screen_name=account)
# https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-followers-list
  
# counting the number of followers
followersList = []
try:
    for follower in c.items(5):
        followersList.append(follower)
except:
    print(f"Ya une erreur surement trop de request")
for follower in followersList:
    print(follower.screen_name)
print(account + " has " + str(len(followersList)) + " followers.")