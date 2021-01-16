import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr
import random 

dynamo_client = boto3.client('dynamodb')


def get_items(category=None):
    # return dynamo_client.scan(TableName='QuizTable')
    questions = None
    print(category)
    if category: 
        questions = dynamo_client.scan(
            TableName='QuizTable',
            FilterExpression='category = :cat',
            ExpressionAttributeValues={
                ":cat": {
                    "S": category
                }
            }
        )
    else:
        questions = dynamo_client.scan(
            TableName='QuizTable',
        )

    nums = random.sample(range(1, len(questions)), 10)
    result = [questions[x] for x in nums]
    return result



def create_quiz_question(question, incorrect_answers, correct_answer, category):
    if type(question) is not str:
        raise ValueError()

    if type(incorrect_answers) is not list:
        raise ValueError()

    if type(correct_answer) is not str:
        raise ValueError()

    if len(incorrect_answers) != 3:
        raise ValueError("Must provide 4 answers")

    return dynamo_client.put_item(
        TableName='QuizTable',
        Item={
            'id': {
                'S': uuid.uuid1().hex,
            },
            'category': {
                'S': category,
            },
            'question': {
                'S': question,
            },
            'incorrect_answers': {
                'L': [{'S': answer} for answer in incorrect_answers]
            },
            'correct_answer': {
                'S': correct_answer,
            },
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

# format with Shift + Option + F
def batch_create_questions(questions):
    put_requests = [
        {
            'PutRequest': {
                'Item': {
                    'id': {
                        'S': uuid.uuid1().hex,
                    },
                    'category': {
                        'S': q['category']
                    },
                    'question': {
                        'S': q['question']
                    },
                    'correct_answer': {
                        'S': q['correct_answer']
                    },
                    'incorrect_answers': {
                        'L': [{'S': answer} for answer in q['incorrect_answers']]
                    }
                }
            }
        } for q in questions
    ]


    dynamo_client.batch_write_item(
        RequestItems={
            'QuizTable': put_requests
        }
    )
