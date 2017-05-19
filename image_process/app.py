from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class PathUrl(Resource):

    """
    """

    # use curl -H "Content-Type: application/json" -X POST -d '{"file":"/tmp/hello/world/text.txt"}' http://localhost:5000/path
    def post(self):
        json_data = request.get_json(force=True)
        return jsonify(json_data['file'])

api.add_resource(PathUrl, '/path', endpoint = 'path')

if __name__ == "__main__":
    app.run(debug=True)
