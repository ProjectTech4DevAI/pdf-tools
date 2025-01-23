import logging
from pathlib import Path
from asyncio import Runner
from argparse import ArgumentParser
from dataclasses import dataclass
from multiprocessing import Pool

from pyzerox import zerox

@dataclass(frozen=True)
class Job:
    src: Path
    dst: Path
    model: str

    def __str__(self):
        return f'{self.src} -> {self.dst}'

def func(job):
    logging.warning(job.src)

    with Runner() as runner:
        try:
            result = runner.run(zerox(
                file_path=str(job.src),
                model=job.model,
            ))
        except Exception as err:
            logging.error('%s: %s', type(err), job.dst)
            result = None

    if result is not None:
        logging.critical(job.dst)
        job.dst.parent.mkdir(parents=True, exist_ok=True)
        job.dst.write_text('\n\n'.join(x.content for x in result.pages))

def jobs(args):
    for i in args.source.rglob('*.pdf'):
        source = i.relative_to(args.source)
        dst = (args
               .destination
               .joinpath(source)
               .with_suffix('.md'))
        if not dst.exists() or args.overwrite:
            yield Job(i, dst, args.model)

if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--model', default='gpt-4o')
    arguments.add_argument('--source', type=Path)
    arguments.add_argument('--destination', type=Path)
    arguments.add_argument('--overwrite', action='store_true')
    arguments.add_argument('--workers', type=int)
    args = arguments.parse_args()

    with Pool(args.workers) as pool:
        for _ in pool.imap_unordered(func, jobs(args)):
            pass
