#!/usr/bin/python
import os
import pprint
from oauth2client.tools import argparser
from googleapiclient.discovery import build

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = os.getenv('DEVELOPER_KEY') or 'AIzaSyCkhoUH3QL7nQMa5vh44ivqzKvWjecmq1M'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q="cach lam " + query,
        part="id,snippet",
        maxResults=10
    ).execute()
    pprint.pprint(search_response.get("items", []))
    return search_response.get("items", [])

if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

    try:
        youtube_search(args.q)
    except Exception as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
