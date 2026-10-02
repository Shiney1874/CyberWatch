"""Fetch headline metadata only; keep last successful data on source failure."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("CISA", "https://www.cisa.gov/cybersecurity-advisories/all.xml"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
]

def fetch(source):
    name, url = source
    request = urllib.request.Request(url, headers={"User-Agent": "CyberWatch headline reader/1.0"})
    with urllib.request.urlopen(request, timeout=25) as response:
        content = response.read(2_000_000)
    root = ET.fromstring(content)
    result = []
    for item in root.findall(".//item")[:6]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        date = item.findtext("pubDate") or ""
        parsed = urllib.parse.urlparse(link)
        if not title or parsed.scheme != "https" or not parsed.netloc:
            continue
        try:
            date = parsedate_to_datetime(date).astimezone(timezone.utc).isoformat()
        except (ValueError, TypeError):
            date = ""
        result.append({"title": title, "url": link, "date": date, "source": name})
    if not result:
        raise ValueError("No valid RSS items")
    return result

def main():
    path = ROOT / "data" / "news.json"
    previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"items": []}
    items, errors = [], []
    successful = 0
    with ThreadPoolExecutor(max_workers=len(SOURCES)) as pool:
        futures = [(source, pool.submit(fetch, source)) for source in SOURCES]
        for (name, _), future in futures:
            try:
                items.extend(future.result())
                successful += 1
                print(name + ": fetched headlines")
            except Exception as exc:
                errors.append(name)
                items.extend(item for item in previous.get("items", []) if item.get("source") == name)
                print(name + ": unavailable (" + type(exc).__name__ + ")")
    if not successful:
        print("No source updated; retaining previous snapshot.")
        return
    items.sort(key=lambda item: item.get("date", ""), reverse=True)
    output = {"updated": datetime.now(timezone.utc).isoformat(), "items": items[:12], "errors": errors}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
