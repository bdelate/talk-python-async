# stdlib imports
import asyncio

# 3rd party imports
import aiohttp

# project imports
import config


async def api(series: str) -> str:
    url = f"https://en.wikipedia.org/w/api.php?format=json&action=parse&prop=wikitext&page={series}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


async def get_data() -> dict:
    tasks = {}
    for series in config.TV_SERIES:
        tasks[series] = asyncio.create_task(api(series=series))

    api_data = {}
    print("\nCalling API for:\n")
    for series, task in tasks.items():
        print(series)
        api_data[series] = await task
    return api_data
