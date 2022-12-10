#!/usr/bin/python3

from models.Thread import Thread
import boto3
from ses_email import send_email
import tweepy
import os
from datetime import date
from dotenv import load_dotenv
load_dotenv()


client_bearer = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))

client = tweepy.Client(
    consumer_key=os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('TOKEN_SECRET')
)

usernames = ['Loopifyyy', 'punk6529', 'OGDfarmer', 'BoredApeYC',
             'Hackatao', 'cobie', 'punk9059', 'iamDCinvestor']

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
    user = client_bearer.get_user(username=username, user_fields=['profile_image_url'])
    print('Username: {}, User ID: {}'.format(str(user.data.username), str(user.data.id)))

    thread = []
    in_conversation = False
    found_thread = False
    conversation_id = None
    for tweets in tweepy.Paginator(client.get_users_tweets, user.data.id, exclude=['retweets', 'replies'], expansions=['attachments.media_keys'],
                                   max_results=100, media_fields=['url'], tweet_fields=['conversation_id'], user_auth=True):
        for tweet in tweets.data:
            if not (tweet.conversation_id == tweet.id) and (tweet.conversation_id != None):
                thread_exists = (threads.get_thread(tweet.conversation_id, user.data.id) != None)
                if (thread_exists):
                    found_thread = True
                    print('Thread {} already exists in DB'.format(
                        tweet.conversation_id))
                    break
                #print(tweets.includes['media'][15].url)
                thread.append({'text': tweet.text, 'media_url': None}) #TODO: find images for each tweet
                in_conversation = True
                conversation_id = tweet.conversation_id
            elif (in_conversation and conversation_id == tweet.id):
                thread.append({'text': tweet.text, 'media_url': None}) #TODO: find images for each tweet
                threads.add_thread(tweet.conversation_id, user.data.id, user.data.username)
                in_conversation = False
                found_thread = True

                send_email(user.data, thread, tweet.conversation_id)

                break

        if (found_thread):
            break
