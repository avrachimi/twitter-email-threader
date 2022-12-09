
from botocore.exceptions import ClientError
import boto3
from datetime import date
from airium import Airium

def get_HTML(user, thread, conversation_id):
    css_string = ''
    with open('email.css', 'r') as f:
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
                a(user.username)
            for tweet in reversed(thread):
                with a.p():
                    tweet = tweet.replace('\n', '<br>')
                    a(tweet)

            with a.a(href='https://twitter.com/{}/status/{}'.format(user.username, conversation_id)):
                a('View thread on Twitter')

                
    html = str(a)
    return html

def send_email(user, thread, conversation_id):
    SENDER = "Threader <avrachimi@gmail.com>"

    RECIPIENT = "avrachimi@hotmail.com"

    AWS_REGION = "eu-west-2"

    today = date.today().strftime("%d %B %Y")
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
