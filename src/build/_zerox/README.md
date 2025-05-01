# Zerox

Zerox relies on third-party LLMs to handle conversions. Therefore, it
is necessary to have your own credentials for those services. Prior
executing the run script, it is important to configure your
environment to facilitate authentication. For OpenAI:

```
$> OPENAI_API_KEY=... python src/build/_zerox/run.py
```

By default, GPT-4o is used. This can be changed using the `--model`
option.
