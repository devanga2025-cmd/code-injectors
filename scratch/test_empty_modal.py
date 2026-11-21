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

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = r"d:\tmp\cdp_chrome_empty_test"
os.makedirs(user_data, exist_ok=True)

proc = subprocess.Popen([
    chrome_exe,
    "--headless=new",
    "--remote-debugging-port=9223",
    f"--user-data-dir={user_data}",
    "--no-first-run",
    "--no-default-browser-check",
    "--window-size=1560,980",
    "about:blank"
])
time.sleep(2)

async def test_popup():
    try:
        tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json").read().decode())
        ws_url = tabs[0]['webSocketDebuggerUrl']
        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id:
                        return resp.get('result', {})

            await send('Network.enable')
            await send('Network.setCookie', {
                'name': 'sessionid',
                'value': session_key,
                'domain': '127.0.0.1',
                'path': '/',
                'httpOnly': True
            })
            await send('Page.enable')
            await send('Page.navigate', {'url': 'http://127.0.0.1:8000/dashboard/'})
            await asyncio.sleep(2.5)

            # Trigger showEmptyRepoModal
            await send('Runtime.evaluate', {
                'expression': "showEmptyRepoModal('dwarapathaa', 'https://github.com/dileep358/dwarapathaa')"
            })
            await asyncio.sleep(1.0)

            # Capture screenshot
            res = await send('Page.captureScreenshot', {'format': 'png'})
            out_path = r"C:\Users\DELL\.gemini\antigravity\brain\818d4e7c-d83b-4423-a2cc-6b619bb968aa\empty_repo_popup_live.png"
            with open(out_path, 'wb') as f:
                f.write(base64.b64decode(res['data']))
            print(f"Captured: {out_path}")
    finally:
        proc.terminate()

asyncio.run(test_popup())
