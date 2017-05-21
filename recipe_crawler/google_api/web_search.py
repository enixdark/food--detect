#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleapiclient.discovery import build
import os, time

def web_search(query,index):
    service = build("customsearch", "v1",
                    developerKey=os.getenv['DEVELOPER_KEY'])
    try:
        res = service.cse().list(
            q=query,
            cx = os.getenv('SEARCH_ID'),
            num=10
        ).execute()
        return res['items'][index]['link']
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    res = web_search("cach lam bun cha",0)
    print(res)
