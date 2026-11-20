import os
import subprocess
import time

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = r"D:\code_injectors\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

targets = [
    {
        "name": "auth_desktop_1890x805.png",
        "url": "http://127.0.0.1:8000/signup/",
        "window_size": "1890,805"
    },
    {
        "name": "auth_desktop_1440x900.png",
        "url": "http://127.0.0.1:8000/signup/",
        "window_size": "1440,900"
    },
    {
        "name": "landing_desktop_1440x900.png",
        "url": "http://127.0.0.1:8000/",
        "window_size": "1440,900"
    },
    {
        "name": "scanner_desktop_1440x900.png",
        "url": "http://127.0.0.1:8000/scan/",
        "window_size": "1440,900"
    },
    {
        "name": "dashboard_preview_1440x900.png",
        "url": "http://127.0.0.1:8000/dashboard/?preview=guest",
        "window_size": "1440,900"
    }
]

for t in targets:
    out_path = os.path.join(OUTPUT_DIR, t["name"])
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={t['window_size']}",
        f"--screenshot={out_path}",
        "--hide-scrollbars",
        t["url"]
    ]
    print(f"Capturing {t['name']} from {t['url']} at {t['window_size']}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_path):
        size_kb = os.path.getsize(out_path) / 1024
        print(f"  ✓ Saved {t['name']} ({size_kb:.1f} KB)")
    else:
        print(f"  ✗ Failed to capture {t['name']}: {res.stderr}")

print("Screenshot capture complete!")
