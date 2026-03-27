# setup-tessl

A GitHub Action to install the [Tessl](https://tessl.io) CLI in your workflows. Optionally configure authentication so subsequent steps can run authenticated commands.

## Usage

```yaml
- uses: tesslio/setup-tessl@v1
```

Or pin a specific version:

```yaml
- uses: tesslio/setup-tessl@v1
  with:
    version: "0.73.0"
```

### Authenticated usage

Pass an API token as `token` to make it available as `TESSL_TOKEN` for every subsequent step in the job. Store the token as a [repository or organization secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) and reference it with `${{ secrets.TESSL_TOKEN }}`.

API tokens can be created in your workspace settings.

```yaml
- uses: tesslio/setup-tessl@v1
  with:
    token: ${{ secrets.TESSL_TOKEN }}
```

Once configured, all later steps in the same job can call the Tessl CLI as authenticated without any extra setup:

```yaml
- run: tessl publish
```

## Inputs

| Input     | Required | Default    | Description                                                        |
|-----------|----------|------------|--------------------------------------------------------------------|
| `version` | No       | `"latest"` | Tessl CLI version to install, or `"latest"`                       |
| `token`   | No       | —          | Tessl API token. When set, exported as `TESSL_TOKEN` for all subsequent steps. |

## Outputs

| Output    | Description                            |
|-----------|----------------------------------------|
| `version` | The version of Tessl CLI installed     |
| `path`    | Path to the installed `tessl` binary   |

## Supported Platforms

| Runner            | Platform         |
|-------------------|------------------|
| `ubuntu-latest`   | `linux-x64`      |
| `ubuntu-24.04-arm`| `linux-arm64`    |
| Alpine-based      | `linux-x64-musl`   |
| Alpine-based ARM  | `linux-arm64-musl` |
| `macos-latest`    | `darwin-arm64`   |
| `macos-13`        | `darwin-x64`     |

## Examples

### Code review on pull requests

```yaml
name: Review
on: pull_request

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: tesslio/setup-tessl@v1
        with:
          token: ${{ secrets.TESSL_TOKEN }}
      - run: tessl review
```

### Pin a CLI version

```yaml
- uses: tesslio/setup-tessl@v1
  with:
    version: "0.73.0"
    token: ${{ secrets.TESSL_TOKEN }}
```

## License

MIT
