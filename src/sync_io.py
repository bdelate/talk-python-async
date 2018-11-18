# 3rd party imports
import requests

# project imports
import config


def api(series: str) -> str:
    url = f"https://en.wikipedia.org/w/api.php?format=json&action=parse&prop=wikitext&page={series}"
    response = requests.get(url)
    return response.text


def get_data() -> dict:
    api_data = {}
    print("\nCalling API for:\n")
    for series in config.TV_SERIES:
        print(series)
        api_data[series] = api(series=series)
    return api_data
