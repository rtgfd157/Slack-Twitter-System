import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import sys
import tweepy
from datetime import datetime, timedelta
import slack_communicator


load_dotenv()

access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#userID_list = ["Python Weekly",'Real Python', 'Full Stack Python','tttbayex']

userID_list = ["PythonWeekly",'realpython', 'fullstackpython','tttbayex']



def get_last_hour_user_tweet(user):
    # time 3 because server of twiiter
    # twitter server is lag 2 hours
    # time delta - 3
    try:
        last_hour_date_time = datetime.now() - timedelta(hours = 3)
        
        t=last_hour_date_time.strftime('%Y-%m-%d-%H-%M')
        print(f'trying to fetch {user}')
        tweets = api.user_timeline(screen_name=user, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended',
                            since=t
                            )
        for tweet in tweets:
            if tweet.created_at > last_hour_date_time:
                slack_communicator.post_message_to_slack(tweet.full_text)
    except:
        print("Oops! method get_last_hour_user_tweet\n", sys.exc_info()[0], "occurred.")


def check_users_new_tweets():
    for user in userID_list:
        get_last_hour_user_tweet(user)
        
  

def make_tweet(message):
    try:
        api.update_status(message)
    except:
        print("Oops! method make_tweet\n", sys.exc_info()[0], "occurred.")