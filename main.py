#!/usr/bin/python3

import tweepy
import os
from dotenv import load_dotenv
load_dotenv()
from ses_email import send_email


client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))

usernames = ['Loopifyyy', 'punk6529']


for username in usernames:
    user = client.get_user(username=username)
    print('Username: ' + str(user.data.username) +
          ', User ID: ' + str(user.data.id))

    thread = []
    in_conversation = False
    found_thread = False
    for tweets in tweepy.Paginator(client.get_users_tweets, user.data.id, exclude=['retweets', 'replies'], tweet_fields=['conversation_id']):
        for tweet in tweets.data:
            # TODO: Also check if this conversation_id is already saved in DB
            if not (tweet.conversation_id == tweet.id):
                thread.append(tweet.text)
                in_conversation = True
            elif (in_conversation and tweet.conversation_id == tweet.id):
                thread.append(tweet.text)
                in_conversation = False
                found_thread = True
                break
        if (found_thread):
            break
    
    temp = ''
    for tweet in reversed(thread):
        temp += tweet + '\n'
        print('Tweet:\n' + tweet)
    send_email(user.data.username, temp)

