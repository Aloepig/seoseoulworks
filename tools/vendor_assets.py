"""Download the site's existing images and full font subsets for self-hosting."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"}


def fetch(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def save(item):
    url, path = item
    data = fetch(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return len(data)


def main():
    css_url = (
        "https://fonts.googleapis.com/css2?"
        "family=DM+Sans:wght@400..700&"
        "family=Noto+Sans+KR:wght@400..800&"
        "family=Noto+Serif+KR:wght@500..700&display=swap"
    )
    css = fetch(css_url).decode("utf-8")
    urls = sorted(set(re.findall(r"https://[^\s)]+", css)))
    downloads = []
    for url in urls:
        name = hashlib.sha256(url.encode()).hexdigest()[:20] + ".woff2"
        downloads.append((url, ROOT / "assets/fonts" / name))
        css = css.replace(url, "./" + name)
    downloads.extend([
        ("https://images.unsplash.com/photo-1455390582262-044cdead277a?fm=jpg&fit=crop&w=2200&q=85", ROOT / "assets/images/hero.jpg"),
        ("https://images.unsplash.com/photo-1519682337058-a94d519337bc?fm=jpg&fit=crop&w=1200&q=80", ROOT / "assets/images/about.jpg"),
    ])
    for family in ("dmsans", "notosanskr", "notoserifkr"):
        downloads.append((f"https://raw.githubusercontent.com/google/fonts/main/ofl/{family}/OFL.txt", ROOT / "assets/fonts" / (family + "-OFL.txt")))
    with ThreadPoolExecutor(max_workers=8) as pool:
        sizes = list(pool.map(save, downloads))
    (ROOT / "assets/fonts/fonts.css").write_text(css, encoding="utf-8")
    print(f"Saved {len(urls)} font files, 2 images, 3 licenses ({sum(sizes):,} bytes).")


if __name__ == "__main__":
    main()
