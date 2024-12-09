# Marker

Use Vik Paruchuri's [marker](https://github.com/VikParuchuri/marker)
library. The Python script (`run.py`) is meant to be run sequentially:

```bash
$> source /path/to/venv/bin/activate
$> find /path/to/pdfs -name '*.pdf' \
    | while read; do
    python run.py \
	   --source "$REPLY" \
	   --destination /path/to/output/directory
done
```

This takes a while, but it is more straightforward than trying to
tackle parallelization in PyTorch. If parallel processing is required,
consider using the [marker command line tool](https://github.com/VikParuchuri/marker?tab=readme-ov-file#convert-multiple-files), or taking inspiration
from Vik's [Python implementation](https://github.com/VikParuchuri/marker/blob/6ded3b9a02c3eba2c7f341b5d07ae1a3b6cfb09f/convert.py#L10).