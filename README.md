# telegram-xkcd_bot
A telegram chat bot to get you the latest xkcd comic

What is this?
-----------
It is a chat bot. You can go to https://web.telegram.org/#/im?p=@xkcd_bot and start a chat. Whatever you write, it'll reply with latest XKCD comic.

Components
----------
* image_fetch.py: Run this in cron. This will check if a new image is published or not. Note that I am using etcd to store parsed rss feed data. This may seems like an overkill at the moment but idea is to add more features and I think etcd will be handy in that case
* xkcd.py: A simple flask app which listens on 5001 for the incoming webhooks from telegram and send image to anyone pings the bot.

To Do
------
* ~~get random xkcd~~
* get <number> xkcd
