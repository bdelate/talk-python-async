# stdlib imports
import json
import time

# 3rd party imports
import mwparserfromhell as parser
import requests


tv_series = [
    'Game_of_Thrones',
    'Homeland_(TV_series)',
    'The_Big_Bang_Theory',
    'House_of_Cards_(U.S._TV_series)',
    'Narcos',
    'The_Haunting_of_Hill_House_(TV_series)',
    'Black_Mirror',
    'Stranger_Things',
    'Westworld_(TV_series)',
    'The_Walking_Dead_(TV_series)',
]


def get_api_data(series: str) -> str:
    url = f'https://en.wikipedia.org/w/api.php?format=json&action=parse&prop=wikitext&page={series}'
    response = requests.get(url)
    return response.text


def process_response(series: str, response: str) -> None:
    json_data = json.loads(response)
    try:
        wiki_text = json_data['parse']['wikitext']['*']
    except KeyError:
        print(f'- {series} > Does not exist')
    else:
        wiki_code = parser.parse(wiki_text)
        templates = wiki_code.filter_templates()
        output_num_seasons(series=series, templates=templates)


def output_num_seasons(series: str, templates: list) -> None:
    for template in templates:
        if template.has('num_seasons'):
            num_seasons = str(template.get('num_seasons').value)
            num_seasons = num_seasons[: num_seasons.find('<!--')]
            print(f'- {series} > {num_seasons}')


def main() -> None:
    io_time, cpu_time = 0.0, 0.0
    total_time_start = time.time()
    for series in tv_series:
        io_start = time.time()
        response = get_api_data(series=series)
        io_time += time.time() - io_start
        cpu_start = time.time()
        process_response(series=series, response=response)
        cpu_time += time.time() - cpu_start
    print(f'\nCPU time: {round(cpu_time, 2)}')
    print(f'IO time: {round(io_time, 2)}')
    print(f'Total time: {round(time.time() - total_time_start, 2)}')


if __name__ == '__main__':
    main()
