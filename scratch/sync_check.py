import os, urllib.request, json
import sys
sys.path.insert(0, r"d:\code_injectors")
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import UserProfile, Repository
from django.contrib.auth.models import User

u = User.objects.get(username='dileep358')
p = UserProfile.objects.get(user=u)
print('Token exists:', bool(p.github_access_token))

req = urllib.request.Request(
    'https://api.github.com/user/repos?per_page=50&sort=updated&type=all',
    headers={
        'Authorization': f'Bearer {p.github_access_token}',
        'User-Agent': 'CodeShield-Security-App',
        'Accept': 'application/vnd.github.v3+json'
    }
)
with urllib.request.urlopen(req, timeout=10) as resp:
    repos_data = json.loads(resp.read().decode('utf-8'))
    print(f'GitHub API returned {len(repos_data)} repositories for {u.username}:')
    for r in repos_data:
        full_name = r.get('full_name')
        is_priv = r.get('private')
        print(f"  GitHub: {full_name} -> Private: {is_priv}")
        db_repo = Repository.objects.filter(user=u, full_name=full_name).first()
        if db_repo:
            print(f"    DB currently has: Private = {db_repo.is_private}")
            if db_repo.is_private != is_priv:
                print(f"    *** MISMATCH! Updating DB to {is_priv} ***")
                db_repo.is_private = is_priv
                db_repo.save()
