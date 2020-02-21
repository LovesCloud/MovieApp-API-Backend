import awsgi
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import os
import boto3
import logging
import json
import db_file
import requests

api_key = 'f0a21ce96b36999b1552ff2cce97def8'

application = Flask(__name__)
application.config["DEBUG"] = True
cors = CORS(application)
logging.getLogger('flask_cors').level = logging.DEBUG


logger = logging.getLogger()
logger.setLevel(int(10))

def lambda_handler(event, context):
    logger.info(event)
    # logger.info(request)
    return awsgi.response(application, event, context)

def lambda_handler_sample(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }


@application.route('/movie/popular', methods=['GET'])
def popular():
    r = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=' + api_key + '&language=hi-IN&page=1')
    print(r)
    result = []
    for temp in r.json()['results']:
            result.append(temp['title'])
    return jsonify(r.json())
# driver function


@application.route('/movie/search', methods=['GET'])
def movie_search():
    name = request.args.get('name')
    movie = Movie()
    result = []
    search = movie.search(name)
    for res in search:
        temp = {'id': res.id,
                'title': res.title,
                'overview': res.overview,
                'rating': res.vote_average}
        result.append(temp)

    return jsonify(result)


@application.route('/movie/watchlist/<string:user_id>', methods=['GET'])
def get_watch_list(user_id):
    result = db_file.get_watch_list(user_id)
    print(result)
    return jsonify(result)


@application.route('/movie/add/watchlist', methods=['POST'])
def add_watch_list():
    request_data = request.get_json()
    user_id = str(request_data['user_id'])
    movie_id = str(request_data['movie_id'])
    movie_name = str(request_data['movie_name'])
    rating = str(request_data['rating'])
    db_file.add_watch_list(user_id, movie_id, movie_name, rating)
    return jsonify(message='Movie Added to WatchList')


@application.route('/movie/delete/watchlist', methods=['POST'])
def delete_watch_list():
    request_data = request.get_json()
    user_id = str(request_data['user_id'])
    movie_id = str(request_data['movie_id'])
    db_file.delete_watch_list(user_id, movie_id)
    return jsonify(message='Movie Deleted from WatchList')


if __name__ == '__main__':
    application.run(debug=True)
