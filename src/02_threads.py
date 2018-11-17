# stdlib imports
import json
import time
from threading import Thread
import queue


# 3rd party imports
import mwparserfromhell as parser
import requests

# project imports
import utils


def get_api_data(series: str, q: queue.Queue) -> None:
    url = f"https://en.wikipedia.org/w/api.php?format=json&action=parse&prop=wikitext&page={series}"
    response = requests.get(url)
    q.put((series, response.text))


def do_io(q: queue.Queue) -> None:
    threads = []
    print("\nCalling API for:\n")
    for series in utils.TV_SERIES:
        print(series)
        threads.append(Thread(target=get_api_data, args=(series, q), daemon=True))
    [t.start() for t in threads]
    [t.join() for t in threads]


def do_cpu(q: queue.Queue) -> None:
    print("\nDoing cpu bound stuff for:\n")
    while not q.empty():
        item = q.get()
        num_seasons = utils.process_response(series=item[0], response=item[1])
        print(num_seasons)


def main() -> None:
    q = queue.Queue()
    io_start = time.time()
    do_io(q=q)
    print(f"\nDone. IO bound time: {round(time.time() - io_start, 2)}")

    cpu_start = time.time()
    do_cpu(q=q)
    print(f"\nDone. CPU bound time: {round(time.time() - cpu_start, 2)}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nTotal time: {round(time.time() - start_time, 2)}")
