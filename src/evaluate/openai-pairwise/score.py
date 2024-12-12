import math
import json
import itertools as it
import statistics as st
import collections as cl
from pathlib import Path
from argparse import ArgumentParser
from dataclasses import dataclass, asdict, astuple

from scipy import spatial

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

def distances(source, target, delimiter='-'):
    keys = (
        'source',
        'target',
    )

    iterable = map(reader, (source, target))
    for (lhs, rhs) in it.product(*iterable):
        # https://platform.openai.com/docs/guides/embeddings/how-can-i-retrieve-k-nearest-embedding-vectors-quickly#which-distance-function-should-i-use
        dist = 1 - spatial.distance.cosine(lhs.data, rhs.data)

        values = (
            lhs.order,
            rhs.order,
        )
        args = (f'{x}{delimiter}{y}' for (x, y) in zip(keys, values))
        yield Distance(*args, dist)

#
#
#
if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--source', type=Path)
    arguments.add_argument('--target', type=Path)
    args = arguments.parse_args()

    _delimiter = '-'

    values = distances(args.source, args.target, _delimiter)
    pairs = sorted(values, reverse=True)
    keys = it.chain.from_iterable(map(list, pairs))
    nodes = dict(zip(keys, it.repeat(True)))

    #
    #
    #
    values = []
    for p in pairs:
        if all(map(nodes.get, p)):
            values.append(p.distance)
            for k in p:
                nodes[k] = False
    score = st.fmean(values)

    #
    #
    #
    counts = cl.defaultdict(list)
    for (k, v) in nodes.items():
        (key, _) = k.split(_delimiter, maxsplit=1)
        counts[key].append(1 - v) # since unseen is True
    coverage = { x: st.fmean(y) for (x, y) in counts.items() }


    #
    #
    #
    result = Result(score, coverage)
    print(json.dumps(asdict(result), indent=3))
