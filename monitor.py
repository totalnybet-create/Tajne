import json
import re
from datetime import datetime, timezone
from pathlib import Path

from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SOURCES = [
    ("AskGamblers — Polska", "https://www.askgamblers.com/casino-bonuses/countries/pl/no-deposit"),
    ("AskGamblers — bez depozytu", "https://www.askgamblers.com/casino-bonuses/no-deposit"),
    ("NoDeposit.games", "https://nodeposit.games/"),
    ("Plotkus — darmowe spiny", "https://plotkus.pl/darmowe-spiny/"),
]
PHRASES = ["free spins", "no deposit", "free bonus", "free jackpot", "darmowe spiny", "darmowych spinów", "bez depozytu", "bonus za rejestrację", "bonus bez depozytu"]


EXCLUDED = {"script", "style", "noscript", "svg", "nav", "footer"}


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = []
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in EXCLUDED:
            self.hidden.append(tag)

    def handle_endtag(self, tag):
        if tag in EXCLUDED and tag in self.hidden:
            self.hidden.remove(tag)

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def extract_matches(html):
    parser = VisibleText()
    parser.feed(html)
    page_text = re.sub(r"\s+", " ", " ".join(parser.parts))
    matches = []
    for phrase in PHRASES:
        hit = re.search(re.escape(phrase), page_text, re.IGNORECASE)
        if hit:
            matches.append({"phrase": phrase, "excerpt": page_text[max(0, hit.start()-75):min(len(page_text), hit.end()+105)].strip()})
    return matches


def scan(sources=SOURCES, fetch=None, output_path="data.json"):
    output = {"checked_at": datetime.now(timezone.utc).isoformat(), "phrases": PHRASES, "sources": []}
    if fetch is None:
        def fetch(url):
            request = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BonusRadar/1.0)"})
            with urlopen(request, timeout=20) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read(3_000_000).decode(charset, errors="replace")
    for name, url in sources:
        item = {"name": name, "url": url, "status": "error", "matches": []}
        try:
            item["matches"] = extract_matches(fetch(url))
            item["status"] = "ok"
        except (HTTPError, URLError, TimeoutError, OSError, UnicodeError, ValueError) as exc:
            item["error"] = str(exc)[:250]
        output["sources"].append(item)
    Path(output_path).write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    scan()
