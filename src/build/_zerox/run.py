import os
import asyncio
import logging
from pathlib import Path
from argparse import ArgumentParser
from multiprocessing import Pool, JoinableQueue

from pyzerox import zerox

def func(queue, args):
    while True:
        src = queue.get()

        source = src.relative_to(args.source)
        destination = (args
                       .destination
                       .joinpath(source)
                       .with_suffix('.md'))
        if destination.exists() and not args.overwrite:
            logging.error('%s exists (skipping)', source)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            logging.warning('%s -> %s', source, destination)
            asyncio.run(zerox(
                file_path=str(src),
                model=args.model,
                output_dir=str(destination.parent),
            ))

        queue.task_done()

if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--model', default='gpt-4o-mini')
    arguments.add_argument('--source', type=Path)
    arguments.add_argument('--destination', type=Path)
    arguments.add_argument('--overwrite', action='store_true')
    arguments.add_argument('--workers', type=int)
    args = arguments.parse_args()

    queue = JoinableQueue()
    initargs = (
        queue,
        args,
    )

    with Pool(args.workers, func, initargs):
        for i in args.source.rglob('*.pdf'):
            queue.put(i)
        queue.join()
