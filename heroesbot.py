#!/usr/bin/python
"""Bot that reads through FireEmblemHeroes subreddit and replies to hero mentions
with detailed info about said hero"""
import os
import pdb
import re
import praw
import GamePedia
import Reply
import traceback

REDDIT = praw.Reddit("bot")
SUBREDDIT = REDDIT.subreddit("jackytestsub")

def start_bot():
    """Begin streaming comments from SUBREDDIT"""
    data_list = []
    try:
        for comment in SUBREDDIT.stream.comments():
            for match in re.finditer("<([^>]*)>", comment.body):
                query = match.group(1)
                gamepedia_data = GamePedia.search_gamepedia(query)
                if gamepedia_data:
                    data_list.append({"data": gamepedia_data[0], "url": gamepedia_data[1]})
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
start_bot()
