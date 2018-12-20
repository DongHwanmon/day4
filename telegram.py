import requests
import json
import os

token = os.getenv('TELEGRAM_TOKEN')

url = 'https://api.hphk.io/telegram/bot{}/getUpdates'.format(token)
response = json.loads(requests.get(url).text)
#print(response)

url = 'https://api.hphk.io/telegram/bot{}/sendMessage'.format(token)

'''
[{"update_id":966056929,
"message":{"message_id":1,"from":{"id":778538509,"is_bot":false,
"first_name":"\ub3d9\ud658","last_name":"\uae40"},"chat":{"id":778538509,
"first_name":"\ub3d9\ud658","last_name":"\uae40","type":"private"},"date":1545281636,
"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}},{"update_id":966056930,
'''
chat_id = response["result"][-1]["message"]["from"]["id"]
msg = response["result"][-1]["message"]["text"]


requests.get(url,params = {"chat_id":chat_id,"text":msg})
print(chat_id,msg)