with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. Code findings card tag
code_card_pattern = r'<div class="finding-item-card[^"]*crit[^>]*>'
# Let's inspect the 3 card templates in templates/dashboard.html
card_patterns = [
    (
        r'<div class="finding-item-card [^>]*onclick="openFindingDrawer\([^)]*\)[^>]*>',
        '''<div class="finding-item-card {% if f.severity == 'CRITICAL' %}crit{% elif f.severity == 'HIGH' %}high{% endif %}" data-finding-id="{{ f.id }}" data-rule="{{ f.rule_id }}" data-file="{{ f.file_path }}" data-line="{{ f.line_number }}" data-repo="{{ f.repository.name }}" data-repoid="{{ f.repository.id }}" data-sev="{{ f.severity }}" data-cat="{{ f.get_category_display }}" data-reach="{{ f.get_reachability_display }}" data-status="{{ f.status }}" data-message="{{ f.message }}" data-remediation="{{ f.remediation }}" onclick="openFindingDrawer({{ f.id }}, this)" style="cursor: pointer; transition: border-color var(--transition);" title="Click to view AI Security Explanation & Remediation Diff">'''
    )
]

# Let's find each finding-item-card
lines = text.splitlines()
for i, line in enumerate(lines):
    if 'class="finding-item-card' in line:
        print(f"Card at line {i+1}: {line[:120]}...")
