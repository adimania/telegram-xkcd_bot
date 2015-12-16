from flask import Flask, request
import json, ast, requests, os, random
import logging, ConfigParser, os.path, sys

app = Flask(__name__)
app.debug = True
logging.basicConfig(filename='msg.log',level=logging.DEBUG, format='%(asctime)s %(message)s')

check = os.path.isfile(os.path.expanduser('~/.telegram.conf'))
if cmp(check,False) == 0:
  print "~/.telegram.conf is missing"
  sys.exit(2)
config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.telegram.conf'))
api_key = config.get("telegram", "xkcd_bot", raw=True)

images = []
for f in os.walk('images/'):
    images = f[2]

@app.route('/bot/setWebhook', methods=['GET', 'POST'])
def webhook():
    if request.method == "POST":
        incoming = request.get_data()
        logging.info(str(incoming))
        try:
            chat_id = ast.literal_eval(incoming)['message']['chat']['id']
            msg = ast.literal_eval(incoming)['message']['text'].strip().lower()
            url = 'https://api.telegram.org/bot%s/sendPhoto?chat_id=%s' % (api_key,str(chat_id))
            if msg[:7] == '\/xkcd ':
                msg = msg[7:]
            if msg in ['new','latest']:
                data = {'photo': open('images/latest.png', 'rb')}
            elif msg in ['moar', 'more', 'random']:
                data = {'photo': open('images/%s' % random.choice(images), 'rb')}
            elif msg.isdigit():
                try:
                    data = {'photo': open('images/' + msg + '.png', 'rb')}
                except:
                    reply = 'I could not find anything with this number. How about I give you the latest comic? Just type "new".'
                    requests.post('https://api.telegram.org/bot%s/sendMessage?chat_id=%s' % (api_key,str(chat_id)), data={'text':reply})
                    return '{"status":"ok"}'
            else:
                reply = 'Hello! I am XKCD Bot. I can serve you the latest XKCD comic or a random one. What would you like? \nYou can say "new" or "latest" for the latest comic and "more" or "random" for a random comic.\nI can serve comics by numbers as well. Just type in an integer and I will check if I have a corresponding comic.'
                requests.post('https://api.telegram.org/bot%s/sendMessage?chat_id=%s' % (api_key,str(chat_id)), data={'text':reply}) 
                return '{"status":"ok"}'
            r = requests.post(url, files=data)
        except Exception as e:
            print e
        return '{"status":"ok"}'

if __name__ == '__main__':
    app.run(port=5001)
