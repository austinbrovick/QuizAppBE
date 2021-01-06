import boto3
import uuid


dynamo_client = boto3.client('dynamodb')

def get_items():
    return dynamo_client.scan(
        TableName='QuizTable'
    )

def create_quiz_question():
    return dynamo_client.put_item(
        TableName='QuizTable',
        Item={
            'id': {
                'S': uuid.uuid1().hex,
            },
            'category': {
                'S': 'sports'
            },
            'questions': {
                'L': [{'S': 'HELLO WORLD Q'}, {'S': 'Q2'}]
            }
        }
    )

def get_question(id):
    return dynamo_client.query(
        TableName='QuizTable',
        KeyConditionExpression='id = :id',
        ExpressionAttributeValues={
            ':id': {'S': id}
        }
    )