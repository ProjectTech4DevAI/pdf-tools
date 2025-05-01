# Document comparison using OpenAI embeddings

These scripts use embeddings from OpenAI to do document
comparison. Documents are first parsed into paragraphs, where a
paragraph is text separated by two new lines. For example, in Python:

```python
with open(...) as fp:
     fp.read().split('\n\n')
```

The whitespace in each chunk is then replaced with a single space, and
that string fed to an OpenAI embedding model.

Two documents are compared by aligning their respective embeddings
based on cosine similarity. Embeddings in a "source" document are
uniquely paired with an embedding in a "target" document based on
highest similarity. The mean of these best-matches is called the
_score_. The number embeddings that are matched is captured in
_coverage_.

## Running a comparison

### Environment

1. Ensure your OpenAI key is in the environment

   ```bash
   $> export OPENAI_API_KEY=...
   ```

2. Ensure you have a proper Python environment. If you do not have the
   packages required in your default environment, consider creating a
   virtual one:

   ```bash
   $> python -m venv venv
   $> source venv/bin/activate
   $> pip install -r requirements.txt
   ```

### Generated embeddings

Assume there are two Markdown files to compare, a source `PR.md` and a
target `GT.md`. First generated embeddings for each:

```bash
$> for i in PR GT; do python embed-paragraphs.py < $i.md > $i.jsonl; done
```

### Score embeddings

Using those JSONLs:

```bash
$> python score.py --source PR.jsonl --target GT.jsonl
```
