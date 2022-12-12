from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


class Thread:
    """Encapsulates an Amazon DynamoDB table of thread data."""

    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = None

    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.
        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                exists = False
            else:
                print("Couldn't check for existence of {}. Here's why: {}: {}".format(
                    table_name, err.response['Error']['Code'], err.response['Error']['Message']))
                raise
        else:
            self.table = table
        return exists

    def create_table(self, table_name):
        """
        Creates an Amazon DynamoDB table that can be used to store thread data.

        :param table_name: The name of the table to create.
        :return: The newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'conversation_id',
                        'KeyType': 'HASH'},  # Partition key
                    {'AttributeName': 'user_id', 'KeyType': 'RANGE'}  # Sort key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'conversation_id', 'AttributeType': 'N'},
                    {'AttributeName': 'user_id', 'AttributeType': 'N'}
                ],
                BillingMode='PAY_PER_REQUEST')
            self.table.wait_until_exists()
        except ClientError as err:
            print("Couldn't create table {}. Here's why: {}: {}".format(
                table_name, err.response['Error']['Code'], err.response['Error']['Message']))
            raise
        else:
            return self.table

    def add_thread(self, conversation_id, user_id, username):
        """
        Adds a thread to the table.
        :param conversation_id: The conversation_id of the thread.
        :param user_id: The user_id of the thread author.
        """
        try:
            self.table.put_item(
                Item={
                    'user_id': user_id,
                    'conversation_id': conversation_id,
                    'username': username})
        except ClientError as err:
            print("Couldn't add thread {} to table {}. Here's why: {}: {}".format(
                conversation_id, self.table.name, err.response['Error']['Code'], err.response['Error']['Message']))
            raise

    def get_thread(self, conversation_id, user_id):
        """
        Gets thread from the table.
        :param conversation_id: The conversation_id of the thread.
        :param user_id: The user_id of the thread author.
        :return: The data about the requested thread.
        """
        try:
            response = self.table.get_item(
                Key={'conversation_id': conversation_id, 'user_id': user_id})
        except ClientError as err:
            print("Couldn't get thread {} from table {}. Here's why: {}: {}".format(
                conversation_id, self.table.name, err.response['Error']['Code'], err.response['Error']['Message']))
            return None
        else:
            if (not 'Item' in response):
                return None
            return response['Item']

    def get_item_count(self):
        try:
            import boto3
            response = boto3.client('dynamodb').describe_table(TableName=self.table.name)
            return response['Table']['ItemCount']
        except:
            print ("Something went wrong while getting table item count")
            return -1
