import os
import sys

sys.path.insert(0, r"d:\code_injectors")
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\DELL\.gemini\antigravity\brain\818d4e7c-d83b-4423-a2cc-6b619bb968aa"

user = User.objects.filter(username='dileep358').first()
session = SessionStore()
session['_auth_user_id'] = str(user.pk)
session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
session['_auth_user_hash'] = user.get_session_auth_hash()
session.save()
session_key = session.session_key

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    context.add_cookies([
        {
            'name': 'sessionid',
            'value': session_key,
            'domain': '127.0.0.1',
            'path': '/',
            'httpOnly': True,
            'secure': False,
            'sameSite': 'Lax'
        }
    ])

    page = context.new_page()
    page.goto('http://127.0.0.1:8000/dashboard/', wait_until='networkidle')

    # 1. Capture Dashboard view with new CodeShield AI Solution Banner & Sidebar without Integrations
    banner_img = os.path.join(artifact_dir, 'codeshield_solution_banner_preview.png')
    page.screenshot(path=banner_img, full_page=False)
    print(f"Captured: {banner_img}")

    # 2. Capture Sidebar close-up
    sidebar = page.locator('.dash-sidebar')
    if sidebar.count() > 0:
        sidebar_img = os.path.join(artifact_dir, 'sidebar_without_integrations_preview.png')
        sidebar.screenshot(path=sidebar_img)
        print(f"Captured: {sidebar_img}")

    # 3. Open a vulnerability finding in the drawer to preview Rescan & Verify Fix + Priority
    finding_card = page.locator('.activity-item, .card-link, [onclick*="openFindingDrawer"]').first
    if finding_card.count() > 0:
        finding_card.click()
        page.wait_for_timeout(1000)
        drawer_img = os.path.join(artifact_dir, 'vuln_drawer_rescan_preview.png')
        page.screenshot(path=drawer_img, full_page=False)
        print(f"Captured: {drawer_img}")

    browser.close()
print("Playwright screenshot capture completed successfully.")
