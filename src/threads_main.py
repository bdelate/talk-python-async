# stdlib imports
import time
import queue

# project imports
import threads_cpu
import threads_io


def main() -> None:
    q = queue.Queue()
    io_start = time.time()
    threads_io.get_data(q=q)
    print(f"\nDone. IO bound time: {round(time.time() - io_start, 2)}")

    cpu_start = time.time()
    threads_cpu.process_response(q=q)
    print(f"\nDone. CPU bound time: {round(time.time() - cpu_start, 2)}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nTotal time: {round(time.time() - start_time, 2)}")
