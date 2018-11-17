# stdlib imports
import json
import math

# 3rd party imports
import mwparserfromhell as parser


TV_SERIES = [
    "Game_of_Thrones",
    "Homeland_(TV_series)",
    "The_Big_Bang_Theory",
    "House_of_Cards_(U.S._TV_series)",
    "Narcos",
    "The_Haunting_of_Hill_House_(TV_series)",
    "Breaking_Bad",
    "Stranger_Things",
    "Westworld_(TV_series)",
    "The_Walking_Dead_(TV_series)",
    "Mr._Robot",
    "Silicon_Valley_(TV_series)",
]


def get_num_seasons(series: str, templates: list) -> str:
    use_cpu()
    for template in templates:
        if template.has("num_seasons"):
            num_seasons = str(template.get("num_seasons").value)
            num_seasons = num_seasons[: num_seasons.find("<!--")]
            return f"- {series} > {num_seasons}"
    return f"- {series} > unknown"


def process_response(series: str, response: str) -> str:
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


def use_cpu():
    """perform arbitrary calculations to use cpu"""
    pos = 25_000_000
    k_sq = 1000 * 1000
    ave = 0
    while pos < 30_000_000:
        pos += 1
        val = math.sqrt((pos - k_sq) * (pos - k_sq))
        ave += val / 30_000_000

