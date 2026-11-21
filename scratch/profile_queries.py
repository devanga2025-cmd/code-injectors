import sys
import os
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

reset_queries()
resp = client.get('/dashboard/supply-chain/')

print(f"Total queries: {len(connection.queries)}")
from collections import Counter
table_counts = Counter()
for q in connection.queries:
    sql = q['sql'].strip()
    # find table name
    words = sql.split()
    first_part = ' '.join(words[:4])
    table_counts[first_part] += 1

print("\nTop Query Patterns:")
for pattern, count in table_counts.most_common(10):
    print(f"  {count:3d}x : {pattern}")

print("\nSample queries:")
for q in connection.queries[:15]:
    print(f"[{q['time']}s] {q['sql'][:120]}...")
