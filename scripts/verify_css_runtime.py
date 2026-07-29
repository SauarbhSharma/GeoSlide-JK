import urllib.request
import re

routes = ['/', '/explorer', '/districts', '/rainfall', '/location-check', '/transparency', '/status']

print("=== GeoSlide-JK CSS Runtime Verification ===")
for r in routes:
    url = f"http://localhost:3000{r}"
    try:
        req = urllib.request.urlopen(url)
        html = req.read().decode('utf-8')
        css_files = re.findall(r'href="(/_next/static/css/[^"]+)"', html)
        print(f"Route '{r}': HTTP {req.status}, HTML size={len(html)} bytes, CSS assets={len(css_files)}")
        for css_path in css_files:
            css_url = f"http://localhost:3000{css_path}"
            css_req = urllib.request.urlopen(css_url)
            css_content = css_req.read().decode('utf-8')
            print(f"  -> CSS Asset '{css_path}': HTTP {css_req.status}, size={len(css_content)} bytes")
            assert css_req.status == 200, f"CSS asset returned non-200 status: {css_req.status}"
            assert len(css_content) > 1000, "CSS asset is unexpectedly small"
    except Exception as e:
        print(f"Route '{r}' FAILED: {e}")
