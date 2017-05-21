from flask import Flask, request, jsonify

from flask_restful import Resource, Api
import os
import unirest
import requests
import json
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

RECIPE_END_POINT = os.getenv('RECIPE_END_POINT') or 'http://0.0.0.0:11000/search'

def detect_text(text):
  try:
    response = unirest.post(DETECH_URI, 
    headers=dict(HEADERS, **{ 'Accept': ACCEPT_TYPE}),
    params={
      "text": text
    })
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
    if response.code == 200:
      return jsonify({'canvas': response.body})
  except:
    pass
  return []

def request_recipe(text):
    response = requests.get(RECIPE_END_POINT, params = {"query": text})
    if response.ok:
        return response.content
    return ""
    

class DetectUrl(Resource):
    def post(self):
        json_data = request.get_json(force=True)      
        return detect_text(json_data['text'])

class VisualText(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        return visual(json_data['text'])

class SearchApi(Resource):
    def get(self):
        query = request.args.get('query')
        if query:
            text = request_recipe(query)
            if text:
                response = detect_text(json.loads(text)['data']['translations'][0]['translatedText'])
                nutrition = visual( map(lambda x: x['annotation'],response['annotations']))
                return dict(dict(response,**json.loads(text)), **json.loads(nutrition.data))
        print('not response')
        return ""
# map(lambda x: x['annotation'],response['annotations'])
api.add_resource(DetectUrl, '/detect', endpoint = 'detect')
api.add_resource(VisualText, '/visual', endpoint = 'visual')
api.add_resource(SearchApi, '/search', endpoint = 'search')

if __name__ == "__main__":
    app.run(host=os.getenv('SERVER_HOST') or '0.0.0.0', 
            debug=os.getenv('DEBUG')  or False, 
            port = 10000)  
