# stdlib imports
import asyncio
import time

# project imports
import asyncio_cpu
import asyncio_io


if __name__ == "__main__":
    start_time = time.time()
    loop = asyncio.get_event_loop()

    io_start = time.time()
    api_data = loop.run_until_complete(asyncio_io.get_data())
    print(f"\nDone. IO bound time: {round(time.time() - io_start, 2)}\n")

    cpu_start = time.time()
    asyncio.run(asyncio_cpu.process_response(api_data=api_data))
    print(f"\nDone. CPU bound time: {round(time.time() - cpu_start, 2)}")

    print(f"\nTotal time: {round(time.time() - start_time, 2)}")
