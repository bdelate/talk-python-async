# stdlib imports
import asyncio
import json
import math
import multiprocessing
import time

# 3rd party imports
import mwparserfromhell as parser
import aiohttp

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


def process_task(data: dict) -> list:
    results = []
    for series, response in data.items():
        num_seasons = utils.process_response(series=series, response=response)
        results.append(num_seasons)
    return results


def do_cpu(api_data: dict) -> None:
    print("\nDoing cpu bound stuff for:\n")
    pool = multiprocessing.Pool()
    processor_count = multiprocessing.cpu_count()
    group_size = math.ceil((len(utils.TV_SERIES) / processor_count))
    tasks = []
    for n in range(0, len(utils.TV_SERIES), group_size):
        series_list = utils.TV_SERIES[n : n + group_size]
        data = {series: api_data[series] for series in series_list}
        task = pool.apply_async(process_task, (data,))
        tasks.append(task)

    pool.close()
    pool.join()
    for t in tasks:
        print(*t.get(), sep="\n")


async def main() -> None:
    io_start = time.time()
    api_data = await do_io()
    print(f"\nDone. IO bound time: {round(time.time() - io_start, 2)}")

    cpu_start = time.time()
    do_cpu(api_data=api_data)
    print(f"\nDone. CPU bound time: {round(time.time() - cpu_start, 2)}")


if __name__ == "__main__":
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f"\nDone. Total time: {round(time.time() - start_time, 2)}")
