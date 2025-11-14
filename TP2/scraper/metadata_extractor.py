from typing import Dict
from bs4 import BeautifulSoup


def extract_standard_meta(html: str) -> Dict[str, str]:
    soup = BeautifulSoup(html, "lxml")
    meta = {}
    for m in soup.find_all("meta"):
        name = m.get("name")
        if name and name.lower() in ("description", "keywords"):
            meta[name.lower()] = m.get("content", "")
        prop = m.get("property")
        if prop and prop.startswith("og:"):
            meta[prop] = m.get("content", "")
    return meta