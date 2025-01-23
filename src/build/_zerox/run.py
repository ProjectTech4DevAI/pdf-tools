import logging
import functools as ft
from pathlib import Path
from asyncio import Runner
from argparse import ArgumentParser
from dataclasses import dataclass
from multiprocessing import Pool

from pyzerox import zerox

#
#
#
@dataclass(frozen=True)
class Job:
    src: Path
    dst: Path
    model: str

    def __str__(self):
        return f'{self.src} -> {self.dst}'

#
#
#
@ft.singledispatch
def extract(source, model):
    raise TypeError(type(source))

@extract.register
def _(file_path: str, model):
    with Runner() as runner:
        result = runner.run(zerox(
            file_path=file_path,
            model=model,
        ))
    output = '\n\n'.join(x.content for x in result.pages)
    if not output:
        raise ValueError('Empty output')

    return output

@extract.register
def _(file_path: Path, model):
    return extract(str(file_path), model)

#
#
#
def func(job):
    logging.warning(job.src)
    try:
        result = extract(job.src, job.model)
    except Exception as err:
        logging.error('%s: %s', type(err), job.dst)
        return

    logging.critical(job.dst)
    job.dst.parent.mkdir(parents=True, exist_ok=True)
    job.dst.write_text(result)

def jobs(args):
    for i in args.source.rglob('*.pdf'):
        source = i.relative_to(args.source)
        dst = (args
               .destination
               .joinpath(source)
               .with_suffix('.md'))
        if not dst.exists() or args.overwrite:
            yield Job(i, dst, args.model)

#
#
#
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
