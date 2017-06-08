import requests
from data import heroes

def search_gamepress(query):
    """Searches Gamepress if spelled incorrectly, otherwise retrieve hero data from gamepress"""
    if heroes.has_key(query):
        gamepress = requests.Session()
        gamepress.headers.update({"User-Agent": "feheroes-bot"})
        query_status = True
        url = heroes[query][1]
        try:
            response = gamepress.get(url, timeout=5)
            gamepress.close()
        except:
            gamepress.close()
        data = [query_status, url]
    else:
        query_status = False
        url = "https://fireemblem.gamepress.gg/search?q=" + query
        try:
            response.url = gamepress.get(url, timeout=5)
            gamepress.close()
        except:
            gamepress.close()
        data = [query_status, url]
    return ""
    