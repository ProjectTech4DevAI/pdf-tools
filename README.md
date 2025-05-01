# PDF-tools

This repository contains tools for managing PDF-to-Markdown
conversion. It focuses on two phases: conversion and evaluation of the
conversion. For now, evaluation is experimental lives in separate
branches; see the relevant PRs for more information.

# Setup

Ensure you have a proper Python environment. If you do not have the
packages required in your default environment, consider creating a
virtual one:

```bash
$> python -m venv venv
$> source venv/bin/activate
$> pip install -r requirements.txt
```

# PDF-to-Markdown Conversion

There are currently two methods support for conversion: Xerox and
Marker. Either can be run using the same interface:

```bash
$> python src/[converter]/run.py \
    --source /path/to/pdfs \
    --destination /path/to/output/directory
```

where _[converter]_ is the directory in `src` corresponding to the
conversion method you want to undertake.

The directory passed to `source` should be the top-level directory
containing your PDF documents; `destination` is where you want them to
go. Documents will be created in destination using the file name
relative to its location in source. As an example, the following file:

```
/path/to/pdfs/A/B/C/d.pdf
```

would be writting to:

```
/path/to/output/directory/A/B/C/d.pdf
```

By default, if the destination file exists, conversion will not be
attempted. Use `--overwrite` to bypass this feature.

While each conversion method follows the same command line interface,
each has additional nuances that are worth noting. For more
information, see the README's in the `src/build` subdirectories
corresponding to each conversion method.
