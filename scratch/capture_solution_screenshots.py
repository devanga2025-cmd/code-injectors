import os
import subprocess
import shutil

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARTIFACTS_DIR = r"C:\Users\DELL\.gemini\antigravity\brain\818d4e7c-d83b-4423-a2cc-6b619bb968aa"
OUTPUT_DIR = r"D:\code_injectors\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

targets = [
    {
        "name": "dashboard_solution_hero.png",
        "url": "http://127.0.0.1:8000/dashboard/?dev_user=dileep358",
        "window_size": "1440,900"
    },
    {
        "name": "code_findings_dynamic.png",
        "url": "http://127.0.0.1:8000/dashboard/code/?dev_user=dileep358",
        "window_size": "1440,900"
    },
    {
        "name": "secrets_findings_dynamic.png",
        "url": "http://127.0.0.1:8000/dashboard/secrets/?dev_user=dileep358",
        "window_size": "1440,900"
    },
    {
        "name": "scan_history_dynamic.png",
        "url": "http://127.0.0.1:8000/dashboard/scans/?dev_user=dileep358",
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
    print(f"Capturing {t['name']}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_path):
        size_kb = os.path.getsize(out_path) / 1024
        print(f"  ✓ Saved {t['name']} ({size_kb:.1f} KB)")
        # Copy to artifacts directory as well
        art_path = os.path.join(ARTIFACTS_DIR, t["name"])
        shutil.copy2(out_path, art_path)
    else:
        print(f"  ✗ Failed: {res.stderr}")

print("All screenshots captured and saved to artifacts!")
