import urllib.request
import re

try:
    resp = urllib.request.urlopen('http://127.0.0.1:8000/dashboard/')
    print("URL:", resp.geturl())
    html = resp.read().decode('utf-8')
    print("HTML length:", len(html))
    print("Title:", re.search(r'<title>(.*?)</title>', html).group(1) if re.search(r'<title>(.*?)</title>', html) else 'No title')
    m = re.search(r'<div class="drawer-footer">[\s\S]*?</aside>', html)
    if m:
        print("MATCH FOUND:")
        print(m.group(0))
    else:
        print("NO MATCH FOUND")
except Exception as e:
    print("ERROR:", e)
