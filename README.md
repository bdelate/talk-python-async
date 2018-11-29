# Presentation given at GPUG

This repo contains the code and slides for a talk that I gave at the Gauteng Python User Group on 28 November 2018.

The slides and demo illustrates various approaches to asynchronous programming in python including:
- Threads
- Multiprocessing
- Asyncio

The demos have purposefully been split into IO and CPU bound sections to illustrate the pros and cons of the above approaches.

## Installation

```
pipenv install
```

## Running the demos

```
pipenv shell
cd src
python sync_main.py
python threads_main.py
python multiprocess_main.py
python asyncio_main.py
```