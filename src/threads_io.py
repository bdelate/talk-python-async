# stdlib imports
from threading import Thread
import queue

# 3rd party imports
import requests

# project imports
import config


def get_data(q: queue.Queue) -> None:
    threads = []
    print("\nCalling API for:\n")
    for series in config.TV_SERIES:
        print(series)
        threads.append(Thread(target=api, args=(series, q), daemon=True))
    [t.start() for t in threads]
    [t.join() for t in threads]


def api(series: str, q: queue.Queue) -> None:
    url = f"https://en.wikipedia.org/w/api.php?format=json&action=parse&prop=wikitext&page={series}"
    response = requests.get(url)
    q.put((series, response.text))
