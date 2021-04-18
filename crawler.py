# Reference: https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/master/Recent-Search/recent_search.py
# Changed by Dayue Bai <dayuebai@gmail.com>
# Date: 04/11/2021

import sys
import requests
import os
import json
import argparse

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url(keywords):
    # Documentation: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    query = f"{keywords} -is:retweet -has:media -has:images -has:videos -has:links -is:reply lang:en"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=id,created_at,author_id,text,public_metrics"
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&{tweet_fields}&max_results=100"
    return url


def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print("HTTP response status code: {}".format(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():

    if len(sys.argv) == 1:
        print("Please enter keywords that you want to search. Try again!")
        return

    keywords = " ".join(sys.argv[1:])
    bearer_token = auth()
    url = create_url(keywords)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)

    with open("blockbuster.json", "w") as output:
    	output.write(json.dumps(json_response, indent=4, sort_keys=True))
    	output.write("\n")


if __name__ == "__main__":
    main()
