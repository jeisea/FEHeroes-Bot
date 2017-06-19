"""Handles GamePedia requests"""
import requests
from bs4 import BeautifulSoup

def get_category(soup):
    category_div = soup.find("div", "mw-normal-catlinks")
    if category_div:
        category = category_div.find_all("a")[1].get_text().encode('utf-8').strip()
        return category
    else:
        return None

def weapon_handler(soup):
    rows = soup.find("div", "hero-infobox").find_all("tr")
    details = []
    for row in rows:
        detail = row.get_text().encode("utf-8").strip()
        if len(detail) > 0:
            formatted_detail = " ".join(detail.split())
            details.append(formatted_detail)
    return {"details": details, "type": "weapon"}


def special_handler(soup):
    table = soup.find("table", "skills-table").find_all("td")
    details = []
    for data in table:
        detail = data.get_text().encode("utf-8").strip()
        details.append(detail)
    details[4] = details[4].replace("\xc2\xa0", "")
    return {"details": details, "type": "special"}

def hero_handler(soup):
    bio = soup.find("div", "hero-infobox").next_sibling.next_sibling.get_text().encode('utf-8').strip()
    stats_rows = soup.find_all("table", "wikitable")[2].find_all("tr")
    max_stats = stats_rows[len(stats_rows)-1].find_all("td")
    stats_list = []
    for stat in max_stats:
        stats_list.append(stat.get_text().encode("utf-8").strip())
    details = {"bio": bio, "stats_list": stats_list}
    return {"details": details, "type": "hero"}

def passive_handler(soup):
    """Don't know what I want to do for passives yet"""
    rows = soup.find_all("table", "wikitable")[0].find_all("tr")
    details = []
    num_rows = len(rows)
    if num_rows == 2:
        for data in rows[1].find_all("td")[1:]:
            details.append(data.get_text().encode("utf-8").strip())
    else:
        restriction = rows[1].find_all("td")[4].get_text().encode("utf-8").strip().replace("\xc2\xa0", "")
        for data in rows[num_rows-1].find_all("td")[1:]:
            details.append(data.get_text().encode("utf-8").strip())
        details.insert(2, restriction)
    return {"details": details, "type": "passive"}

def seal_handler(soup):
    table = soup.find("table", "skills-table").find_all("td")
    details = []
    for data in table[1:]:
        detail = data.get_text().encode("utf-8").strip()
        details.append(detail)
    return {"details": details, "type": "seal"}

def parse_response(response):
    soup = BeautifulSoup(response.content, "html.parser")
    category = get_category(soup)
    if category == "Heroes":
        return hero_handler(soup)
    elif category == "Weapons":
        return weapon_handler(soup)
    elif category == "Specials":
        return special_handler(soup)
    elif category == "Passives":
        return passive_handler(soup)
    else:
        return seal_handler(soup)

def get_closest_url(gamepedia, query):
    """Finds the closest url when user has incorrect query by requesting the wiki's search service.
    args:
    gamepedia -- the requests session
    query -- user's query
    """
    advanced_search_url = "http://feheroes.gamepedia.com/api.php?action=opensearch&search=" + query
    search_response = gamepedia.get(advanced_search_url, timeout=5)
    res_json = search_response.json()
    for res_item in res_json:
        if type(res_item) is list and res_item[0].startswith("http"):
            return res_item[0]
    return None


def search_gamepedia(query):
    """Searches GamePedia wiki for query in the reddit comment"""
    gamepedia = requests.Session()
    gamepedia.headers.update({"User-Agent": "feheroes-bot"})
    query = query.replace(" ", "%20")
    search_url = "http://feheroes.gamepedia.com/index.php?search=" + query

    try:
        response = gamepedia.get(search_url, timeout=5)
        print response.url
        if response.url == search_url:
            closest_url = get_closest_url(gamepedia, query)
            if closest_url:
                response = gamepedia.get(closest_url, timeout=5)
                print parse_response(response)
            else:
                return None
        else:
            print parse_response(response)
        gamepedia.close()
    except:
        gamepedia.close()
    return


search_gamepedia("Dire thu")
