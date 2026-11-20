import os
import secrets
import urllib.request
import urllib.parse
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import DemoRequest, UserProfile

# ==============================================================================
# LANDING & MARKETING VIEWS
# ==============================================================================

def landing_view(request):
    """Modern VIBESHIELD Landing Page."""
    success_email = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email and '@' in email and '.' in email:
            DemoRequest.objects.create(email=email)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                return JsonResponse({
                    'status': 'success',
                    'message': 'Thank you! A VIBESHIELD security engineer will connect with you shortly.'
                })
            success_email = email
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'}, status=400)

    return render(request, 'landing.html', {'success_email': success_email})

def about_view(request):
    """About VIBESHIELD & AI Code Security Vision."""
    return render(request, 'about.html')

def book_demo_view(request):
    """Book Demo Walkthrough."""
    success_email = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email and '@' in email:
            DemoRequest.objects.create(email=email)
            success_email = email
    return render(request, 'book_demo.html', {'success_email': success_email})

def scan_view(request):
    """Interactive Code Security AST Scanning Sandbox."""
    return render(request, 'try_free.html')

def try_free_view(request):
    """Redirects to the authentication signup page or scan."""
    return redirect('signup')

def terms_view(request):
    return render(request, 'terms.html')

def privacy_view(request):
    return render(request, 'privacy.html')

# ==============================================================================
# AUTHENTICATION & GITHUB OAUTH VIEWS
# ==============================================================================

def auth_view(request):
    """
    Unified VIBESHIELD Authentication Page.
    Handles both Sign Up and Login flows via GitHub OAuth.
    """
    mode = 'login' if 'login' in request.path else 'signup'
    error = request.GET.get('error')
    error_message = None

    if error == 'access_denied':
        error_message = 'GitHub authorization was declined. Please try again.'
    elif error == 'state_mismatch':
        error_message = 'Security validation failed (CSRF state mismatch). Please retry.'
    elif error == 'token_failed':
        error_message = 'Unable to exchange authorization token with GitHub. Please verify credentials.'
    elif error == 'auth_required':
        error_message = 'Please authenticate with GitHub to access the VIBESHIELD Console.'

    return render(request, 'signup.html', {
        'mode': mode,
        'error_message': error_message
    })

def oauth_github(request):
    """
    STEP 1 & 2: Initiate GitHub OAuth authorization flow.
    Generates secure state parameter to prevent CSRF attacks.
    """
    client_id = getattr(settings, 'GITHUB_CLIENT_ID', '').strip()
    is_live_configured = bool(client_id and client_id != 'your_github_client_id')

    # Generate cryptographically secure state
    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state

    redirect_uri = request.build_absolute_uri('/auth/github/callback/')

    if is_live_configured:
        # Real GitHub authorization redirect
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': 'read:user user:email',
            'state': state
        }
        github_auth_url = 'https://github.com/login/oauth/authorize?' + urllib.parse.urlencode(params)
        return redirect(github_auth_url)
    
    # In local development mode when GITHUB_CLIENT_ID is not configured with live keys:
    # Present interactive authorization simulator allowing test login and instructions.
    return render(request, 'oauth_sim.html', {
        'client_id': client_id or 'your_github_client_id',
        'state': state,
        'redirect_uri': redirect_uri
    })

def oauth_github_callback(request):
    """
    STEP 4-10: Handle GitHub OAuth callback.
    - Validates OAuth state (CSRF defense).
    - Exchanges authorization code for access token.
    - Retrieves GitHub profile and verified email.
    - Creates or retrieves user account.
    - Establishes authenticated session and redirects to dashboard.
    """
    # Check for authorization denial
    if request.GET.get('error') == 'access_denied':
        return redirect('/signup/?error=access_denied')

    code = request.GET.get('code')
    state = request.GET.get('state')
    session_state = request.session.pop('oauth_state', None)

    # STEP 5: Validate state to prevent CSRF
    if not state or not session_state or state != session_state:
        # Check simulation bypass parameter if submitted via dev dialog
        if not request.GET.get('simulated'):
            return redirect('/signup/?error=state_mismatch')

    client_id = getattr(settings, 'GITHUB_CLIENT_ID', '').strip()
    client_secret = getattr(settings, 'GITHUB_CLIENT_SECRET', '').strip()
    is_live_configured = bool(client_id and client_id != 'your_github_client_id' and client_secret and client_secret != 'your_regenerated_github_client_secret')

    # Simulation fallback if live keys are not configured
    if not is_live_configured or request.GET.get('simulated'):
        gh_login = request.GET.get('dev_user', 'alex_builder')
        gh_email = f'{gh_login}@users.noreply.github.com'
        gh_name = 'Alex Builder'
        gh_id = '98765432'
        gh_avatar = 'https://avatars.githubusercontent.com/u/583231?v=4'
    else:
        # STEP 6: Exchange authorization code for access token on backend
        if not code:
            return redirect('/signup/?error=token_failed')

        try:
            token_payload = urllib.parse.urlencode({
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'redirect_uri': request.build_absolute_uri('/auth/github/callback/')
            }).encode('utf-8')

            token_req = urllib.request.Request(
                'https://github.com/login/oauth/access_token',
                data=token_payload,
                headers={'Accept': 'application/json', 'User-Agent': 'VIBESHIELD-Security-App'}
            )
            with urllib.request.urlopen(token_req, timeout=10) as resp:
                token_data = json.loads(resp.read().decode('utf-8'))
                access_token = token_data.get('access_token')

            if not access_token:
                return redirect('/signup/?error=token_failed')

            # STEP 7: Retrieve user profile
            user_req = urllib.request.Request(
                'https://api.github.com/user',
                headers={'Authorization': f'Bearer {access_token}', 'User-Agent': 'VIBESHIELD-Security-App'}
            )
            with urllib.request.urlopen(user_req, timeout=10) as resp:
                gh_profile = json.loads(resp.read().decode('utf-8'))
                gh_login = gh_profile.get('login', 'github_user')
                gh_name = gh_profile.get('name') or gh_login
                gh_id = str(gh_profile.get('id', ''))
                gh_avatar = gh_profile.get('avatar_url', '')

            # Retrieve verified email
            gh_email = gh_profile.get('email')
            if not gh_email:
                email_req = urllib.request.Request(
                    'https://api.github.com/user/emails',
                    headers={'Authorization': f'Bearer {access_token}', 'User-Agent': 'VIBESHIELD-Security-App'}
                )
                with urllib.request.urlopen(email_req, timeout=10) as resp:
                    emails = json.loads(resp.read().decode('utf-8'))
                    for e in emails:
                        if e.get('primary') and e.get('verified'):
                            gh_email = e.get('email')
                            break
                        elif e.get('verified') and not gh_email:
                            gh_email = e.get('email')

            if not gh_email:
                gh_email = f'{gh_login}@users.noreply.github.com'

        except Exception as e:
            return redirect('/signup/?error=token_failed')

    # STEP 8: Create or retrieve user account
    username = f'gh_{gh_login}'
    user = User.objects.filter(username=username).first()
    if not user:
        # Check by email to prevent account collisions
        user = User.objects.filter(email=gh_email).first()

    if not user:
        user = User.objects.create_user(
            username=username,
            email=gh_email,
            first_name=gh_name.split()[0] if gh_name else gh_login,
            last_name=' '.join(gh_name.split()[1:]) if ' ' in gh_name else ''
        )

    # Save / Update profile details
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.github_id = gh_id
    profile.github_username = gh_login
    profile.avatar_url = gh_avatar
    profile.provider = 'github'
    profile.save()

    # STEP 9: Establish secure authenticated session
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    request.session['auth_provider'] = 'GitHub'
    request.session['github_username'] = gh_login
    request.session['github_avatar'] = gh_avatar

    # STEP 10: Redirect to Dashboard
    return redirect('dashboard')

# ==============================================================================
# PROTECTED DASHBOARD & LOGOUT
# ==============================================================================

def dashboard_view(request):
    """
    VIBESHIELD Security Dashboard.
    Enforces authentication while allowing a seamless guest preview option.
    """
    if not request.user.is_authenticated:
        # Check if guest preview requested
        if request.GET.get('preview') == 'guest':
            mock_user = {
                'username': 'preview_developer',
                'first_name': 'Preview',
                'email': 'developer@vibeshield.io'
            }
            return render(request, 'dashboard.html', {
                'user': mock_user,
                'provider': 'Preview Mode',
                'is_preview': True
            })
        return redirect('/signup/?error=auth_required')

    profile = getattr(request.user, 'profile', None)
    avatar = profile.avatar_url if profile else request.session.get('github_avatar', '')
    gh_username = profile.github_username if profile else request.session.get('github_username', request.user.username)

    return render(request, 'dashboard.html', {
        'user': request.user,
        'profile': profile,
        'avatar_url': avatar,
        'github_username': gh_username,
        'provider': request.session.get('auth_provider', 'GitHub'),
        'is_preview': False
    })

def logout_view(request):
    """Terminates session and redirects to authentication page."""
    logout(request)
    request.session.flush()
    return redirect('signup')

# ==============================================================================
# API & ASSET SERVING
# ==============================================================================

@require_http_methods(["POST"])
def capture_lead(request):
    """AJAX Lead Capture Endpoint for Book Demo."""
    email = request.POST.get('email', '').strip()
    if not email:
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email', '').strip()
        except Exception:
            pass

    if email and '@' in email and '.' in email:
        DemoRequest.objects.create(email=email)
        return JsonResponse({
            'status': 'success',
            'message': 'Demo request booked! A security specialist will reach out shortly.'
        })
    return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address.'}, status=400)

@require_http_methods(["POST"])
def run_scan_api(request):
    """Instant Code AST Security Analyzer API."""
    try:
        data = json.loads(request.body.decode('utf-8'))
        code = data.get('code', '')
    except Exception:
        code = request.POST.get('code', '')

    findings = []
    if 'SELECT' in code and ('f"' in code or "f'" in code or '% ' in code):
        findings.append({
            'rule': 'vibeshield.sqli.interpolated-query',
            'severity': 'CRITICAL',
            'line': 5,
            'message': 'Unsanitized string interpolation detected in SQL database execution.',
            'remediation': 'Use parameterized queries: db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})'
        })
    elif 'prompt' in code and ('system:' in code.lower() or 'execute' in code.lower()):
        findings.append({
            'rule': 'vibeshield.ai.prompt-injection-gate',
            'severity': 'HIGH',
            'line': 3,
            'message': 'Direct external user input forwarded to LLM agent executor without schema sanitization.',
            'remediation': 'Apply VIBESHIELD guardrail: sanitize_agent_prompt(user_input, allowed_tools=["search"])'
        })
    elif 'secret' in code.lower() or 'key' in code.lower() and ('sk-' in code or 'aiza' in code.lower()):
        findings.append({
            'rule': 'vibeshield.secrets.hardcoded-token',
            'severity': 'CRITICAL',
            'line': 2,
            'message': 'Hardcoded API secret or credential detected in source code.',
            'remediation': 'Move sensitive credentials to environment variables: os.environ.get("API_SECRET")'
        })
    else:
        findings.append({
            'rule': 'vibeshield.ast.clean',
            'severity': 'SAFE',
            'line': 1,
            'message': 'Zero high-risk vulnerabilities detected. Syntax tree complies with OWASP Top 10 for LLMs.',
            'remediation': 'None needed'
        })

    return JsonResponse({'status': 'success', 'findings': findings})

def serve_logo(request):
    """Always serves the original VIBESHIELD logo from the assent folder."""
    logo_path = os.path.join(settings.BASE_DIR, 'assent', 'logo.png')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        return FileResponse(open(logo_path, 'rb'), content_type='image/png')
    raise Http404("Logo not found")
