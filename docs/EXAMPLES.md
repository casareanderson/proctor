# proctor — worked examples

## 1. Review the current working-tree changes

```bash
git diff | proctor diff -
```

## 2. Review a saved patch

```bash
git format-patch -1 --stdout > pr.patch
proctor diff pr.patch
```

## 3. Review a GitHub PR

```bash
GITHUB_TOKEN=ghp_... proctor pr casareanderson/sieve#23
```

## 4. In a GitHub Actions PR check

```yaml
name: proctor review
on:
  pull_request:

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: pip install requests
      - name: proctor
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > /tmp/diff.patch
          python3.12 ./proctor diff /tmp/diff.patch
```

`proctor` exits non-zero only when the model is unreachable or the diff can't be read — not on a `changes` verdict —
so the review never fails your build on its own judgement.

## 5. Review every PR on a repo on a timer

```bash
for n in $(gh pr list --json number --jq '.[].number'); do
  gh pr diff "$n" > "/tmp/pr-$n.patch"
  GITHUB_TOKEN=$GH_TOKEN ./proctor pr "owner/repo#$n"
done
```
