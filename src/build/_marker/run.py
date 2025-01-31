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
    arguments.add_argument('--overwrite', action='store_true')
    args = arguments.parse_args()

    artifact_dict = create_model_dict()
    converter = PdfConverter(artifact_dict=artifact_dict)

    for i in args.source.rglob('*.pdf'):
        source = i.relative_to(args.source)
        destination = (args
                       .destination
                       .joinpath(source)
                       .with_suffix('.md'))
        if destination.exists() and not args.overwrite:
            logging.error('%s exists (skipping)', source)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)

        logging.warning('%s -> %s', i, destination)
        (text, *_) = text_from_rendered(converter(str(i)))
        destination.write_text(text)
