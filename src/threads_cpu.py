####################
# This illustrates that threads do not increase performance
# for cpu bound operations. Threads are suited to io bound operations.
####################

# stdlib imports
import json
import math
import queue
from threading import Thread, Lock

# 3rd party imports
import mwparserfromhell as parser


print_lock = Lock()


def process_response(q: queue.Queue) -> None:
    threads = []
    print("\nDoing cpu bound stuff for:\n")
    while not q.empty():
        item = q.get()
        threads.append(
            Thread(target=parse_response, args=(item[0], item[1]), daemon=True)
        )
    [t.start() for t in threads]
    [t.join() for t in threads]


def parse_response(series: str, response: str) -> None:
    json_data = json.loads(response)
    try:
        wiki_text = json_data["parse"]["wikitext"]["*"]
    except KeyError:
        num_seasons = f"- {series} > Does not exist"
    else:
        wiki_code = parser.parse(wiki_text)
        templates = wiki_code.filter_templates()
        num_seasons = get_num_seasons(series=series, templates=templates)

    with print_lock:
        print(num_seasons)


def get_num_seasons(series: str, templates: list) -> str:
    use_cpu()
    for template in templates:
        if template.has("num_seasons"):
            num_seasons = str(template.get("num_seasons").value)
            num_seasons = num_seasons[: num_seasons.find("<!--")]
            return f"- {series} > {num_seasons}"
    return f"- {series} > unknown"


def use_cpu():
    """perform arbitrary calculations to use cpu"""
    pos = 25_000_000
    k_sq = 1000 * 1000
    ave = 0
    while pos < 30_000_000:
        pos += 1
        val = math.sqrt((pos - k_sq) * (pos - k_sq))
        ave += val / 30_000_000
