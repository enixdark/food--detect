#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from google_api.web_search import web_search
from google_api.translator import translate

def get_recipe(url, index):
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    # print(soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).get_text()
    if index == 1:
        # buncha
        return (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).get_text()
    elif index == 2:
        # pho
        return (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).find_next_siblings("p")[0].get_text()
    elif index == 3:
        # banhmi
        return (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent.parent).find_next_siblings("ul")[0].get_text()
    else:
        # comrang
        return (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).find_next_siblings("p")[0].get_text()

app = Flask(__name__)
api = Api(app)

class PathUrl(Resource):
    def get(self):
        query = request.args.get('query')
        if query == 'buncha':
            # url = web_search("cach lam bun cha", 0)
            query = get_recipe("http://vaobepnauan.com/cach-lam-bun-cha-gia-truyen-ha-noi-bai-ban-dung-chuan/", 1)
        elif query == 'pho':
            # url = web_search("cach lam pho" + query, 0)
            query = get_recipe("http://vaobepnauan.com/cach-nau-pho-bo-ha-noi-nam-dinh-ngon-theo-cong-thuc-gia-truyen/",
                               2)
        if query == 'banhmi':
            # url = web_search("cach lam banh mi" + query, 0)
            query = get_recipe("http://www.savourydays.com/banh-mi-viet-nam-vo-gion-ruot-xop-p2-cong-thuc-chi-tiet/", 3)
        if query == 'comrang':
            # url = web_search("cach lam com rang", 5)
            query = get_recipe("http://eva.vn/bep-eva/com-rang-thap-cam-ngon-nhu-ngoai-hang-c162a168429.html", 4)
        result = translate(query)
        return jsonify(result)

api.add_resource(PathUrl, '/search', endpoint='search')

if __name__ == "__main__":
    app.run(host=os.getenv('SERVER_HOST') or '0.0.0.0',
            debug=os.getenv('DEBUG') or False,
            port=11000)
