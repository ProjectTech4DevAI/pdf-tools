import logging
from pathlib import Path
from argparse import ArgumentParser

from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.converters.pdf import PdfConverter

if __name__ == '__main__':
    arguments = ArgumentParser()
    arguments.add_argument('--source', type=Path)
    arguments.add_argument('--destination', type=Path)
    args = arguments.parse_args()

    artifact_dict = create_model_dict()
    converter = PdfConverter(artifact_dict=artifact_dict)

    for i in args.source.rglob('*.pdf'):
        dst = (args
               .destination
               .joinpath(i.relative_to(args.source))
               .with_suffix('.md'))
        dst.parent.mkdir(parents=True, exist_ok=True)

        logging.warning('%s -> %s', i, dst)
        (text, *_) = text_from_rendered(converter(str(i)))
        dst.write_text(text)
