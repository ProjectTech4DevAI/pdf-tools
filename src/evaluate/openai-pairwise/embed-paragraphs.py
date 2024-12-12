import sys
import json
import logging
import itertools as it
from typing import Union
from argparse import ArgumentParser
from dataclasses import dataclass, asdict, replace
from multiprocessing import Pool, Queue

from openai import OpenAI

#
#
#
@dataclass(frozen=True)
class Paragraph:
    order: int
    data: Union[str, list[float]]

class Blocker(list):
    def flush(self):
        data = ' '.join(it.chain.from_iterable(x.split() for x in self))
        self.clear()
        return data

#
#
#
def func(incoming, outgoing, model):
    client = OpenAI()

    while True:
        paragraph = incoming.get()
        logging.warning(paragraph.order)

        response = client.embeddings.create(
            model=model,
            input=paragraph.data,
        )
        data = response.data[0].embedding
        outgoing.put(replace(paragraph, data=data))

def psplit(fp):
    blocks = Blocker()
    for i in fp:
        line = i.strip()
        if line:
            blocks.append(line)
        else:
            yield blocks.flush()
    if blocks:
        yield blocks.flush()

if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--model', default='text-embedding-3-small')
    arguments.add_argument('--workers', type=int)
    args = arguments.parse_args()

    incoming = Queue()
    outgoing = Queue()
    initargs = (
        outgoing,
        incoming,
        args.model,
    )

    with Pool(args.workers, func, initargs):
        jobs = 0
        for i in enumerate(psplit(sys.stdin)):
            outgoing.put(Paragraph(*i))
            jobs += 1

        for _ in range(jobs):
            result = incoming.get()
            print(json.dumps(asdict(result)))
