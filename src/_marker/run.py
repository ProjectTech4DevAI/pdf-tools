from pathlib import Path
from argparse import ArgumentParser

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

def func(queue, args):
    while True:
        src = queue.get()
        logging.warning(src)

        converter = PdfConverter(
            artifact_dict=create_model_dict(),
        )
        rendered = converter(src)
        (text, *_) = text_from_rendered(rendered)

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
