# CI templates

Workflow files staged here instead of `.github/workflows/` because the initial
push was made with a GitHub token that lacked the `workflow` scope. To enable
GitHub Actions CI:

## Option A — via gh CLI (one command)

```bash
gh auth refresh --hostname github.com --scopes workflow
git mv docs/ci-templates/github-actions-validate.yml.template .github/workflows/validate.yml
git commit -m "Enable GitHub Actions CI"
git push
```

## Option B — via GitHub web UI

1. Open `https://github.com/ali-saadat/llms-txt-ops/new/main/.github/workflows`
2. Filename: `validate.yml`
3. Paste contents of `docs/ci-templates/github-actions-validate.yml.template`
4. Commit directly to `main`

The workflow runs `check.py + sync.py + pytest + cookbook dry-run + JSON/YAML
parse` on every push and PR.
