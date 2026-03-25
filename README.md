# setup-tessl

A GitHub Action to install the [Tessl](https://tessl.io) CLI in your workflows.

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

## Inputs

| Input     | Required | Default    | Description                                    |
|-----------|----------|------------|------------------------------------------------|
| `version` | No       | `"latest"` | Tessl CLI version to install, or `"latest"`   |

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

## Example

```yaml
name: Review
on: pull_request

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: tesslio/setup-tessl@v1
      - run: tessl review
```

## License

MIT
