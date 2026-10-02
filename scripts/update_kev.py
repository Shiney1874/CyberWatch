"""Save the newest entries in CISA's public exploited-vulnerability catalog."""
from datetime import datetime, timezone
from pathlib import Path
import json
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
URL = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"

def main():
    try:
        request = urllib.request.Request(URL, headers={"User-Agent": "CyberWatch/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
        entries = data.get("vulnerabilities", [])
        if not entries:
            raise ValueError("Empty catalog")
        entries.sort(key=lambda item: (item.get("dateAdded", ""), item.get("cveID", "")), reverse=True)
        fields = ["cveID", "vendorProject", "product", "vulnerabilityName", "dateAdded", "requiredAction", "knownRansomwareCampaignUse", "notes"]
        output = {"updated": datetime.now(timezone.utc).isoformat(), "catalogVersion": data.get("catalogVersion"), "total": len(entries), "items": [{key: item.get(key, "") for key in fields} for item in entries[:8]]}
        path = ROOT / "data" / "kev.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("CISA: saved 8 most recently added vulnerabilities")
    except Exception as exc:
        print("CISA catalog unavailable; keeping saved data: " + type(exc).__name__)

if __name__ == "__main__":
    main()
