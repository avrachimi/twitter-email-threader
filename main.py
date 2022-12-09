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
threads_table_exists = threads.exists(table_name)
if not threads_table_exists:
    print(f"\nCreating table '{table_name}'...")
    threads.create_table(table_name)
    print(f"\nCreated table '{threads.table.name}'.")

# Look through users' tweets to find threads
for username in usernames:
    user = client.get_user(username=username, user_fields=['profile_image_url'])
    print('Username: {}, User ID: {}'.format(str(user.data.username), str(user.data.id)))

    thread = []
    in_conversation = False
    found_thread = False
    for tweets in tweepy.Paginator(client.get_users_tweets, user.data.id, exclude=['retweets', 'replies'], tweet_fields=['conversation_id']):
        for tweet in tweets.data:
            if not (tweet.conversation_id == tweet.id):
                thread_exists = threads.get_thread(tweet.conversation_id, user.data.id) != None
                if (thread_exists):
                    found_thread = True
                    print('Thread {} already exists in DB'.format(tweet.conversation_id))
                    break
                thread.append(tweet.text)
                in_conversation = True
            elif (in_conversation and tweet.conversation_id == tweet.id):
                thread.append(tweet.text)
                threads.add_thread(tweet.conversation_id, user.data.id, user.data.username)
                in_conversation = False
                found_thread = True

                send_email(user.data, thread, tweet.conversation_id)

                break

        if (found_thread):
            break
