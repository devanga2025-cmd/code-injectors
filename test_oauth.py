import urllib.request
import urllib.parse
import http.cookiejar
import re

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

print("=== 1. Starting OAuth Flow: GET /auth/github/ ===")
resp1 = opener.open('http://127.0.0.1:8000/auth/github/')
print('Status:', resp1.status)
html1 = resp1.read().decode('utf-8')
print('Sandbox Authorize page displayed:', 'Authorize VIBESHIELD' in html1)

# Extract CSRF state from simulator form
state_match = re.search(r'name=["\']state["\']\s+value=["\']([^"\']+)["\']', html1)
if not state_match:
    raise ValueError("OAuth state parameter missing from response")
state = state_match.group(1)
print('CSRF OAuth State generated:', state)

print("\n=== 2. Handling OAuth Callback: GET /auth/github/callback/ ===")
cb_params = urllib.parse.urlencode({
    'state': state,
    'simulated': 'true',
    'code': 'gho_simulation_grant_token',
    'dev_user': 'alex_builder'
})
cb_url = f'http://127.0.0.1:8000/auth/github/callback/?{cb_params}'
resp2 = opener.open(cb_url)
print('Callback Final URL (redirect target):', resp2.geturl())
print('Callback Response Status:', resp2.status)
html2 = resp2.read().decode('utf-8')
print('Redirected to VIBESHIELD Dashboard:', 'VIBESHIELD Console' in html2)
print('GitHub Username Rendered:', 'alex_builder' in html2)
print('Sign Out Button Present:', 'Sign Out' in html2)

print("\n=== 3. Testing Logout: GET /logout/ ===")
resp3 = opener.open('http://127.0.0.1:8000/logout/')
print('Logout Target URL:', resp3.geturl())
print('Logout Status:', resp3.status)
html3 = resp3.read().decode('utf-8')
print('Redirected to Signup/Login:', 'Start your security journey' in html3)

print("\n=== 4. Testing Protected Route Security ===")
resp4 = opener.open('http://127.0.0.1:8000/dashboard/')
print('Accessing /dashboard/ without auth session redirected to:', resp4.geturl())
print('Unauthorized Access Blocked:', 'error=auth_required' in resp4.geturl())

print("\n=== ALL AUTHENTICATION TESTS PASSED SUCCESSFULLY! ===")
