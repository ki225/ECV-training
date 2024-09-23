import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

class ConversationHistoryDB:
    def __init__(self, table_name='waf_conversation_history'):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_conversation_history(self, user_id, limit=10):
        response = self.table.query(
            KeyConditionExpression=Key('user_id').eq(user_id),
            ScanIndexForward=False,  # This will return the most recent messages first
            Limit=limit
        )
        # Reverse the order so that the oldest message comes first
        items = response['Items'][::-1]
        return [{'role': item['role'], 'content': item['content']} for item in items]

    def store_message(self, user_id, role, content):
        self.table.put_item(
            Item={
                'user_id': user_id,
                'timestamp': int(datetime.now().timestamp() * 1000),
                'role': role,
                'content': content
            }
        )

    def clear_history(self, user_id):
        # This method will delete all conversation history for a given user
        # Be cautious when using this method as it permanently deletes data
        response = self.table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        with self.table.batch_writer() as batch:
            for item in response['Items']:
                batch.delete_item(
                    Key={
                        'user_id': item['user_id'],
                        'timestamp': item['timestamp']
                    }
                )