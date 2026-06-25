# github-mcp

A small [MCP](https://modelcontextprotocol.io/) server, built with
[FastMCP](https://gofastmcp.com/), that exposes read-only GitHub data as tools
your AI assistant (Claude, etc.) can call.

It talks to the public GitHub REST API, so no token is required to get started —
though setting one raises your rate limit.

## Tools

| Tool | Description |
| --- | --- |
| `get_github_user` | Public profile for a user: name, bio, followers, public repo count. |
| `get_github_repo` | Info about a repo: description, stars, forks, language, open issues. |
| `list_user_repos` | A user's public repos (most recently updated first). |
| `search_github_repos` | Search public repos by keyword, sorted by stars. |

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/) (or [uv](https://docs.astral.sh/uv/))

## Installation

```bash
git clone https://github.com/anujsingla/github-mcp.git
cd github-mcp
poetry install
```

## Configuration

No token is needed for basic use, but the public GitHub API allows only 60
requests/hour unauthenticated. Set a [personal access token](https://github.com/settings/tokens)
to raise the limit to 5,000/hour:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

## Running

```bash
poetry run python -m github_mcp.server
```

## Using with Claude Code

Register the server so Claude can call its tools:

```bash
claude mcp add github -- poetry run python -m github_mcp.server
```

Then ask things like *"Look up the GitHub user octocat"* or
*"Search GitHub for popular rust web frameworks."*

## Project structure

```
src/github_mcp/server.py   # FastMCP server and tool definitions
tests/                     # Tests
```

## License

MIT
