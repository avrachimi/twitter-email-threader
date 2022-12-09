#!/usr/bin/python3

from models.Thread import Thread
import boto3
from ses_email import send_email
import tweepy
import os
from dotenv import load_dotenv
load_dotenv()


client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))

usernames = ['Loopifyyy', 'punk6529']

# Setup DynamoDB table
table_name = 'thread'
threads = Thread(boto3.resource('dynamodb'))
threads_exists = threads.exists(table_name)
if not threads_exists:
    print(f"\nCreating table '{table_name}'...")
    threads.create_table(table_name)
    print(f"\nCreated table '{threads.table.name}'.")

# Look through users' tweets to find threads
for username in usernames:
    user = client.get_user(username=username)
    print('Username: ' + str(user.data.username) +
          ', User ID: ' + str(user.data.id))

    thread = []
    in_conversation = False
    found_thread = False
    conversation_id = None
    for tweets in tweepy.Paginator(client.get_users_tweets, user.data.id, exclude=['retweets', 'replies'], tweet_fields=['conversation_id']):
        for tweet in tweets.data:
            if not (tweet.conversation_id == tweet.id):
                if (threads.get_thread(tweet.conversation_id, user.data.id) != None):
                    found_thread = True
                    print('Thread {} already exists in DB'.format(tweet.conversation_id))
                    break
                thread.append(tweet.text)
                in_conversation = True
                conversation_id = tweet.conversation_id
            elif (in_conversation and tweet.conversation_id == tweet.id):
                thread.append(tweet.text)
                in_conversation = False
                found_thread = True
                break

        if (found_thread):
            if (conversation_id != None):
                threads.add_thread(conversation_id, user.data.id, user.data.username)
            else:
                found_thread = False

            break

    if (found_thread):
        temp = ''
        for tweet in reversed(thread):
            temp += tweet + '\n'
            print('Tweet:\n' + tweet)
        send_email(user.data.username, temp)
