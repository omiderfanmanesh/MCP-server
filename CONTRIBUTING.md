# Contributing to Books MCP Server

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/omiderfanmanesh/MCP-server/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/omiderfanmanesh/MCP-server/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports. I'm not even kidding.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/omiderfanmanesh/MCP-server.git
   cd MCP-server
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests** (when available)
   ```bash
   python -m pytest
   ```

4. **Test the server**
   ```bash
   python -m mcp_server.server
   ```

## Code Style

* Follow PEP 8 for Python code
* Use meaningful variable and function names
* Add docstrings to functions and classes
* Keep functions small and focused
* Add type hints where appropriate

## Adding New Features

1. **Discuss first**: For major changes, please open an issue first to discuss what you would like to change.

2. **Follow the existing patterns**: Look at how current tools are implemented and follow similar patterns.

3. **Update documentation**: Add or update relevant documentation in the `docs/` directory.

4. **Test your changes**: Ensure your feature works with common MCP clients like Cursor and Claude Desktop.

## Project Structure Guidelines

When adding new files or modifying the structure:

- Keep the main server logic in `mcp_server/server.py`
- Add new data sources as separate modules (like `books.py`, `exchange.py`)
- Put utility functions in `mcp_server/util/`
- Add documentation to `docs/`
- Include examples in `examples/`

## Testing Guidelines

- Test with real MCP clients when possible
- Verify Docker builds work: `docker build -t books-mcp-server .`
- Test both successful operations and error cases
- Ensure configuration examples work

## Documentation Guidelines

- Update README.md for user-facing changes
- Update API.md for tool changes
- Add examples to EXAMPLES.md for new features
- Keep documentation clear and beginner-friendly

## Commit Message Guidelines

- Use clear and meaningful commit messages
- Start with a verb in the present tense ("Add", "Fix", "Update")
- Reference issues when applicable: "Fix #123: Handle missing data files"

## Questions?

Feel free to open an issue with the "question" label if you have any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under its MIT License.