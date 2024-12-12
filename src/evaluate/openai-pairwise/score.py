import math
import json
import itertools as it
import collections as cl
from pathlib import Path
from argparse import ArgumentParser
from dataclasses import dataclass, asdict, astuple

import numpy as np

from utils import Paragraph

@dataclass
class Distance:
    src: str
    dst: str
    distance: float

    def __iter__(self):
        yield from it.islice(astuple(self), 2)

    def __lt__(self, other):
        return self.distance < other.distance

@dataclass
class Result:
    score: float
    confusion: dict

#
#
#
def reader(path):
    with path.open() as fp:
        for row in fp:
            kwargs = json.loads(row)
            yield Paragraph(**kwargs)

def distances(source, target):
    keys = (
        'source',
        'target',
    )

    iterable = map(reader, (source, target))
    for (lhs, rhs) in it.product(*iterable):
        # https://help.openai.com/en/articles/6824809-embeddings-frequently-asked-questions
        dist = np.dot(lhs.data, rhs.data)
        args = (f'{x}-{y}' for (x, y) in zip(keys, (lhs.order, rhs.order)))

        yield Distance(*args, dist)

#
#
#
if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--source', type=Path)
    arguments.add_argument('--target', type=Path)
    args = arguments.parse_args()

    pairs = sorted(distances(args.source, args.target))
    keys = it.chain.from_iterable(map(list, pairs))
    nodes = dict(zip(keys, it.repeat(False)))

    #
    #
    #
    values = []
    for p in pairs:
        if not any(map(nodes.get, p)):
            values.append(p.distance)
            for k in p:
                nodes[k] = True
    score = np.mean(values)

    #
    #
    #
    counts = cl.defaultdict(list)
    for (k, v) in nodes.items():
        key = k[:3]
        counts[key].append(int(v))
    coverage = { x: np.mean(y) for (x, y) in counts.items() }


    #
    #
    #
    result = Result(score, coverage)
    print(json.dumps(asdict(result), indent=3))
