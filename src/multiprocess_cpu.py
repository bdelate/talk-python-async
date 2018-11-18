# stdlib imports
import json
import math
import multiprocessing

# 3rd party imports
import mwparserfromhell as parser

# project imports
import config


def process_response(api_data: dict) -> None:
    print("\nDoing cpu bound stuff for:\n")
    pool = multiprocessing.Pool()
    processor_count = multiprocessing.cpu_count()
    group_size = math.ceil((len(config.TV_SERIES) / processor_count))
    tasks = []
    for n in range(0, len(config.TV_SERIES), group_size):
        series_list = config.TV_SERIES[n : n + group_size]
        data = {series: api_data[series] for series in series_list}
        process_num = int(n / 3 + 1)
        task = pool.apply_async(process_task, (data, process_num))
        tasks.append(task)

    pool.close()
    pool.join()
    for t in tasks:
        print(*t.get(), sep="\n")


def process_task(data: dict, process_num: int) -> list:
    results = []
    for series, response in data.items():
        print(f"process {process_num}:\t{series}")
        num_seasons = parse_response(series=series, response=response)
        results.append(num_seasons)
    return results


def parse_response(series: str, response: str) -> str:
    json_data = json.loads(response)
    try:
        wiki_text = json_data["parse"]["wikitext"]["*"]
    except KeyError:
        num_seasons = f"- {series} > Does not exist"
    else:
        wiki_code = parser.parse(wiki_text)
        templates = wiki_code.filter_templates()
        num_seasons = get_num_seasons(series=series, templates=templates)
    return num_seasons


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
