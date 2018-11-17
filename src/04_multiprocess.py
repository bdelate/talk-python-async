# stdlib imports
import json
import math
import multiprocessing
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


def process_task(data: dict) -> list:
    results = []
    for series, response in data.items():
        num_seasons = utils.process_response(series=series, response=response)
        results.append(num_seasons)
    return results


def do_io() -> dict:
    api_data = {}
    print("\nCalling API for:\n")
    for series in utils.TV_SERIES:
        print(series)
        api_data[series] = get_api_data(series=series)
    return api_data


def do_cpu(api_data: dict) -> None:
    print("\nDoing cpu bound stuff for:\n")
    pool = multiprocessing.Pool()
    processor_count = multiprocessing.cpu_count()
    group_size = math.ceil((len(utils.TV_SERIES) / processor_count))
    tasks = []
    for n in range(0, len(utils.TV_SERIES), group_size):
        series_list = utils.TV_SERIES[n : n + group_size]
        data = {series: api_data[series] for series in series_list}
        task = pool.apply_async(process_task, (data,))
        tasks.append(task)

    pool.close()
    pool.join()
    for t in tasks:
        print(*t.get(), sep="\n")


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
