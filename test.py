import time
import tweepy
import csv

consumer_key = "WSzBqxpYLncmrQ16XdB1r8hR9"

consumer_secret = "o3TDZW11YFfnhQN6OPTMt7u0bdeuE3lQWj1TMBhaTAnMJtjsnE"

access_token = "1488132313934405634-eh70phke8cguE3apiiuZWBHZD7cvdj"

access_token_secret = "Lx9bBDHz6JF4dUcfGTc7T2K7pWr1Vs1I6TFYt50xGUqKm"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

account = "elonmusk"

api = tweepy.API(auth)

followers = []

user = api.get_user(screen_name=account)

for friend in user.friends():
   print(friend.screen_name)

print(len(followers))


# def save_followers_to_csv(user_name, data):
#     """
#     saves json data to csv
#     :param data: data recieved from twitter
#     :return: None
#     """
#     HEADERS = ["name", "screen_name", "description", "followers_count",
#                'friends_count', "listed_count", "favourites_count", "created_at"]
#     with open(user_name + "_followers.csv", 'w',encoding="utf-8") as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow(HEADERS)
#         for profile_data in data:
#             profile = []
#             for header in HEADERS:
#                 profile.append(profile_data._json[header])
#             csv_writer.writerow(profile)

# save_followers_to_csv("elonmusk", followers)