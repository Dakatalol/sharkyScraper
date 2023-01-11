import requests
from Utils.helper import get_nested


def floor_prices_dict():
    req = requests.get('https://sharky.fi/api/floor-prices')
    floor_prices = req.json()
    collections_and_floor_prices = floor_prices['floorPrices']
    floors = {}
    for collection in collections_and_floor_prices:
        name = get_nested(collections_and_floor_prices, collection, "name")
        floor_price = get_nested(collections_and_floor_prices, collection, "floorPriceSol")
        floors[name] = floor_price
    return floors


def collection_names():
    req = requests.get('https://sharky.fi/api/floor-prices')
    floor_prices = req.json()
    collections_and_floor_prices = floor_prices['floorPrices']
    names = []
    for collection in collections_and_floor_prices:
        names.append(get_nested(collections_and_floor_prices, collection, "name"))
    return names
