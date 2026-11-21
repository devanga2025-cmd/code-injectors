with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. Code finding card
old_code_card = '<div class="finding-item-card {% if f.severity == \'CRITICAL\' %}crit{% elif f.severity == \'HIGH\' %}high{% endif %}" data-engine="{% if \'bandit\' in f.rule_id|lower %}bandit{% elif \'semgrep\' in f.rule_id|lower %}semgrep{% else %}other{% endif %}" data-severity="{{ f.severity }}" data-text="{{ f.rule_id|lower }} {{ f.file_path|lower }} {{ f.message|lower }}" onclick="openFindingDrawer({{ f.id }}, this)" style="cursor: pointer; transition: border-color var(--transition);" title="Click to view AI Security Explanation & Remediation Diff">'
new_code_card = '<div class="finding-item-card {% if f.severity == \'CRITICAL\' %}crit{% elif f.severity == \'HIGH\' %}high{% endif %}" data-finding-id="{{ f.id }}" data-rule="{{ f.rule_id }}" data-file="{{ f.file_path }}" data-line="{{ f.line_number }}" data-repo="{{ f.repository.name }}" data-repoid="{{ f.repository.id }}" data-sev="{{ f.severity }}" data-cat="Code Security" data-reach="{{ f.get_reachability_display }}" data-status="{{ f.status }}" data-message="{{ f.message|escape }}" data-remediation="{{ f.remediation|escape }}" data-engine="{% if \'bandit\' in f.rule_id|lower %}bandit{% elif \'semgrep\' in f.rule_id|lower %}semgrep{% else %}other{% endif %}" data-severity="{{ f.severity }}" data-text="{{ f.rule_id|lower }} {{ f.file_path|lower }} {{ f.message|lower }}" onclick="openFindingDrawer({{ f.id }}, this)" style="cursor: pointer; transition: border-color var(--transition);" title="Click to view AI Security Explanation & Remediation Diff">'

if old_code_card in text:
    text = text.replace(old_code_card, new_code_card, 1)
    print("1. Updated code finding card tag")
else:
    print("1. Could not match old_code_card directly, searching pattern")
    text = re.sub(
        r'<div class="finding-item-card \{% if f\.severity == [^>]*onclick="openFindingDrawer\([^)]*\)[^>]*>',
        new_code_card,
        text,
        count=1
    )
    print("1. Replaced code finding card via pattern")

# 2. Secrets finding card
old_secrets_card = '<div class="finding-item-card high" data-type="{% if \'openai\' in f.rule_id|lower %}openai{% elif \'aws\' in f.rule_id|lower %}aws{% else %}token{% endif %}" data-severity="{{ f.severity }}" data-text="{{ f.rule_id|lower }} {{ f.file_path|lower }} {{ f.message|lower }}" onclick="openFindingDrawer({{ f.id }}, this)" style="cursor: pointer;" title="Click to view secret remediation details">'
new_secrets_card = '<div class="finding-item-card high" data-finding-id="{{ f.id }}" data-rule="{{ f.rule_id }}" data-file="{{ f.file_path }}" data-line="{{ f.line_number }}" data-repo="{{ f.repository.name }}" data-repoid="{{ f.repository.id }}" data-sev="{{ f.severity }}" data-cat="Secrets Detection" data-reach="Reachable" data-status="{{ f.status }}" data-message="{{ f.message|escape }}" data-remediation="{{ f.remediation|escape }}" data-type="{% if \'openai\' in f.rule_id|lower %}openai{% elif \'aws\' in f.rule_id|lower %}aws{% else %}token{% endif %}" data-severity="{{ f.severity }}" data-text="{{ f.rule_id|lower }} {{ f.file_path|lower }} {{ f.message|lower }}" onclick="openFindingDrawer({{ f.id }}, this)" style="cursor: pointer;" title="Click to view secret remediation details">'

if old_secrets_card in text:
    text = text.replace(old_secrets_card, new_secrets_card, 1)
    print("2. Updated secrets finding card tag")
else:
    print("2. Searching secrets pattern")
    text = re.sub(
        r'<div class="finding-item-card high" data-type=[^>]*onclick="openFindingDrawer\([^)]*\)[^>]*>',
        new_secrets_card,
        text,
        count=1
    )
    print("2. Replaced secrets card via pattern")

# 3. Supply chain finding card
old_supply_card = '<div class="finding-item-card" data-ecosystem="{% if \'npm\' in f.rule_id|lower %}npm{% else %}pypi{% endif %}" data-severity="{{ f.severity }}" data-text="{{ f.rule_id|lower }} {{ f.file_path|lower }} {{ f.message|lower }}" onclick="openFindingDrawer({{ f.id }}, this)" style="cursor: pointer;" title="Click to view dependency CVE details">'
new_supply_card = '<div class="finding-item-card" data-finding-id="{{ f.id }}" data-rule="{{ f.rule_id }}" data-file="{{ f.file_path }}" data-line="{{ f.line_number }}" data-repo="{{ f.repository.name }}" data-repoid="{{ f.repository.id }}" data-sev="{{ f.severity }}" data-cat="Supply Chain" data-reach="Reachable Runtime" data-status="{{ f.status }}" data-message="{{ f.message|escape }}" data-remediation="{{ f.remediation|escape }}" data-ecosystem="{% if \'npm\' in f.rule_id|lower %}npm{% else %}pypi{% endif %}" data-severity="{{ f.severity }}" data-text="{{ f.rule_id|lower }} {{ f.file_path|lower }} {{ f.message|lower }}" onclick="openFindingDrawer({{ f.id }}, this)" style="cursor: pointer;" title="Click to view dependency CVE details">'

if old_supply_card in text:
    text = text.replace(old_supply_card, new_supply_card, 1)
    print("3. Updated supply chain card tag")
else:
    print("3. Searching supply chain pattern")
    text = re.sub(
        r'<div class="finding-item-card" data-ecosystem=[^>]*onclick="openFindingDrawer\([^)]*\)[^>]*>',
        new_supply_card,
        text,
        count=1
    )
    print("3. Replaced supply chain card via pattern")

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved updated dashboard.html successfully!")
