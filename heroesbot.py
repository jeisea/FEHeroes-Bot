#!/usr/bin/python
"""Bot that reads through FireEmblemHeroes subreddit and replies to hero mentions
with detailed info about said hero"""
import re
import os
import praw
import GamePedia
import Reply
import traceback

REDDIT = praw.Reddit(client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    password=os.environ["REDDIT_PASSWORD"],
    username=os.environ["REDDIT_USERNAME"],
    user_agent="feheroes-bot for reddit")
SUBREDDIT = REDDIT.subreddit("FireEmblemHeroes")

def run_bot():
    """Try to reply to comments that query bot
     Excepts in place for reddit rate limits"""
    data_list = []
    try:
        for comment in SUBREDDIT.stream.comments():
            for match in re.finditer("<([^>]*)>", comment.body):
                query = match.group(1)
                gamepedia_data = GamePedia.search_gamepedia(query)
                if gamepedia_data:
                    data_list.append({"data": gamepedia_data[0], "url": gamepedia_data[1], "query": gamepedia_data[2]})
            if len(data_list) > 0:
                try:
                    comment.reply(Reply.build_reply(data_list))
                    del data_list[:]
                except:
                    traceback.print_exc()
                    print "waiting"
                    del data_list[:]
    except:
        traceback.print_exc()
        print "Bot exiting"
run_bot()
