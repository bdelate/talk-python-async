# stdlib imports
import time

# project imports
import multiprocess_cpu
import multiprocess_io


def main() -> None:
    io_start = time.time()
    api_data = multiprocess_io.get_data()
    print(f"\nDone. IO bound time: {round(time.time() - io_start, 2)}")

    cpu_start = time.time()
    multiprocess_cpu.process_response(api_data=api_data)
    print(f"\nDone. CPU bound time: {round(time.time() - cpu_start, 2)}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nDone. Total time: {round(time.time() - start_time, 2)}")
