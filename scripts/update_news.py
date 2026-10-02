"""Fetch headline metadata only; keep last successful data on source failure."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
import json
import time
import urllib.error
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("CISA", "https://www.cisa.gov/cybersecurity-advisories/all.xml"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
]
KEV_URL = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"

def download(url):
    request = urllib.request.Request(url, headers={
        "User-Agent": "CyberWatch/1.1 (+https://shiney1874.github.io/CyberWatch/)",
        "Accept": "application/rss+xml, application/xml, application/json, text/xml;q=0.9, */*;q=0.5",
    })
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return response.read(5_000_000)
        except urllib.error.HTTPError as exc:
            if attempt or exc.code not in (429, 500, 502, 503, 504):
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt:
                raise
        time.sleep(1)

def fetch_cisa_kev():
    """Use official catalogue additions, explicitly labelled as KEV updates."""
    data = json.loads(download(KEV_URL))
    entries = sorted(data.get("vulnerabilities", []), key=lambda item: (item.get("dateAdded", ""), item.get("cveID", "")), reverse=True)
    result = []
    for item in entries:
        identifier = item.get("cveID", "")
        added = item.get("dateAdded", "")
        if not identifier.startswith("CVE-") or not added:
            continue
        try:
            date = datetime.fromisoformat(added).replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            continue
        product = " · ".join(str(item.get(key, "")) for key in ("vendorProject", "product"))
        result.append({"title": f"Added to CISA’s exploited-vulnerability catalogue: {identifier} — {product}",
                       "url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                       "date": date, "source": "CISA KEV", "dateType": "catalogue addition"})
        if len(result) == 6:
            break
    if not result:
        raise ValueError("No valid CISA catalogue additions")
    return result

def fetch(source):
    name, url = source
    content = download(url)
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

def fetch_source(source):
    try:
        return fetch(source), "fresh"
    except Exception as exc:
        reason = f"HTTP {exc.code}" if isinstance(exc, urllib.error.HTTPError) else type(exc).__name__
        if source[0] != "CISA":
            raise
        print(f"CISA RSS unavailable ({reason}); trying official KEV data")
        return fetch_cisa_kev(), "fallback"

def main():
    path = ROOT / "data" / "news.json"
    previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"items": []}
    items, errors, source_status = [], [], {}
    successful = 0
    now = datetime.now(timezone.utc).isoformat()
    with ThreadPoolExecutor(max_workers=len(SOURCES)) as pool:
        futures = [(source, pool.submit(fetch_source, source)) for source in SOURCES]
        for (name, _), future in futures:
            try:
                fetched, state = future.result()
                items.extend(fetched)
                source_status[name] = {"state": state, "updated": now}
                successful += 1
                print(name + (": refreshed official KEV updates" if state == "fallback" else ": fetched headlines"))
            except Exception as exc:
                errors.append(name)
                items.extend(item for item in previous.get("items", []) if item.get("source") in (name, "CISA KEV" if name == "CISA" else name))
                old_status = previous.get("sourceStatus", {}).get(name, {})
                source_status[name] = {"state": "saved", "updated": old_status.get("updated", previous.get("updated"))}
                reason = f"HTTP {exc.code}" if isinstance(exc, urllib.error.HTTPError) else type(exc).__name__
                print(name + ": unavailable (" + reason + "); retaining saved items")
    items.sort(key=lambda item: item.get("date", ""), reverse=True)
    output = {"updated": now if successful else previous.get("updated", now), "items": items[:12], "errors": errors, "sourceStatus": source_status}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
