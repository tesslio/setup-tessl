# setup-tessl

A GitHub Action to use the [Tessl](https://tessl.io) CLI in your workflows

## Usage

```yaml
- uses: tesslio/setup-tessl@v2
```

### Authentication

1. Create an API token in your workspace settings in the
   [Tessl Web UI](https://tessl.io)
2. Store the token as a
   [repository or organization secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)
   and reference it with `${{ secrets.TESSL_TOKEN }}`.

```yaml
- uses: tesslio/setup-tessl@v2
  with:
    token: ${{ secrets.TESSL_TOKEN }}
```

Once configured, all later steps in the same job can call the Tessl CLI as
authenticated without any extra setup:

```yaml
- run: tessl publish
```

## Examples

### Review a skill on pull request

This runs a quality review of a skill on every pull request. The command fails the
job when the skill has validation errors, such as a malformed `name` or a missing
`description`. Add `--threshold` to fail on the review score as well, so skills
don't degrade over time, or `--threshold 0` to report a score without ever failing
the job.

Reviews run against a Tessl workspace – pass its name or ID with `--workspace`
(`tessl workspace list` shows what your token can see). This command needs Tessl
CLI 0.90.0 or later, which the default `latest` installs.

```yaml
name: Review
on: pull_request

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: tesslio/setup-tessl@v2
        with:
          token: ${{ secrets.TESSL_TOKEN }}
      - run: tessl review run quality --workspace your-workspace path/to/SKILL.md
      # Optionally gate on review score as well
      # - run: tessl review run quality --workspace your-workspace --threshold 80 path/to/SKILL.md
```

> For turn-key PR review that comments scores and required changes, use the
> [`tesslio/skill-review`](https://github.com/tesslio/skill-review) action, which
> wraps this command.

### Publish a plugin on push

```yaml
name: Publish
on:
  push:
    branches: [main]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v6
      - uses: tesslio/setup-tessl@v2
        with:
          token: ${{ secrets.TESSL_TOKEN }}
      - run: tessl plugin publish
```

### Publish multiple plugins

```yaml
name: Publish
on:
  push:
    branches: [main]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    strategy:
      matrix:
        plugin: [plugins/auth, plugins/payments, plugins/notifications]
    defaults:
      run:
        working-directory: ${{ matrix.plugin }}
    steps:
      - uses: actions/checkout@v6
      - uses: tesslio/setup-tessl@v2
        with:
          token: ${{ secrets.TESSL_TOKEN }}
      - run: tessl plugin lint
      - run: tessl plugin publish
```

### Pin a CLI version

```yaml
- uses: tesslio/setup-tessl@v2
  with:
    version: "0.93.0"
    token: ${{ secrets.TESSL_TOKEN }}
```

## Extensions

Community actions that build on top of `setup-tessl`:

| Action                                                                            | Description                                                                                                                                                                                        | How to use                                                                                 |
| --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [tesslio/patch-version-publish](https://github.com/tesslio/patch-version-publish) | Publish plugins with automatic patch version bumping — queries the registry for the latest version, bumps patch, publishes, and commits the updated `.tessl-plugin/plugin.json` back. Respects manual version bumps. | Use instead of `setup-tessl` + `tessl plugin publish`. It includes `setup-tessl` internally. |

## Cleanup

At job completion, the action automatically runs `tessl logout` on a
best-effort basis, clearing on-disk Tessl credentials (such as
`~/.tessl/llm-key.json`) so they do not persist on self-hosted or otherwise
persistent runners. This teardown never fails the job — if the CLI is missing
or there is nothing to clear, it is a harmless no-op.

## License

MIT

## Supported Platforms

| Runner             | Platform           |
| ------------------ | ------------------ |
| `ubuntu-latest`    | `linux-x64`        |
| `ubuntu-24.04-arm` | `linux-arm64`      |
| Alpine-based       | `linux-x64-musl`   |
| Alpine-based ARM   | `linux-arm64-musl` |
| `macos-latest`     | `darwin-arm64`     |
| `macos-13`         | `darwin-x64`       |
