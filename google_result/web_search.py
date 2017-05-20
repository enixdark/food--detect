from googleapiclient.discovery import build
import os

def web_search(query):
    service = build("customsearch", "v1",
                    developerKey=os.environ['DEVELOPER_KEY'])

    res = service.cse().list(
        q=query,
        cx=os.environ['SEARCH_ID'],
    ).execute()
    return res['items']

if __name__ == '__main__':
    res = web_search("buncha")
