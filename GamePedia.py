"""Handles GamePedia requests"""
import requests
from data import heroes
def search_gamepedia(query):
    """Searches GamePedia wiki for query in the reddit comment"""
    gamepedia = requests.Session()
    gamepedia.headers.update({"User-Agent": "feheroes-bot"})
    if heroes.has_key(query):
        query_status = True
        url = heroes[query][0]
        try:
            response = gamepedia.get(url, timeout=5)
            gamepedia.close()
        except:
            gamepedia.close()
        data = [query_status, url]
    else:
        query_status = False
        url = "https://feheroes.gamepedia.com/index.php?search=" + query
        try:
            response.url = gamepedia.get(url, timeout=5)
            gamepedia.close()
        except:
            gamepedia.close()
        data = [query_status, url]
    return ""