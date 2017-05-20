#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleapiclient.discovery import build
import os
# from pymongo import MongoClient
# client = MongoClient('mongodb://localhost:27017/')
# import time
# db = client.foods
# collection = db.location

def web_search(query):
    service = build("customsearch", "v1",
                    developerKey=os.environ['DEVELOPER_KEY'])
    for i in xrange(1,100):
        try:             
            print "processing " + str(i)
            res = service.cse().list(
                q=query,
                cx=os.environ['SEARCH_ID'],
                start=i
            ).execute()
            time.sleep(5)
            for r in res['items']:
                collection.insert({
                    'url': r['link'],
                    'video_url': None,
                    'localtion': None,
                    'content': r
                }, check_keys=False)
        except Exception as e:
            print e
            return []

if __name__ == '__main__':
    res = web_search("phở")
    print(res)
