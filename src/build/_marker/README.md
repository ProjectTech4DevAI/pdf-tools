# Marker

Use Vik Paruchuri's [marker](https://github.com/VikParuchuri/marker)
library. Point the Python script (`run.py`) at your directory
containing PDFs. It will search the directory, perform the conversion,
and add the file to a destionation with the same relative path:

```bash
$> python run.py \
    --source /path/to/pdfs \
    --destination /path/to/output/directory
```

This should be run on a GPU; Amazon EC2 `g4dn.4xlarge` or
larger. Using a CPU with lots of memory is doable, but takes
significantly more time.

The script processes files sequentially. While this is time consuming,
we have found it is more straightforward and reliable than trying to
tackle parallelization in PyTorch. If parallel processing is required,
consider using the [marker command line
tool](https://github.com/VikParuchuri/marker?tab=readme-ov-file#convert-multiple-files),
or taking inspiration from Vik's [Python
implementation](https://github.com/VikParuchuri/marker/blob/6ded3b9a02c3eba2c7f341b5d07ae1a3b6cfb09f/convert.py#L10).
