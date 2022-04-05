from dataclasses import field
import requests as rq

consumer_key = "WSzBqxpYLncmrQ16XdB1r8hR9"

consumer_secret = "o3TDZW11YFfnhQN6OPTMt7u0bdeuE3lQWj1TMBhaTAnMJtjsnE"

access_token = "1488132313934405634-eh70phke8cguE3apiiuZWBHZD7cvdj"

access_token_secret = "Lx9bBDHz6JF4dUcfGTc7T2K7pWr1Vs1I6TFYt50xGUqKm"

bearer_token = "AAAAAAAAAAAAAAAAAAAAAEwGYwEAAAAAaba7gk5O4NfgE92zNzftr3u1tj4%3DepQYjPq8Bb6romcPolsAb8hrghgRSoGefBTMK3qaokwVojec45"

import base64

key_secret = f'{consumer_key}:{consumer_secret}'.encode('ascii')

import requests

base_url = 'https://api.twitter.com/'

search_headers = {
    'Authorization': f'Bearer {bearer_token}'
}

search_params = {}

username = "ZemmourEric"

fields = "?expansions=pinned_tweet_id&user.fields=public_metrics"

search_url = f'{base_url}2/users/by/username/{username}{fields}'

search_resp = requests.get(search_url, headers=search_headers)

tweet_data = search_resp.json()

print(tweet_data)