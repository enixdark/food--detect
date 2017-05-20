from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from worker import process_image
import os
app = Flask(__name__)
api = Api(app)

class PathUrl(Resource):

    """
    """

    # use curl -H "Content-Type: application/json" -X POST -d '{"file":"/tmp/hello/world/text.txt"}' http://localhost:5000/path
    def post(self):
        json_data = request.get_json(force=True)
        process_image.delay(json_data['file'], json_data['client_id'])
        return jsonify(json_data['file'])

api.add_resource(PathUrl, '/path', endpoint = 'path')

if __name__ == "__main__":
    app.run(host=os.getenv('SERVER_HOST') or '0.0.0.0', 
            debug=os.getenv('DEBUG')  or False,
            port = 5000) 
