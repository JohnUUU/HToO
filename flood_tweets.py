import sys
import os
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from IPython.display import clear_output
import matplotlib.pyplot as plt
from sqlalchemy import create_engine




query = "anime"

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
if (not api):
    print ("Can’t Authenticate")
    sys.exit(-1)

tweet_lst=[]
geoc= "35.652832,139.839478,100mi"
for tweet in tweepy.Cursor(api.search_tweets, query).items(100):
    tweetDate = tweet.created_at.date()
    if(tweet.coordinates !=None):
        tweet_lst.append([tweetDate,tweet.id,tweet.
        coordinates['coordinates'][0],
        tweet.coordinates['coordinates'][1],
        tweet.user.screen_name,
        tweet.user.name, tweet.text,
        tweet.user._json['geo_enabled']])
tweet_df = pd.DataFrame(tweet_lst, columns=['tweet_dt', 'id', 'lat','long','username', 'name', 'tweet','geo'])

sql_path = 'sqlite:///' + "flood_tweets.sql"
engine = create_engine(sql_path, echo=False)
tweet_df.to_sql('tweets', engine, if_exists='replace', index=False)




# def search_twitter(query, bearer_token = BEARER_TOKEN, tweet_fields = "tweet.fields=text,author_id,created_at,public_metrics,geo"):
#     headers = {"Authorization": "Bearer {}".format(bearer_token)}

#     # url = "https://api.twitter.com/1.1/geo/search.json?query={}&tweet.fields{}&lat={}&lon={}&start_time={}".format(
#     #     query, tweet_fields,  30.391830, -92.329102, '2019-08-29T12:00:00'
#     # )
#     url = "https://api.twitter.com/2/tweets/search/recent?query={}".format(query)
#     response = requests.request("GET", url, headers=headers)

#     print(response.status_code) # Should be 200 if everything went correctly 

#     if response.status_code != 200:
#         raise Exception(response.status_code, response.text)
#     return response.json()


# print(json.dumps(search_twitter("Hurricane"), indent=4, sort_keys=True))