from Utils.browser_util import browser_source
from Utils.helper import percentage_difference
from Utils.floor_price_util import floor_prices_dict, collection_names
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from collections import OrderedDict

app = FastAPI(
    title="SharkyFI scraper"
)


@app.get("/get-ltf", tags=["LTF"])
def get_ltf():
    """
    Returns Loan to FloorPrice value and collection name in descending order
    """
    return calculate_lft()


@app.get('/get-collection-ltf', tags=["LTF"])
def get_collection_ltf(name):
    if name in collection_names():
        ltf_dict = calculate_lft()
        if name is not None:
            return ltf_dict[name]
        else:
            return None
    else:
        raise HTTPException(status_code=404, detail="Collection not found.")


def calculate_lft():
    soup = BeautifulSoup(browser_source(), 'html.parser')

    names = []
    prices = []
    for collection_name in soup.find_all('h5'):
        # checking if the collection is seeking borrowers
        if collection_name \
                .findParent("div", class_="contents") \
                .find('span',
                      class_="col-span-2 flex h-full w-full items-center justify-center whitespace-nowrap pl-8 text-2xl") \
                is not None:
            pass
        else:
            names.append(collection_name.text)

    for collection_price in soup.find_all("div", class_="text-3xl font-semibold"):
        prices.append(float(collection_price.text.replace('◎', '')))

    names_and_prices = dict(zip(names, prices))

    ltf = {}
    floor_prices = floor_prices_dict()
    for x in names_and_prices.keys() & floor_prices.keys():
        ltf[x] = round(percentage_difference(names_and_prices[x], floor_prices[x]), 2)
    sorted_dict = [(i, ltf[i]) for i in ltf]
    sorted_dict.sort(key=lambda x: x[1])
    sorted_dict = OrderedDict(sorted_dict)

    return sorted_dict
