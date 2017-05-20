from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from youtube_search import youtube_search
import os
app = Flask(__name__)
api = Api(app)


class PathUrl(Resource):
    def get(self):
        query = request.args.get('query')
        result = youtube_search(query)
        return jsonify(result)

api.add_resource(PathUrl, '/search', endpoint='search')

if __name__ == "__main__":
    app.run(host=os.getenv('SERVER_HOST') or '0.0.0.0', 
            debug=os.getenv('DEBUG')  or False, 
            port = os.getenv('SERVER_PORT') or  6000)  
