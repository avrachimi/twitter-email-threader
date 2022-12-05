from dotenv import load_dotenv
load_dotenv()

import os
import json
import tweepy

client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))

user = client.get_user(username='punk6529')
print(user.data.id)



tweets = client.get_users_tweets(user.data.id)
for tweet in tweets:
    print(tweet)