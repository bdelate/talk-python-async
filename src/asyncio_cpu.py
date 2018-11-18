####################
# This illustrates that asyncio does not increase performance
# for cpu bound operations. Asyncio is aimed at io bound operations.
####################

# stdlib imports
import json
import math

# 3rd party imports
import mwparserfromhell as parser


async def process_response(api_data: dict) -> None:
    for series, data in api_data.items():
        num_seasons = await parse_response(series=series, response=data)
        print(num_seasons)


async def parse_response(series: str, response: str) -> str:
    json_data = json.loads(response)
    try:
        wiki_text = json_data["parse"]["wikitext"]["*"]
    except KeyError:
        num_seasons = f"- {series} > Does not exist"
    else:
        wiki_code = parser.parse(wiki_text)
        templates = wiki_code.filter_templates()
        num_seasons = await get_num_seasons(series=series, templates=templates)
    return num_seasons


async def get_num_seasons(series: str, templates: list) -> str:
    await use_cpu()
    for template in templates:
        if template.has("num_seasons"):
            num_seasons = str(template.get("num_seasons").value)
            num_seasons = num_seasons[: num_seasons.find("<!--")]
            return f"- {series} > {num_seasons}"
    return f"- {series} > unknown"


async def use_cpu():
    """perform arbitrary calculations to use cpu"""
    pos = 25_000_000
    k_sq = 1000 * 1000
    ave = 0
    while pos < 30_000_000:
        pos += 1
        val = math.sqrt((pos - k_sq) * (pos - k_sq))
        ave += val / 30_000_000
