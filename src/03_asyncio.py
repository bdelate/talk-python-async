# stdlib imports
import asyncio
import json
import time

# 3rd party imports
import aiohttp
import mwparserfromhell as parser

# project imports
import utils


async def get_api_data(series: str) -> str:
    url = f"https://en.wikipedia.org/w/api.php?format=json&action=parse&prop=wikitext&page={series}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


async def do_io() -> dict:
    tasks = {}
    for series in utils.TV_SERIES:
        tasks[series] = asyncio.create_task(get_api_data(series=series))

    api_data = {}
    print("\nCalling API for:\n")
    for series, task in tasks.items():
        print(series)
        api_data[series] = await task
    return api_data


def do_cpu(api_data: dict) -> None:
    for series, data in api_data.items():
        num_seasons = utils.process_response(series=series, response=data)
        print(num_seasons)


async def main() -> None:
    io_start = time.time()
    api_data = await do_io()
    print(f"\nDone. IO bound time: {round(time.time() - io_start, 2)}\n")

    cpu_start = time.time()
    do_cpu(api_data=api_data)
    print(f"\nDone. CPU bound time: {round(time.time() - cpu_start, 2)}")


if __name__ == "__main__":
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f"\nTotal time: {round(time.time() - start_time, 2)}")
