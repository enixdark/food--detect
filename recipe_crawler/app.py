#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from recipe_crawler.google_api.web_search import web_search
from recipe_crawler.google_api.translator import translate

def get_recipe(url, index):
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    # print(soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).get_text()
    if index == 1:
        # buncha
        result = {}
        result["trans"] = (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).get_text()
        result[
            "img"] = "http://vaobepnauan.com/wp-content/uploads/2014/09/cach-lam-bun-cha-gia-truyen-ha-noi-bai-ban-dung-chuan-12.jpg"
        result["content"] = (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).get_text()
        return result
    elif index == 2:
        # pho
        result = {}
        result["trans"] = (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).find_next_siblings("p")[0].get_text()
        result["img"] = "http://vaobepnauan.com/wp-content/uploads/2014/08/cach-nau-pho-bo-gia-truyen-2.jpg"
        result["content"] = (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).find_next_siblings("p")[
            0].get_text()
        return result
        # return (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).find_next_siblings("p")[0].get_text()
    elif index == 3:
        # banhmi
        result = {}
        result["trans"] = (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent.parent).find_next_siblings("ul")[
            0].get_text()
        result["img"] = "http://www.savourydays.com/wp-content/uploads/2014/10/BanhMiVNPhan2.jpg"
        result["content"] = (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent.parent).find_next_siblings("ul")[
            0].get_text()
        return result
        # return (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent.parent).find_next_siblings("ul")[0].get_text()
    else:
        # comrang
        result = {}
        result["trans"] = (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).find_next_siblings("p")[0].get_text()
        result["img"] = "http://anh.eva.vn/upload/1-2014/images/2014-02-10/1391999972-comrang-thap-cam13.jpg"
        result["content"] = (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).find_next_siblings("p")[
            0].get_text()
        return result
        # return (soup(text=re.compile(r"Nguyên liệu"))[0].parent.parent).find_next_siblings("p")[0].get_text()

app = Flask(__name__)
app.debug = True
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
        query["trans"] = translate(query["trans"])
        result ={}
        result["data"]={}
        result["data"]["translations"] = query["trans"]["data"]["translations"]
        result["data"]["img"] = query["img"]
        result["data"]["content"] = query["content"]
        return jsonify(result)

api.add_resource(PathUrl, '/search', endpoint='search')

if __name__ == "__main__":
    app.run(host=os.getenv('SERVER_HOST') or '0.0.0.0',
            debug=os.getenv('DEBUG') or False,
            port=11000)
