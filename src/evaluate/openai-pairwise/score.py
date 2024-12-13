import json
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

#
# Using cosine similarity is appropriate:
# https://platform.openai.com/docs/guides/embeddings/how-can-i-retrieve-k-nearest-embedding-vectors-quickly#which-distance-function-should-i-use
#
if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--source', type=Path)
    arguments.add_argument('--target', type=Path)
    args = arguments.parse_args()

    (source, target) = (list(scanf(x)) for x in (args.source, args.target))
    ratio = len(source) / len(target)

    similarity = cosine_similarity(source, target)
    (r, c) = linear_sum_assignment(similarity, maximize=True)
    score = similarity[r, c].mean()

    result = {
        'score': score,
        'st-ratio': ratio,
    }
    print(json.dumps(result, indent=3))
