"""Build reply for each query type"""

def build_reply(data_list):
    reply_list = []
    for query_item in data_list:
        gamepedia_data = query_item["data"]
        query = query_item["query"]
        headline = "#" + gamepedia_data["type"] + ": " + query + " \n\n"
        curr_reply = ""
        if gamepedia_data["type"] == "Hero":
            curr_reply = hero_reply(gamepedia_data["details"], query)
        elif gamepedia_data["type"] == "Weapon":
            curr_reply = weapon_reply(gamepedia_data["details"])
        elif gamepedia_data["type"] == "Special":
            curr_reply = special_reply(gamepedia_data["details"])
        elif gamepedia_data["type"] == "Passive":
            curr_reply = passive_reply(gamepedia_data["details"])
        elif gamepedia_data["type"] == "Assist":
            curr_reply = assist_reply(gamepedia_data["details"])
        else:
            curr_reply = seal_reply(gamepedia_data["details"])
        reply_list.append(headline+curr_reply.decode('utf-8'))
        reply_list.append(createFooter(query_item["url"]) + "\n\n***")
    total_reply = "\n\n".join(reply_list)
    return total_reply

def hero_reply(details, hero):
    stats_list = details["stats_list"]
    bio = "*" + details["bio"] + "*\n\n 5 Star Rarity \n\n"
    table_header = "Level|HP|Atk|Spd|Def|Res|Total\n"
    table_alignment = ":--:|:--:|:--:|:--:|:--:|:--:|:--:\n"
    table_content = "|".join(stats_list[0:7]) + "\n" + "|".join(stats_list[7:]) + "\n\n\n\n"
    reply = bio + table_header + table_alignment + table_content
    return reply

def assist_reply(details):
    effect = "**" + details[2] + "**\n\n"
    del details[2]
    table_header = "Name|Range|SP Cost|Exclusive\n"
    table_alignment = ":--:|:--:|:--:|:--:\n"
    table_content = "|".join(details[0:4]) + "\n\n\n\n"
    reply = effect + table_header + table_alignment + table_content + "\n\n\n\n"
    return reply

def weapon_reply(details):
    special_effect = "**" + ": ".join(details[4:]) + "**\n\n"
    table_header = "Might|Range|SP Cost|Exclusive\n"
    table_alignment = ":--:|:--:|:--:|:--:\n"
    table_content = "|".join(details[0:4]) + "\n\n\n\n"
    reply = special_effect + table_header + table_alignment + table_content + "\n\n\n\n"
    return reply

def special_reply(details):
    effect = "**" + details[2] + "**\n\n"
    table_header = "Cooldown|SP Cost|Inherit Restriction\n"
    table_alignment = ":--:|:--:|:--:\n"
    table_content = details[1] + "|" + details[3] + "|" + details[4] + "\n\n\n\n"
    reply = effect + table_header + table_alignment + table_content
    return reply

def passive_reply(details):
    effect = "**" + details[2] + "**\n\n"
    del details[2]
    table_header = "Name|SP Cost\n"
    table_alignment = ":--:|:--:\n"
    table_content = "|".join(details) + "\n\n\n\n"
    reply = effect + table_header + table_alignment + table_content
    return reply

def seal_reply(details):
    effect = "**" + details[1] + "**\n\n"
    reply = effect
    return reply

def createFooter(url):
    return "Find more info at " + url
