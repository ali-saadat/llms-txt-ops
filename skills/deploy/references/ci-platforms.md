# CI/CD Platform Integrations

*Wire `templates/validate.sh` into the user's CI/CD pipeline. Load when the user's CI platform needs platform-specific syntax.*

## GitHub Actions

Create `.github/workflows/validate-llms-txt.yml`:

```yaml
name: Validate llms.txt

on:
  pull_request:
    paths:
      - 'llms.txt'
      - 'llms-full.txt'
      - 'static/llms.txt'
      - 'public/llms.txt'
  push:
    branches: [main]
    paths:
      - 'llms.txt'
      - 'llms-full.txt'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y xxd file
          pip install llms-txt  # optional spec-shape parser

      - name: Validate llms.txt
        run: |
          chmod +x ./templates/validate.sh
          ./templates/validate.sh ./llms.txt $EXPECTED_HASH
        env:
          EXPECTED_HASH: ${{ vars.LLMS_TXT_SHA256 }}

      - name: Validate llms-full.txt (if present)
        if: hashFiles('llms-full.txt') != ''
        run: ./templates/validate.sh ./llms-full.txt
```

For post-deploy hash verification, add a second job:

```yaml
  verify-deployed:
    needs: [validate]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Wait for deployment
        run: sleep 30  # adjust based on your deploy time

      - name: Verify deployed file matches source
        run: |
          LOCAL_HASH=$(shasum -a 256 llms.txt | awk '{print $1}')
          LIVE_HASH=$(curl -s https://${{ vars.SITE_DOMAIN }}/llms.txt | shasum -a 256 | awk '{print $1}')
          if [ "$LOCAL_HASH" != "$LIVE_HASH" ]; then
            echo "::error::Deployed file differs from source"
            echo "Local:  $LOCAL_HASH"
            echo "Live:   $LIVE_HASH"
            exit 1
          fi
          echo "✓ Deployed file matches source: $LOCAL_HASH"

      - name: Verify headers
        run: |
          curl -I https://${{ vars.SITE_DOMAIN }}/llms.txt | tee headers.txt
          grep -q "charset=utf-8" headers.txt || (echo "::error::Missing charset=utf-8"; exit 1)
          grep -qi "x-robots-tag.*noindex" headers.txt || (echo "::warning::Missing X-Robots-Tag: noindex")
```

## GitLab CI

In `.gitlab-ci.yml`:

```yaml
stages:
  - validate
  - deploy
  - verify

validate_llms_txt:
  stage: validate
  image: ubuntu:24.04
  before_script:
    - apt-get update && apt-get install -y curl xxd file python3 python3-pip
    - pip3 install llms-txt
  script:
    - chmod +x ./templates/validate.sh
    - ./templates/validate.sh ./llms.txt $LLMS_TXT_SHA256
  rules:
    - changes:
        - llms.txt
        - llms-full.txt
        - static/llms.txt

verify_deployed:
  stage: verify
  image: ubuntu:24.04
  dependencies:
    - validate_llms_txt
  script:
    - sleep 30
    - LOCAL_HASH=$(sha256sum llms.txt | awk '{print $1}')
    - LIVE_HASH=$(curl -s https://${SITE_DOMAIN}/llms.txt | sha256sum | awk '{print $1}')
    - |
      if [ "$LOCAL_HASH" != "$LIVE_HASH" ]; then
        echo "Deployed file differs from source"
        exit 1
      fi
  only:
    - main
```

## CircleCI

In `.circleci/config.yml`:

```yaml
version: 2.1

jobs:
  validate-llms-txt:
    docker:
      - image: cimg/base:2024.10
    steps:
      - checkout
      - run:
          name: Install deps
          command: |
            sudo apt-get update
            sudo apt-get install -y xxd file
            pip3 install llms-txt
      - run:
          name: Validate
          command: |
            chmod +x ./templates/validate.sh
            ./templates/validate.sh ./llms.txt $LLMS_TXT_SHA256

workflows:
  llms-txt-validation:
    jobs:
      - validate-llms-txt:
          filters:
            branches:
              only:
                - main
```

## Bitbucket Pipelines

In `bitbucket-pipelines.yml`:

```yaml
pipelines:
  default:
    - step:
        name: Validate llms.txt
        image: ubuntu:24.04
        script:
          - apt-get update && apt-get install -y curl xxd file python3 python3-pip
          - pip3 install llms-txt
          - chmod +x ./templates/validate.sh
          - ./templates/validate.sh ./llms.txt $LLMS_TXT_SHA256
```

## Jenkins

In `Jenkinsfile`:

```groovy
pipeline {
    agent any

    stages {
        stage('Validate llms.txt') {
            steps {
                sh '''
                    chmod +x ./templates/validate.sh
                    ./templates/validate.sh ./llms.txt ${LLMS_TXT_SHA256}
                '''
            }
        }

        stage('Verify deployed') {
            when { branch 'main' }
            steps {
                sh '''
                    sleep 30
                    LOCAL_HASH=$(sha256sum llms.txt | awk '{print $1}')
                    LIVE_HASH=$(curl -s https://${SITE_DOMAIN}/llms.txt | sha256sum | awk '{print $1}')
                    [ "$LOCAL_HASH" = "$LIVE_HASH" ] || exit 1
                '''
            }
        }
    }
}
```

## Pre-commit hook (local, not CI)

In `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-llms-txt
        name: Validate llms.txt
        entry: ./templates/validate.sh
        files: '(llms\.txt|llms-full\.txt)$'
        language: system
        pass_filenames: true
```

Install via `pre-commit install`.

## Configuration variables to set per platform

Each CI platform needs these secrets/variables:

| Variable | Purpose | Source |
|---|---|---|
| `LLMS_TXT_SHA256` | Pinned source hash (manual) | Set after a known-good commit |
| `SITE_DOMAIN` | Production domain for post-deploy hash check | Your domain |
| `CF_API_TOKEN` (if Cloudflare) | For purge after deploy | Cloudflare dashboard |
| `CF_ZONE_ID` (if Cloudflare) | Zone for purge | Cloudflare dashboard |
| `FASTLY_API_KEY` (if Fastly) | For purge | Fastly dashboard |
| `CLOUDFRONT_DIST_ID` (if AWS) | For invalidation | AWS console |

## CDN purge in CI (post-deploy)

GitHub Actions example with Cloudflare:

```yaml
  purge-cdn:
    needs: [deploy]
    runs-on: ubuntu-latest
    steps:
      - name: Purge Cloudflare cache
        run: |
          curl -X POST "https://api.cloudflare.com/client/v4/zones/${{ secrets.CF_ZONE_ID }}/purge_cache" \
            -H "Authorization: Bearer ${{ secrets.CF_API_TOKEN }}" \
            -H "Content-Type: application/json" \
            --data '{"files":["https://${{ vars.SITE_DOMAIN }}/llms.txt","https://${{ vars.SITE_DOMAIN }}/llms-full.txt"]}'
```

## Cross-references

- `../SKILL.md` — main deployment flow
- `../../../templates/validate.sh` — the validation script being wired in
- `platform-configs.md` — server-side configuration
