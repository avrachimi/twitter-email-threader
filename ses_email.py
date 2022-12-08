
from botocore.exceptions import ClientError
import boto3
from datetime import date


def send_email(username, thread):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = username + " <smemseth@gmail.com>"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "avrachimi@hotmail.com"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-west-2"

    # The subject line for the email.
    today = date.today().strftime("%d %B %Y")
    SUBJECT = "Twitter Threads: " + today

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ('Tweet thread from ' + username + ': ' + str(thread))

    # The HTML body of the email.
    html_string = ''
    with open('email.html', 'r') as f:
        html_string = f.read()
    BODY_HTML = html_string.format(username, thread)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
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
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
