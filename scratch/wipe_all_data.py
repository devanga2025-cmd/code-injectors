import os
import sys
import shutil

sys.path.insert(0, r"d:\code_injectors")
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import SecurityFinding, SecurityScan, Repository, FeedbackSubmission, DemoRequest, UserProfile
from django.contrib.auth.models import User

print("--- STARTING DATABASE CLEANUP ---")

# 1. Delete all security findings
num_findings = SecurityFinding.objects.count()
SecurityFinding.objects.all().delete()
print(f"1. Deleted {num_findings} SecurityFinding records.")

# 2. Delete all security scans
num_scans = SecurityScan.objects.count()
SecurityScan.objects.all().delete()
print(f"2. Deleted {num_scans} SecurityScan records.")

# 3. Delete all repositories
num_repos = Repository.objects.count()
Repository.objects.all().delete()
print(f"3. Deleted {num_repos} Repository records.")

# 4. Delete demo requests & feedback
num_demo = DemoRequest.objects.count()
DemoRequest.objects.all().delete()
print(f"4. Deleted {num_demo} DemoRequest records.")

num_fb = FeedbackSubmission.objects.count()
FeedbackSubmission.objects.all().delete()
print(f"5. Deleted {num_fb} FeedbackSubmission records.")

# 6. Delete sample/test user accounts (preserve dileep358, kaif)
keep_usernames = ['dileep358', 'kaif']
deleted_users = []
for u in User.objects.all():
    if u.username not in keep_usernames:
        deleted_users.append(u.username)
        u.delete()

print(f"6. Cleaned test users: {deleted_users}. Kept real accounts: {keep_usernames}")

# 7. Clean up scan temp files on Drive D
scan_tmp = r"d:\tmp\scans"
if os.path.exists(scan_tmp):
    shutil.rmtree(scan_tmp, ignore_errors=True)
    os.makedirs(scan_tmp, exist_ok=True)
    print("7. Cleaned temporary scan workspaces.")

print("--- DATABASE WIPE COMPLETED: 100% CLEAN SLATE ---")
