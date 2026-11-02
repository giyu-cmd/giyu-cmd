import re, json, os, urllib.request, datetime

USER = "giyu-cmd"  # change this to your GitHub username
TOKEN = os.environ["STATS_TOKEN"]

query = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      restrictedContributionsCount
      contributionCalendar { totalContributions }
    }
  }
}
"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": query, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
)
with urllib.request.urlopen(req) as r:
    u = json.load(r)["data"]["user"]

cc = u["contributionsCollection"]
total = cc["contributionCalendar"]["totalContributions"]
private = cc["restrictedContributionsCount"]
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

block = (
    f"- Contributions (last year): **{total}**\n"
    f"- Of which private: **{private}**\n"
    f"- Followers: **{u['followers']['totalCount']}**\n"
    f"- Last updated: {now}"
)

# Write the block into README.md between the markers
with open("README.md", encoding="utf-8") as f:
    readme = f.read()

new = re.sub(
    r"(<!-- STATS:START -->)(.*?)(<!-- STATS:END -->)",
    rf"\1\n{block}\n\3",
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new)
