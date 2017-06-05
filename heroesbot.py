#!/usr/bin/python
"""Bot that reads through FireEmblemHeroes subreddit and replies to hero mentions
with detailed info about said hero"""
import os
import pdb
import re

import praw

REDDIT = praw.Reddit("bot")
SUBREDDIT = REDDIT.subreddit("FireEmblemHeroes")


def start_bot():
    """Does stuff"""
    for comment in SUBREDDIT.stream.comments():
        for match in re.finditer("<<([^>]*)>>", comment.body):
            query = match.group(1)

            comment.reply()

    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as replied_posts:
            posts_replied_to = replied_posts.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))
