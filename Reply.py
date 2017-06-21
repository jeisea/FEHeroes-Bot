def build_reply(data_list):
    reply_list = []
    for data in data_list["data"]:
        headline = "***\n\n#" + data["type"] + ": " + data_list["query"] + "\n\n" 
        curr_reply = ""
        if data["type"] == "hero":
            curr_reply = hero_reply(data["details"])
        elif data["type"] == "weapon":
            curr_reply = weapon_reply(data["details"])
        elif data["type"] == "special":
            curr_reply = special_reply(data["details"])
        elif data["details"] == "passive":
            curr_reply = passive_reply(data["details"])
        else:
            curr_reply = seal_reply(data["details"])

        reply_list.append(headline+curr_reply)
    total_reply = reply_list.join(createFooter(data_list["query"]) + "\n\n")
    return total_reply

def hero_reply(details):
     bio = "*" + details["bio"] + "*\n\n"
     stats = "5* Stats \n\n"
     table_header = "HP|Atk|Spd|Def|Res\n"
     table_alignment = ":--:|:--:|:--:"
     table_content = details["stats_list"].join("|") + "\n\n\n\n"
     reply = bio + stats + table_header + table_alignment + table_content

def weapon_reply(details):
    table_header = "Might|Rng|\n"

def special_reply(details):
    table_header = 
def createFooter(query):
    return "Link to more info: http://feheroes.gamepedia.com/" + query