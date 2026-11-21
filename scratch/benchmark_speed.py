import sys
import os
import time
sys.path.insert(0, r"d:\code_injectors")
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.db import connection, reset_queries
from django.conf import settings

settings.DEBUG = True

client = Client()
user = User.objects.get(username='dileep358')
client.force_login(user)

endpoints = [
    '/dashboard/',
    '/dashboard/projects/',
    '/dashboard/code/',
    '/dashboard/secrets/',
    '/dashboard/supply-chain/',
    '/dashboard/scans/',
    '/dashboard/reporting/',
]

print("=== REAL OPTIMIZED BENCHMARK (LIVE VIEWS) ===")
print(f"{'Endpoint':<30} | {'Status':<6} | {'Time (ms)':<10} | {'SQL Queries':<12}")
print("-" * 65)

for ep in endpoints:
    reset_queries()
    t0 = time.perf_counter()
    resp = client.get(ep)
    elapsed = (time.perf_counter() - t0) * 1000
    print(f"{ep:<30} | {resp.status_code:<6} | {elapsed:8.1f} ms | {len(connection.queries):3d} queries")
