from flask import Flask, jsonify, request
import requests
import db_file
import json
# creating a Flask app
app = Flask(__name__)
import re


api_key = 'f0a21ce96b36999b1552ff2cce97def8'

@app.route('/movie/popular', methods=['GET'])
def popular():
    r = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=' + api_key + '&language=hi-IN&page=1')
    result = []
    for temp in r.json()['results']:
            result.append(temp['title'])
    return jsonify(result)
# driver function


@app.route('/movie/search', methods=['GET'])
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


@app.route('/get/watchlist/<string:user_id>', methods=['GET'])
def get_watch_list(user_id):
    result = db_file.get_watch_list(user_id)
    print(result)
    return jsonify(result)


@app.route('/add/watchlist', methods=['POST'])
def add_watch_list():
    request_data = request.get_json()
    user_id = str(request_data['user_id'])
    movie_id = str(request_data['movie_id'])
    movie_name = str(request_data['movie_name'])
    rating = str(request_data['rating'])
    db_file.add_watch_list(user_id, movie_id, movie_name, rating)
    return jsonify('Movie Added to WatchList')


@app.route('/delete/watchlist', methods=['POST'])
def delete_watch_list():
    request_data = request.get_json()
    user_id = str(request_data['user_id'])
    movie_id = str(request_data['movie_id'])
    db_file.delete_watch_list(user_id, movie_id)
    return jsonify('Movie Deleted from WatchList')


if __name__ == '__main__':
    app.run(debug=True)
