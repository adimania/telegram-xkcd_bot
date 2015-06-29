import feedparser
from bs4 import BeautifulSoup
import json
import requests
import ast
import shutil
import ConfigParser
import os.path
import sys

check = os.path.isfile(os.path.expanduser('~/.telegram.conf'))
if cmp(check,False) == 0:
  print "~/.telegram.conf is missing"
  sys.exit(2)
config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.telegram.conf'))
etcd_url = config.get("etcd", "url", raw=True)

feed = feedparser.parse("http://xkcd.com/rss.xml")
comic_dict = {}
for comic in feed['entries']:
    comic_img = BeautifulSoup(comic['summary']).img.attrs['src'].split('/')[-1]
    comic_url = comic["links"][0]["href"]
    comic_dict[comic_url] = comic_img

try:
    old_data = json.loads(requests.get(etcd_url + '/xkcd_latest')._content)
    comic_dict_old = ast.literal_eval(old_data['node']['value'])
except:
    comic_dict_old = {}
diff = set(comic_dict.keys()) - set(comic_dict_old.keys())
if diff:
    img = comic_dict[diff.pop()]
    img_url = "http://imgs.xkcd.com/comics/" + img
    response = requests.get(img_url, stream=True)
    with open("images/latest.png", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    requests.put(etcd_url + "/xkcd_latest", data={"value": str(comic_dict)})
