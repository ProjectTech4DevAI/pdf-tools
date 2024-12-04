import logging
from pathlib import Path
from argparse import ArgumentParser
from multiprocessing import Pool, JoinableQueue

from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.converters.pdf import PdfConverter

def func(queue, args):
    converter = PdfConverter(
        artifact_dict=create_model_dict(),
    )

    while True:
        src = queue.get()
        logging.warning(src)

        (text, *_) = text_from_rendered(converter(src))

        dst = args.destination.joinpath(src.relative_to(args.source))
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text)

        queue.task_done()

if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--source', type=Path)
    arguments.add_argument('--destination', type=Path)
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
        queue.task_done()
