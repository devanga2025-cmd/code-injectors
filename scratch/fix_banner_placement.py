import re

dashboard_path = r'd:\code_injectors\templates\dashboard.html'

with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the mistakenly placed banner
banner_match = re.search(r'([ \t]*<!-- CODESHIELD AI SOLUTION & KEY FEATURES HERO BANNER -->[\s\S]*?</div>\s*</div>)', content)
if not banner_match:
    print("Error: Could not find banner in content")
    exit(1)

banner_text = banner_match.group(1)

# Remove the banner from its current location inside the sidebar
content_cleaned = content.replace(banner_text, '')

# Fix line 67 where the anchor tag class was split
content_fixed = re.sub(
    r'<a href="\{% url [\'"]dashboard[\'"] %\}" class="nav-link-btn \{% if active_tab == [\'"]dashboard[\'"] %\}\s*active\{% endif %\}">',
    r'<a href="{% url \'dashboard\' %}" class="nav-link-btn {% if active_tab == \'dashboard\' %}active{% endif %}">',
    content_cleaned
)

# If it was still open:
content_fixed = re.sub(
    r'<a href="\{% url [\'"]dashboard[\'"] %\}" class="nav-link-btn \{% if active_tab == [\'"]dashboard[\'"] %\}(?!active)',
    r'<a href="{% url \'dashboard\' %}" class="nav-link-btn {% if active_tab == \'dashboard\' %}active{% endif %}">',
    content_fixed
)

# Now insert banner right under `<!-- TAB: DASHBOARD (MAIN OVERVIEW) -->\s*\{% if active_tab == 'dashboard' %\}`
body_target = "<!-- TAB: DASHBOARD (MAIN OVERVIEW) -->\n        {% if active_tab == 'dashboard' %}"
if body_target in content_fixed:
    content_fixed = content_fixed.replace(
        body_target,
        body_target + "\n\n" + banner_text,
        1
    )
    print("Successfully inserted banner into dashboard main body!")
else:
    print("Alternate body search:")
    body_target_alt = "{% if active_tab == 'dashboard' %}\n\n\n\n          <!-- THREE-COLUMN OVERVIEW METRICS GRID -->"
    if body_target_alt in content_fixed:
        content_fixed = content_fixed.replace(
            body_target_alt,
            "{% if active_tab == 'dashboard' %}\n\n" + banner_text + "\n\n          <!-- THREE-COLUMN OVERVIEW METRICS GRID -->",
            1
        )
        print("Successfully inserted via alternate body search!")
    else:
        print("Could not match body target!")

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(content_fixed)

print("Saved updated dashboard.html!")
