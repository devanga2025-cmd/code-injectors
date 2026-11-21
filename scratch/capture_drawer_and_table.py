import asyncio
import base64
import json
import os
import subprocess
import time
import urllib.request
import websockets

import sys
sys.path.insert(0, r"d:\code_injectors")
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore

user = User.objects.get(username='dileep358')
session = SessionStore()
session['_auth_user_id'] = str(user.id)
session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
session['_auth_user_hash'] = user.get_session_auth_hash()
session.save()
session_key = session.session_key

base_dir = r"C:\Users\DELL\.gemini\antigravity\brain\818d4e7c-d83b-4423-a2cc-6b619bb968aa"
user_data = r"d:\tmp\cdp_drawer_profile"
os.makedirs(user_data, exist_ok=True)

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
proc = subprocess.Popen([
    chrome_exe,
    "--headless=new",
    "--remote-debugging-port=9224",
    f"--user-data-dir={user_data}",
    "--no-first-run",
    "--no-default-browser-check",
    "--window-size=1560,1100",
    "about:blank"
])

time.sleep(2)

async def run_capture():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9224/json").read().decode())
    ws_url = tabs[0]['webSocketDebuggerUrl']

    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        msg_id = 0

        async def send_cmd(method, params=None):
            nonlocal msg_id
            msg_id += 1
            payload = {"id": msg_id, "method": method, "params": params or {}}
            await ws.send(json.dumps(payload))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get("id") == msg_id:
                    return resp.get("result")

        await send_cmd("Network.enable")
        await send_cmd("Page.enable")

        await send_cmd("Network.setCookie", {
            "name": "sessionid",
            "value": session_key,
            "domain": "127.0.0.1",
            "path": "/",
            "httpOnly": True
        })

        async def capture(file_name):
            res = await send_cmd("Page.captureScreenshot", {"format": "png"})
            img_bytes = base64.b64decode(res["data"])
            out_path = os.path.join(base_dir, file_name)
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            print(f"Captured: {out_path}")

        # 1. Overview Table scrolled down
        await send_cmd("Page.navigate", {"url": "http://127.0.0.1:8000/dashboard/"})
        await asyncio.sleep(2.5)
        await send_cmd("Runtime.evaluate", {
            "expression": "window.scrollTo(0, 950);"
        })
        await asyncio.sleep(0.5)
        await capture("repos_table_scrolled_private_live.png")

        # 2. Projects tab
        await send_cmd("Page.navigate", {"url": "http://127.0.0.1:8000/dashboard/projects/"})
        await asyncio.sleep(2.0)
        await capture("projects_cards_private_badges_live.png")

        # 3. Supply chain findings tab + open drawer
        await send_cmd("Page.navigate", {"url": "http://127.0.0.1:8000/dashboard/supply-chain/"})
        await asyncio.sleep(2.0)
        
        await send_cmd("Runtime.evaluate", {
            "expression": """
                (() => {
                    const firstCard = document.querySelector('.finding-item-card');
                    if (firstCard) {
                        const id = parseInt(firstCard.getAttribute('data-finding-id'));
                        openFindingDrawer(id, firstCard);
                    }
                })()
            """
        })
        await asyncio.sleep(2.0)
        await capture("drawer_fixed_clean_live.png")

try:
    asyncio.run(run_capture())
finally:
    proc.terminate()
    print("CDP run completed.")
