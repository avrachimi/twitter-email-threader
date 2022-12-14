# Twitter Email Threader
## Description

I'm not very active on Twitter nowadays and I'm missing some important tweets that contain valuable information. I wanted to create something simple that would send me an email whenever one of my favorite accounts tweeted a thread, that way I wouldn't miss any important information shared by these accounts. 

This is definitely not 'production ready' and it wasn't meant to be offered as a service. *You can clone this repo and deploy it on AWS if you still want something like this. It's practically free to run this on AWS. More info below.*

I coded it using **Python** and deployed it on **AWS** using **Lambda**, **EventBridge**, **DynamoDB** and **SES**. EventBridge was used to trigger the Lambda function **every 6 hours**.

I tried my best to write thorough instructions below, let me know if something doesn't make sense.

**Note**: Yeah I hate the nested for loops in `lambda_function.py` too, but it's good enough for my use case.

***
## How to Install and Run

1. Clone this repository and navigate into it.
2. Install the dependencies listed below using `pip3`
3. Change the list of usernames to the ones you'd like to monitor in the `lambda_function.py` file
4. Add Environment Variables in a `.env` file for Twitter (`CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN`, `TOKEN_SECRET`, `BEARER_TOKEN`) and Email (`EMAIL_SENDER`, `EMAIL_RECIPIENT`).
5. Create an AWS account if you don't have one and setup your access keys on your machine ([more info](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration))
6. Run `python3 lambda_function.py`

## How to Deploy to AWS

1. Create a Lambda deployment package following the instructions [here](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-package-with-dependency). 
   - Make sure to install all project dependencies on *step 4*
   - Also add the `models/Thread.py`, `email_template/email.css` and `ses_email.py` files in the zip file on *step 6*
2. Create a new Lambda Function and upload zip using [these instructions](https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-zip.html#configuration-function-update).
3. Add the appropriate policies to the Lambda function IAM Role for DynamoDB and SES access. ([more info](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html))
4. Change function timeout to ~30 seconds (or a longer time frame, depending on the number of Twitter users this script will go through). ([more info](https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html#configuration-timeout-console))
5. Add Environment Variables to your Lambda function for Twitter (`CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN`, `TOKEN_SECRET`, `BEARER_TOKEN`) and Email (`EMAIL_SENDER`, `EMAIL_RECIPIENT`).
6. Test your Function! You should receive a few emails with threads from the accounts you specified in *Step 3* of the previous segment.
7. Create an EventBridge Trigger for your Lambda function and schedule it to run every 6 hours. ([more info](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html))
8. Done! Things might break, sorry. Let me know if they do :)

***
### Dependencies
- [tweepy](https://www.tweepy.org/)  
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)  
- [dotenv](https://pypi.org/project/python-dotenv/)  
- [airium](https://pypi.org/project/airium/)  

### Tech Stack
- Python 3
- AWS Lambda
- AWS DynamoDB (NoSQL)
- AWS Simple Email Service
- AWS EventBridge
