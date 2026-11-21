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
from unittest.mock import patch
from core.models import SecurityFinding

client = Client()
user = User.objects.get(username='dileep358')
client.force_login(user)

# Test query count for rendering supply chain template with select_related
with patch('core.views.sync_github_repositories'):
    reset_queries()
    resp = client.get('/dashboard/supply-chain/')
    print(f"Current query count without select_related in view: {len(connection.queries)}")
