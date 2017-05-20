from flask import Flask, request, 

from flask_restful import Resource, Api
import os
import unirest

app = Flask(__name__)
api = Api(app)

API_KEY = os.getenv('API_KEY') or 'QwGbA9i9eZmshcmQpoc3Dlqys4Oyp1cjb02jsnqiEQS1V3F1l9'
CONTEXT_TYPE = "application/x-www-form-urlencoded"
ACCEPT_TYPE = "application/json"
ACCEPT_TYPE_TEXT = "text/html"
DETECH_URI = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/detect"
VISUAL_URI = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/visualizeIngredients"

HEADERS = {
  "X-Mashape-Key": API_KEY,
  "Content-Type": CONTEXT_TYPE,
}

def detect_text(text):
  try:
    response = unirest.post(DETECH_URI, 
    headers=dict(HEADERS, **{ 'Accept': ACCEPT_TYPE}),
    params={
      "text": text
    })
    import ipdb; ipdb.set_trace()
    if response.code == 200:
      return response.body
  except:
    pass
  return []


def visual(text):
  try:
    response = unirest.post(VISUAL_URI,
    headers=dict(HEADERS, **{ 'Accept': ACCEPT_TYPE_TEXT}), 
    params={
      "defaultCss": True,
      "ingredientList": text,
      "measure": "metric",
      "servings": 2,
      "showBacklink": True,
      "view": "grid"
    })
    import ipdb;ipdb.set_trace()
    if response.code == 200:
      return jsonify({'canvas': response.body})
  except:
    pass
  return []
    

class DetectUrl(Resource):
    def post(self):
        json_data = request.get_json(force=True)      
        return detect_text(json_data['text'])

class VisualText(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        return visual(json_data['text'])

api.add_resource(DetectUrl, '/detect', endpoint = 'detect')
api.add_resource(VisualText, '/visual', endpoint = 'visual')

if __name__ == "__main__":
    app.run(host=os.getenv('SERVER_HOST') or '0.0.0.0', 
            debug=os.getenv('DEBUG')  or True, 
            port = 10000)  
