import time
import tweepy
import csv

consumer_key = "WSzBqxpYLncmrQ16XdB1r8hR9"

consumer_secret = "o3TDZW11YFfnhQN6OPTMt7u0bdeuE3lQWj1TMBhaTAnMJtjsnE"

access_token = "1488132313934405634-eh70phke8cguE3apiiuZWBHZD7cvdj"

access_token_secret = "Lx9bBDHz6JF4dUcfGTc7T2K7pWr1Vs1I6TFYt50xGUqKm"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def get_followers(user_name):
    """
    get a list of all followers of a twitter account
    :param user_name: twitter username without '@' symbol
    :return: list of usernames without '@' symbol
    """
    api = tweepy.API(auth)
    followers = []
    for page in tweepy.Cursor(api.followers, screen_name=user_name, wait_on_rate_limit=True,count=200).pages():
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return followers


def save_followers_to_csv(user_name, data):
    """
    saves json data to csv
    :param data: data recieved from twitter
    :return: None
    """
    HEADERS = ["name", "screen_name", "description", "followers_count", "followers_count",
               'friends_count', "listed_count", "favourites_count", "created_at"]
    with open(user_name + "_followers.csv", 'w',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(HEADERS)
        for profile_data in data:
            profile = []
            for header in HEADERS:
                profile.append(profile_data._json[header])
            csv_writer.writerow(profile)


followers = get_followers("ZemmourEric")
save_followers_to_csv("ZemmourEric", followers)