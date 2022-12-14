import os
from botocore.exceptions import ClientError
import boto3
from datetime import datetime
from airium import Airium

def get_HTML(user, thread, conversation_id):
    css_string = ''
    with open('email_template/email.css', 'r') as f:
        css_string = f.read()
    a = Airium()

    a('<!DOCTYPE html>')
    with a.html():
        with a.head():
            with a.style():
                a(css_string)
        with a.body():
            a.img(src=user.profile_image_url, alt="{}'s profile picture".format(user.username))
            with a.h1():
                a(user.name)
            with a.h2():
                a('@' + user.username)
            for tweet_obj in reversed(thread):
                with a.p():
                    tweet_obj['text'] = tweet_obj['text'].replace('\n', '<br>')
                    a(tweet_obj['text'])
                    if (tweet_obj['media_url'] != None):
                        a.img(src=tweet_obj['media_url'])

            with a.a(href='https://twitter.com/{}/status/{}'.format(user.username, conversation_id)):
                a('View thread on Twitter')

                
    html = str(a)
    return html

def send_email(user, thread, conversation_id):
    SENDER = "Threader <{}>".format(os.getenv('EMAIL_SENDER'))

    RECIPIENT = os.getenv('EMAIL_RECIPIENT')

    AWS_REGION = "eu-west-2"

    today = datetime.today().strftime("%d %B %Y, %H:%M")
    SUBJECT = "{} Thread: {}".format(user.username, today)

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = 'Tweet thread from {}: {}'.format(user.username, str(thread))

    # The HTML body of the email.
    BODY_HTML = get_HTML(user, thread, conversation_id)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
