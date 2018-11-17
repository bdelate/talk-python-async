# stdlib imports
import json
import time

# 3rd party imports
import mwparserfromhell as parser
import requests

# project imports
import utils


def get_api_data(series: str) -> str:
    url = f"https://en.wikipedia.org/w/api.php?format=json&action=parse&prop=wikitext&page={series}"
    response = requests.get(url)
    return response.text


def do_io() -> dict:
    api_data = {}
    print("\nCalling API for:\n")
    for series in utils.TV_SERIES:
        print(series)
        api_data[series] = get_api_data(series=series)
    return api_data


def do_cpu(api_data: dict) -> None:
    print("\nDoing cpu bound stuff for:\n")
    for series, data in api_data.items():
        num_seasons = utils.process_response(series=series, response=data)
        print(num_seasons)


def main() -> None:
    io_start = time.time()
    api_data = do_io()
    print(f"\nDone. IO bound time: {round(time.time() - io_start, 2)}")

    cpu_start = time.time()
    do_cpu(api_data=api_data)
    print(f"\nDone. CPU bound time: {round(time.time() - cpu_start, 2)}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nDone. Total time: {round(time.time() - start_time, 2)}")
