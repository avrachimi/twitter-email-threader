
from botocore.exceptions import ClientError
import boto3
from datetime import date


def send_email(username, thread):
    SENDER = "Threader <avrachimi@gmail.com>"

    RECIPIENT = "avrachimi@hotmail.com"

    AWS_REGION = "eu-west-2"

    today = date.today().strftime("%d %B %Y")
    SUBJECT = "{} Thread: {}".format(username, today)

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = 'Tweet thread from {}: {}'.format(username, str(thread))

    # The HTML body of the email.
    html_string = ''
    with open('email.html', 'r') as f:
        html_string = f.read()
    BODY_HTML = html_string.format(username, thread)

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
