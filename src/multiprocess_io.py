# stdlib imports
import math
import multiprocessing

# 3rd party imports
import requests

# project imports
import config


def api(series_list: list, process_num: int) -> dict:
    api_data = {}
    for series in series_list:
        print(f"process {process_num}:\t{series}")
        url = f"https://en.wikipedia.org/w/api.php?format=json&action=parse&prop=wikitext&page={series}"
        response = requests.get(url)
        api_data[series] = response.text
    return api_data


def get_data() -> dict:
    print("\nCalling API for:\n")
    api_data = {}
    pool = multiprocessing.Pool()
    processor_count = multiprocessing.cpu_count()
    group_size = math.ceil((len(config.TV_SERIES) / processor_count))
    tasks = []
    for n in range(0, len(config.TV_SERIES), group_size):
        series_list = config.TV_SERIES[n : n + group_size]
        process_num = int((n / (processor_count - 1)) + 1)
        task = pool.apply_async(api, (series_list, process_num))
        tasks.append(task)

    pool.close()
    pool.join()
    for t in tasks:
        api_data.update(t.get())
    return api_data
