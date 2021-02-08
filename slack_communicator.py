
import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import sys


load_dotenv()

slack_token = os.environ['SLACK_TOKEN']
slack_channel = '#content'
slack_icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuGqps7ZafuzUsViFGIremEL2a3NR0KO0s0RTCMXmzmREJd5m4MA&s'
slack_user_name = 'Double Images Monitor'
content_channel_token=os.environ['CONTENT_CHANNEL_TOKEN']


def send(text, blocks = None):
    """
        send text to slack channel
    """
    try:
        return requests.post('https://slack.com/api/chat.postMessage', {
            'token': slack_token,
            'channel': slack_channel,
            'text': text,
            'icon_url': slack_icon_url,
            'username': slack_user_name,
            'blocks': json.dumps(blocks) if blocks else None
        }).json()
    except:
        print("Oops! method send\n", sys.exc_info()[0], "occurred.")
    	

def get_all_channel_messages_from_slack():
    """
        get latest 500 messages
    """
    try:
        return requests.get('https://slack.com/api/conversations.history',{
            'token': slack_token,
            'channel': content_channel_token,
            'limit':500
        }).json()
    except:
        print("Oops! method get_all_channel_messages_from_slack\n", sys.exc_info()[0], "occurred.")
        	

def post_message_to_slack(message):
    """
        post message to slack if there isnt identical in last 500 channel messages
    """
    messages = get_all_channel_messages_from_slack()
    try:
        is_get_ok=messages.get("ok", False)
        if is_get_ok:
            messages_list = messages.get("messages", None)
            for dic in messages_list:
                if dic.get("text", None) == message:
                    print(f' message: {message}, found same message in latest 500 ')
                    return -1
            print("sent")    
            send(message)
        else:
            print("get_all_channel_messages_from_slack call didnt succeed")
    except:
        print("Oops! method post_message_to_slack\n", sys.exc_info()[0], "occurred.")

