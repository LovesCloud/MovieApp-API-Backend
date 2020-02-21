import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('watch_list')


def get_watch_list(user_id):
    response = table.scan(
                FilterExpression=Attr('user_id').eq(user_id)
            )
    items = response['Items']
    print(items)
    return items


def add_watch_list(user_id, movie_id, movie_name, rating):
    table.put_item(
        Item={
            'user_id': user_id,
            'movie_id': movie_id,
            'movie_name': movie_name,
            'rating': rating
        }
    )


def delete_watch_list(user_id, movie_id):
    table.delete_item(
        Key={
            'user_id': user_id,
            'movie_id': movie_id
        }
    )
#print(table.creation_date_time)