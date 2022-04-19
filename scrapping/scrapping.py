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

account = "ZemmourEric"

user = api.get_user(screen_name=account)
# print(user.screen_name)
# print(user.followers_count)
# get description
# print(user.description)


# Get user tweets
tweets = api.user_timeline(screen_name=account, count=5, include_rts = False, tweet_mode = 'extended')
for info in tweets:
     print("ID: {}".format(info.id))
     print(info.created_at)
     print(info.full_text)
     print("\n")


# for friend in user.friends():
#    print(friend.screen_name)