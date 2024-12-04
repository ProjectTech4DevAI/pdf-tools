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

    logging.warning(args.source)

    artifact_dict = create_model_dict()
    converter = PdfConverter(artifact_dict=artifact_dict)
    (text, *_) = text_from_rendered(converter(str(args.source)))

    dst = args.destination.joinpath(args.source.relative_to(args.source))
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)
