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
    with Runner() as runner:
        output_dir = job.dst.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        try:
            runner.run(zerox(
                file_path=str(job.src),
                model=job.model,
                output_dir=str(output_dir),
            ))
            logging.warning(job)
        except Exception as err:
            job.dst.unlink(missing_ok=True)
            logging.error('%s: %s', type(err), job)

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
    arguments.add_argument('--model', default='gpt-4o-mini')
    arguments.add_argument('--source', type=Path)
    arguments.add_argument('--destination', type=Path)
    arguments.add_argument('--overwrite', action='store_true')
    arguments.add_argument('--workers', type=int)
    args = arguments.parse_args()

    with Pool(args.workers) as pool:
        for _ in pool.imap_unordered(func, jobs(args)):
            pass
