#!/usr/bin/python
"""Bot that reads through FireEmblemHeroes subreddit and replies to hero mentions
with detailed info about said hero"""
import os
import pdb
import re
import praw
import GamePedia
import Reply

REDDIT = praw.Reddit("bot")
SUBREDDIT = REDDIT.subreddit("FireEmblemHeroes")

def start_bot():
    """Does stuff"""
    all_data = []
    for comment in SUBREDDIT.stream.comments():
        for match in re.finditer("<<([^>]*)>>", comment.body):
            query = match.group(1)
            gamepedia_data = GamePedia.search_gamepedia(query)
            if gamepedia_data:
                all_data.append(gamepedia_data)
        if (len(all_data) > 0):
            comment.reply(Reply.build_reply(all_data))
            del all_data[:]

def build_reply(query):
    reply = "Here is more information about " + query
    return reply
