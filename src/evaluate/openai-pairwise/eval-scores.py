import sys
import json
import logging
from pathlib import Path
from argparse import ArgumentParser

import pandas as pd

class PathManager:
    _keys = (
        'source',
        'target',
    )

    def __init__(self, root):
        self.root = root

    def __call__(self, data):
        for i in self._keys:
            p = Path(data[i])
            yield p.relative_to(self.root)

def scanf(fp, pathman):
    for row in fp:
        data = json.loads(row)
        (src, dst) = pathman(data)

        result = { x: data[x] for x in ('score', 'st-ratio') }
        result.update({
            'model': src.parents[-2], # index may vary!
            'document': dst,
        })

        yield result

if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--root', type=Path)
    args = arguments.parse_args()

    manager = PathManager(args.root)
    df = pd.DataFrame.from_records(scanf(sys.stdin, manager))
    df.to_csv(sys.stdout, index=False)
