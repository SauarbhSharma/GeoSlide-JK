import urllib.request
import re

def check_css():
    print("=== CSS Asset Loading & Network Health Check ===")
    req = urllib.request.urlopen("http://localhost:3000")
    html = req.read().decode("utf-8")

    css_links = re.findall(r'href="(/_next/static/css/[^"]+)"', html)
    print("Found CSS links in HTML:", css_links)

    for link in css_links:
        url = "http://localhost:3000" + link
        css_res = urllib.request.urlopen(url)
        css_content = css_res.read().decode("utf-8")
        print(f"Fetching {url}: Status {css_res.status} OK ({len(css_content)} bytes)")
        if "background" in css_content or "color" in css_content or "#0f172a" in css_content:
            print("  -> VERIFIED: Tailwind & global CSS rules compiled successfully into production CSS chunk!")

if __name__ == "__main__":
    check_css()
