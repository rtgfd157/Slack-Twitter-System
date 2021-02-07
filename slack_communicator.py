
import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv


#env-path = Path('.') 
#load_dotenv(dotenv_path= env-path )

load_dotenv()

#slack_token = 'xoxb-my-bot-token'
slack_token = os.environ['SLACK_TOKEN']
slack_channel = '#content'
slack_icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuGqps7ZafuzUsViFGIremEL2a3NR0KO0s0RTCMXmzmREJd5m4MA&s'
slack_user_name = 'Double Images Monitor'

content_channel_token=os.environ['CONTENT_CHANNEL_TOKEN']


def post_message_to_slack(text, blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_url': slack_icon_url,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()	

def get_all_messages_from_slack():
    return requests.get('https://slack.com/api/conversations.history',{
        'token': slack_token,
        'channel': content_channel_token,
    }).json()	

r = get_all_messages_from_slack()

#print(r['messages'])

messages =r['messages']

# messages =r['messages']
# print(messages)

for m in messages:
    print(m['text'])

# print (r.content)
# print (r.status_code)
# print (r.headers)
# print (r.json)
#https://slack.com/api/channels.history

#slack_info = 'There are 1111111111'

#post_message_to_slack(slack_info)	