# proctor — setup

## Endpoint

`proctor` talks to any OpenAI-compatible `/chat/completions` endpoint. The default is OpenRouter:

```bash
export OPENROUTER_API_KEY=sk-or-...
```

To use a local Ollama instead:

```bash
export MENTOR_URL=http://192.0.2.50:11434/v1
export MENTOR_API_KEY=ollama
export MENTOR_MODEL=qwen3:8b
```

## Model

```bash
export MENTOR_MODEL=qwen/qwen3.7-flash   # default; any OpenAI-compatible model works
```

The review is a single ~2k-token call, so a small/free model is fine. A reasoning-capable model works too — proctor
strips any `<think>` block before parsing.

## GitHub (only for `proctor pr`)

`proctor pr` reads the PR title + diff over the public GitHub API. A `GITHUB_TOKEN` (read-only `public_repo` scope is
enough) lifts the unauthenticated rate limit:

```bash
export GITHUB_TOKEN=ghp_...
```

## Where findings come from

`review.py` holds the system prompt and the diff fact-check. The verdict → GitHub review event mapping lives in
`VERDICT_EVENT` (`approve` → `APPROVE`, `comment` → `COMMENT`, `changes` → `REQUEST_CHANGES`) if you wire it into your
own bot; the CLI itself only prints.
