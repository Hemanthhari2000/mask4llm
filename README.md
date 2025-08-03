# mask4llm

A terminal user interface (TUI) tool to safely mask and unmask sensitive data before interacting with large language models (LLMs). Built with Textual, it lets you obfuscate protected fields in your data before sending to an LLM, and then restore the originals after receiving the LLM's response.

## Features

- Mask sensitive info (names, emails, etc.) before sending prompts to LLMs.
- Unmask LLM output swap masked placeholders back after processing.
- Modern TUI built with Textual, with easy navigation.
- Clipboard support via pyperclip.
- Simple installation, cross-platform support.

## Installation

Install via pip (PyPI):

```base
pip install mask4llm
```

Or, if using the uv package manager:

```bash
uv pip install mask4llm
```

Once installed, launch the app with:

```bash
mask4llm
```

## Development Setup

This project is managed with `uv` and uses `Just` for dev tasks. The dev dependencies include basedpyright, ruff, pytest, and pre-commit.

1. Clone the repository and install Just and uv

```bash
git clone https://github.com/hemanthhari2000/mask4llm.git
cd mask4llm
# Install uv and just using your OS/package manager
```

2. Sync the Development Environment

```bash
just install
# or, directly:
uv sync
```

This sets up `.venv` and installs all runtime and [dev] dependencies.

3. Run App in Development

```bash
uv run mask4llm
```

## Common Just Commands

| Command         | Description                                       |
| :-------------- | :------------------------------------------------ |
| just install    | Sync env & install all dependencies               |
| just update     | Upgrade all dependencies                          |
| just lint       | Run Ruff for linting (with autofix)               |
| just format     | Run Ruff for formatting                           |
| just typing     | Type-check with basedpyright                      |
| just test       | Run all tests with pytest                         |
| just pre-commit | Run pre-commit hooks                              |
| just clean      | Complete cleanup (caches, pyc files, venv)        |
| just fresh      | Clean and reinstall all dependencies              |
| just all-dev    | Run lint, format, and type-check (fast dev check) |

## Usage/Examples

- Mask Data:

  - Paste or type sensitive data, run mask, and copy masked output to LLM prompt.

- Unmask Output:
  - Paste LLM output, run unmask, and restore sensitive data.

Details and instructions are shown in the TUI footer and help screens.

## Contributing

Contributions are welcome! Please open issues or PRs as needed. Run all checks before submitting:

```bash
just all-dev && just test
```

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license. See [LICENSE](./LICENSE) file for details.

## Acknowledgements

- [Textual](https://textual.textualize.io/) for the TUI framework.
- [uv](https://docs.astral.sh/uv/), [ruff](https://docs.astral.sh/ruff/), and [basedpyright](https://docs.basedpyright.com/latest/) for the awesome developer tools.
