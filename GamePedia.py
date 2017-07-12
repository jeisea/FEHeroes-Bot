"""Handles GamePedia requests"""
import requests
from bs4 import BeautifulSoup

def get_category(soup):
    """Find category at bottom of page to know which comment handler to use"""
    category_div = soup.find("div", "mw-normal-catlinks")
    if category_div:
        category = category_div.find_all("a")[1].get_text().encode('utf-8').strip()
        return category
    else:
        return None

def hero_handler(soup):
    """Get Hero bio and stats of min/max level at 5 star rating"""
    bio = soup.find("div", "hero-infobox").next_sibling.next_sibling.get_text().encode('utf-8').strip()
    min_stats_rows = soup.find_all("table", "wikitable")[1].find_all("tr")
    max_stats_rows = soup.find_all("table", "wikitable")[2].find_all("tr")
    min_stats = min_stats_rows[len(min_stats_rows)-1].find_all("td")
    max_stats = max_stats_rows[len(max_stats_rows)-1].find_all("td")
    stats_list = []
    stats_list.append("1")
    for stat in min_stats[1:]:
        stats_list.append(stat.get_text().encode("utf-8").strip())
    stats_list.append("40")
    for stat in max_stats[1:]:
        stats_list.append(stat.get_text().encode("utf-8").strip())
    details = {"bio": bio, "stats_list": stats_list}
    return {"details": details, "type": "Hero"}

def weapon_handler(soup):
    """Get weapon details from box"""
    rows = soup.find("div", "hero-infobox").find_all("tr")
    details = []
    for i, row in enumerate(rows[2:]):
        detail = row.get_text().encode("utf-8").strip()
        if i == 5: #Special Effect
            details.append(detail)
        elif i == 2: #SP Cost
            details.append(detail.split()[2])
        else:
            details.append(detail.split()[1])
    return {"details": details, "type": "Weapon"}

def special_handler(soup):
    """Get special details from first table"""
    table = soup.find("table", "skills-table").find_all("td")
    details = []
    for data in table:
        detail = data.get_text().encode("utf-8").strip()
        details.append(detail)
    details[4] = details[4].replace("\xc2\xa0", "")
    return {"details": details, "type": "Special"}

def passive_handler(soup):
    """Get passive details from wiki table"""
    rows = soup.find_all("table", "wikitable")[0].find_all("tr")
    details = []
    num_rows = len(rows)
    # if only 1 detail row (2 because +1 for header), then get everything
    # else get restriction and skill type from first row and then get rest of details
    # for highest level of the skill
    if num_rows == 2:
        for data in rows[1].find_all("td")[1:]:
            details.append(data.get_text().encode("utf-8").strip())
    else:
        restriction = rows[1].find_all("td")[4].get_text().encode("utf-8").strip().replace("\xc2\xa0", "")
        skill_type = rows[1].find_all("td")[5].get_text().encode("utf-8").strip()
        for data in rows[num_rows-1].find_all("td")[1:]:
            details.append(data.get_text().strip())
        details.append(restriction)
        details.append(skill_type)
    return {"details": details, "type": "Passive"}

def seal_handler(soup):
    """Get seal details from skills table"""
    table = soup.find("table", "skills-table").find_all("td")
    details = []
    for data in table[1:]:
        detail = data.get_text().encode("utf-8").strip()
        details.append(detail)
    return {"details": details, "type": "Seal"}

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
        if response.url == search_url:
            closest_url = get_closest_url(gamepedia, query)
            if closest_url:
                response = gamepedia.get(closest_url, timeout=5)
                return [parse_response(response), closest_url]
            else:
                return None
        else:
            return [parse_response(response), response.url]
        gamepedia.close()
    except:
        gamepedia.close()
    return
