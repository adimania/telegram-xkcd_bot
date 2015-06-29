from flask import Flask, request
import json, ast, requests
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

@app.route('/bot/setWebhook', methods=['GET', 'POST'])
def webhook():
    if request.method == "POST":
        incoming = request.get_data()
        logging.info(incoming)
        chat_id = ast.literal_eval(incoming)['message']['chat']['id']
        url = 'https://api.telegram.org/bot%s/sendPhoto?chat_id=%s' % (api_key,str(chat_id))
        data = {'photo': open('images/latest.png', 'rb')} #, 'chat_id':chat_id}
        r = requests.post(url, files=data)
    return '{"status":"ok"}'

if __name__ == '__main__':
    app.run(port=5001)
