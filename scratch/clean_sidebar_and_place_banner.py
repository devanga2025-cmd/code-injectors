with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the messy dashboard sidebar item with the correct clean item
target_sidebar_item = """          <!-- 1. Dashboard -->
          <li class="nav-item">
            <a href="{% url 'dashboard' %}" class="nav-link-btn {% if active_tab == 'dashboard' %}"""

# Find from `<!-- 1. Dashboard -->` up to `<span class="nav-label">Dashboard</span>\n            </a>\n          </li>`
import re
pattern = r'[ \t]*<!-- 1\. Dashboard -->[\s\S]*?<span class="nav-label">Dashboard</span>\s*</a>\s*</li>'

clean_sidebar_item = '''          <!-- 1. Dashboard -->
          <li class="nav-item">
            <a href="{% url 'dashboard' %}" class="nav-link-btn {% if active_tab == 'dashboard' %}active{% endif %}">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7"></rect>
                <rect x="14" y="3" width="7" height="7"></rect>
                <rect x="14" y="14" width="7" height="7"></rect>
                <rect x="3" y="14" width="7" height="7"></rect>
              </svg>
              <span class="nav-label">Dashboard</span>
            </a>
          </li>'''

text = re.sub(pattern, clean_sidebar_item, text, count=1)

# Now check if the full Solution Banner is inside the body
full_banner = '''          <!-- CODESHIELD AI SOLUTION & KEY FEATURES HERO BANNER -->
          <div class="codeshield-solution-banner" id="codeshieldSolutionBanner">
            <div class="solution-header-row">
              <div class="solution-title-block">
                <div class="solution-badge">
                  <span class="solution-badge-dot"></span>
                  <span>Active Remediation Platform</span>
                </div>
                <h2 class="solution-title">CodeShield AI Solution</h2>
                <p class="solution-mission">
                  Automatically scan GitHub repositories using security tools to detect vulnerabilities, exposed secrets, insecure code and dependency risks.
                </p>
              </div>
              <div class="solution-actions-block">
                <button type="button" class="btn-solution-scan" onclick="openNewScanModal()">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                  <span>Run Security Scan</span>
                </button>
                <a href="{% url 'dashboard_code' %}" class="btn-solution-secondary">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
                  <span>View Findings</span>
                </a>
              </div>
            </div>

            <!-- 5 KEY FEATURES GRID -->
            <div class="solution-features-label">
              <span class="feat-label-text">Key Features</span>
              <span class="feat-label-sub">Enterprise Continuous DevSecOps Capability</span>
            </div>
            <div class="solution-features-grid">
              <div class="solution-feature-card">
                <div class="feat-card-top">
                  <div class="feat-icon-wrap ai-purple">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 2a10 10 0 0 1 10 10"></path><path d="M12 12L2.5 7.5"></path></svg>
                  </div>
                  <span class="feat-badge">Root-Cause</span>
                </div>
                <div class="feat-card-title">AI-Powered Explanations</div>
                <div class="feat-card-desc">Contextual root-cause diagnostics, attack vector analysis, and business impact risk synthesis for every finding.</div>
              </div>

              <div class="solution-feature-card">
                <div class="feat-card-top">
                  <div class="feat-icon-wrap prio-orange">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  </div>
                  <span class="feat-badge">P0-P3 Triage</span>
                </div>
                <div class="feat-card-title">Risk Prioritisation</div>
                <div class="feat-card-desc">Deterministic severity categorization combined with call-graph reachability triage to focus on exploitable threats first.</div>
              </div>

              <div class="solution-feature-card">
                <div class="feat-card-top">
                  <div class="feat-icon-wrap fix-green">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
                  </div>
                  <span class="feat-badge">1-Click Diffs</span>
                </div>
                <div class="feat-card-title">Secure Fix Recommendations</div>
                <div class="feat-card-desc">Actionable, verified code patch diffs and syntax-safe replacement patterns tailored to your framework.</div>
              </div>

              <div class="solution-feature-card">
                <div class="feat-card-top">
                  <div class="feat-icon-wrap scan-blue">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                  </div>
                  <span class="feat-badge">Zero-Trust</span>
                </div>
                <div class="feat-card-title">Private Repository Scanning</div>
                <div class="feat-card-desc">Zero-trust inspection supporting private and public GitHub repos with ephemeral, token-encrypted cloning pipelines.</div>
              </div>

              <div class="solution-feature-card">
                <div class="feat-card-top">
                  <div class="feat-icon-wrap verify-teal">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                  </div>
                  <span class="feat-badge">Live Rescan</span>
                </div>
                <div class="feat-card-title">Rescanning to Verify Fixes</div>
                <div class="feat-card-desc">Immediate 1-click multi-engine re-audit to validate developer patches and automatically resolve findings.</div>
              </div>
            </div>
          </div>'''

# Remove any existing partial codeshieldSolutionBanner in body if present
text = re.sub(r'[ \t]*<!-- CODESHIELD AI SOLUTION & KEY FEATURES HERO BANNER -->[\s\S]*?</div>\s*</div>\s*</div>', '', text)
text = re.sub(r'[ \t]*<div class="codeshield-solution-banner"[\s\S]*?</div>\s*</div>\s*</div>', '', text)

# Insert the complete banner right after `{% if active_tab == 'dashboard' %}` in the main body
body_anchor = "<!-- TAB: DASHBOARD (MAIN OVERVIEW) -->\n        {% if active_tab == 'dashboard' %}"
if body_anchor in text:
    text = text.replace(body_anchor, body_anchor + "\n\n" + full_banner)
    print("Placed full banner into dashboard body anchor")
else:
    print("Could not find body anchor")

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Finished cleanup.")
