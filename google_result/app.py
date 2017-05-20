from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from google_result.youtube_search import youtube_search

app = Flask(__name__)
api = Api(app)

class PathUrl(Resource):
    def get(self):
        query = request.args.get('query')
        result = youtube_search(query)
        return jsonify(result)

api.add_resource(PathUrl, '/search', endpoint='search')

if __name__ == "__main__":
    app.run(debug=True)
