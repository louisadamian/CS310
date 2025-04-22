import requests
import json
def location_search(query:str):
    query.replace(' ', '+')
    headers = {"User-Agent": "CS310-Navigation"}
    res = requests.get(f"https://nominatim.openstreetmap.org/search.php?q={query}&viewbox=-71.06081%2C42.32107%2C-71.03228%2C42.31029&bounded=1&format=jsonv2", headers=headers)
    return res.json()[0]["osm_id"], res.json()[0]

if __name__ == '__main__':
    osm_id, res= location_search("university hall")
    print(osm_id)