import os

import httpx
from fastmcp import FastMCP

mcp = FastMCP("GitHub Server")

GITHUB_API = "https://api.github.com"


def _headers() -> dict:
    """Standard GitHub API headers. Uses GITHUB_TOKEN if set to raise the
    unauthenticated rate limit from 60 to 5000 requests/hour."""
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


@mcp.tool()
def get_github_user(username: str) -> dict:
    """Get public profile info for a GitHub user: name, bio, followers,
    and public repo count."""
    url = f"{GITHUB_API}/users/{username}"
    r = httpx.get(url, headers=_headers())
    r.raise_for_status()
    data = r.json()
    return {
        "login": data["login"],
        "name": data["name"],
        "bio": data["bio"],
        "company": data["company"],
        "location": data["location"],
        "followers": data["followers"],
        "following": data["following"],
        "public_repos": data["public_repos"],
        "html_url": data["html_url"],
    }


@mcp.tool()
def get_github_repo(owner: str, repo: str) -> dict:
    """Get public information about a repository by owner and name:
    description, stars, forks, language, and open issues."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}"
    r = httpx.get(url, headers=_headers())
    r.raise_for_status()
    data = r.json()
    return {
        "full_name": data["full_name"],
        "description": data["description"],
        "language": data["language"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "open_issues": data["open_issues_count"],
        "default_branch": data["default_branch"],
        "topics": data.get("topics", []),
        "html_url": data["html_url"],
    }


@mcp.tool()
def list_user_repos(username: str, limit: int = 10) -> list[dict]:
    """List a user's public repositories (most recently updated first),
    each with name, description, stars, and language."""
    url = f"{GITHUB_API}/users/{username}/repos"
    params = {"sort": "updated", "per_page": min(limit, 100)}
    r = httpx.get(url, headers=_headers(), params=params)
    r.raise_for_status()
    return [
        {
            "name": repo["name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "html_url": repo["html_url"],
        }
        for repo in r.json()
    ]


@mcp.tool()
def search_github_repos(query: str, limit: int = 10) -> list[dict]:
    """Search GitHub for public repositories matching a keyword query,
    sorted by stars (most popular first). Each result has full name,
    description, stars, and language."""
    url = f"{GITHUB_API}/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": min(limit, 100)}
    r = httpx.get(url, headers=_headers(), params=params)
    r.raise_for_status()
    return [
        {
            "full_name": repo["full_name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "html_url": repo["html_url"],
        }
        for repo in r.json()["items"]
    ]


if __name__ == "__main__":
    mcp.run()
