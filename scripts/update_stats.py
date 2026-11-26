"""Generate a local SVG from public GitHub repository metadata."""
import datetime
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

headers = {"Accept": "application/vnd.github+json", "User-Agent": "ARWA044-profile-stats"}
if os.environ.get("GH_TOKEN"):
    headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
repos = []
page = 1
while True:
    request = Request(
        f"https://api.github.com/users/ARWA044/repos?type=owner&per_page=100&page={page}",
        headers=headers,
    )
    with urlopen(request, timeout=30) as response:
        batch = json.load(response)
    if not isinstance(batch, list):
        raise ValueError("Unexpected GitHub response")
    repos.extend(item for item in batch if not item.get("private", False))
    if len(batch) < 100:
        break
    page += 1

count = len(repos)
stars = sum(item["stargazers_count"] for item in repos)
forks = sum(item["forks_count"] for item in repos)
date = datetime.datetime.now(datetime.timezone.utc).date()
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="460" height="180" viewBox="0 0 460 180" role="img" aria-labelledby="title desc">
<title id="title">ARWA044 GitHub statistics</title>
<desc id="desc">{count} public repositories, {stars} stars received, {forks} forks received.</desc>
<rect x="1" y="1" width="458" height="178" rx="14" fill="#141321" stroke="#44334f"/>
<text x="22" y="35" fill="#fe428e" font-family="Verdana,Arial,sans-serif" font-size="18" font-weight="bold">GitHub Statistics</text>
<g font-family="Verdana,Arial,sans-serif" font-size="13" fill="#a9fef7">
<text x="22" y="69">Public repositories</text><text x="432" y="69" text-anchor="end" font-weight="bold">{count}</text>
<text x="22" y="98">Stars received</text><text x="432" y="98" text-anchor="end" font-weight="bold">{stars}</text>
<text x="22" y="127">Forks received</text><text x="432" y="127" text-anchor="end" font-weight="bold">{forks}</text>
</g><text x="22" y="155" fill="#b4a8c0" font-family="Verdana,Arial,sans-serif" font-size="10">Public repository snapshot · {date}</text>
</svg>"""
path = Path("assets/github-stats.svg")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(svg + "\n", encoding="utf-8")
