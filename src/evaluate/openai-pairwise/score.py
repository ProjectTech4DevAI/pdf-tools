import json
import functools as ft
from pathlib import Path
from argparse import ArgumentParser

from scipy.optimize import linear_sum_assignment
from sklearn.metrics.pairwise import cosine_similarity

from utils import Paragraph

def scanf(path):
    with path.open() as fp:
        for row in fp:
            para = Paragraph(**json.loads(row))
            yield para.data

class Similarity:
    @ft.cached_property
    def score(self):
        (r, c) = linear_sum_assignment(self.similarity, maximize=True)
        return self.similarity[r, c].mean()

    @ft.cached_property
    def ratio(self):
        (m, n) = self.similarity.shape
        return m / n

    def __init__(self, source, target):
        args = (list(scanf(x)) for x in (source, target))
        self.similarity = cosine_similarity(*args)

#
# Using cosine similarity is appropriate:
# https://platform.openai.com/docs/guides/embeddings/how-can-i-retrieve-k-nearest-embedding-vectors-quickly#which-distance-function-should-i-use
#
if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--source', type=Path)
    arguments.add_argument('--target', type=Path)
    args = arguments.parse_args()

    similarity = Similarity(args.source, args.target)
    result = {
        'score': similarity.score,
        'st-ratio': similarity.ratio,
    }
    print(json.dumps(result, indent=3))
