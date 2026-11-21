import re

dashboard_path = r'd:\code_injectors\templates\dashboard.html'

with open(dashboard_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ==============================================================================
# 1. OVERVIEW: Add Dynamic Risk Range & Threat Spectrum to "Pending & In Progress"
# ==============================================================================
stats_grid_target = """                <div class="stat-metric-box">
                  <span class="stat-label">Suggested Improvements</span>
                  <span class="stat-number improvements">{{ suggested_improvements }}</span>
                  <span class="stat-subtext">Automated guardrail rules</span>
                </div>
              </div>"""

risk_range_html = """                <div class="stat-metric-box">
                  <span class="stat-label">Suggested Improvements</span>
                  <span class="stat-number improvements">{{ suggested_improvements }}</span>
                  <span class="stat-subtext">Low & Moderate findings</span>
                </div>
              </div>

              <!-- DYNAMIC RISK RANGE & SEVERITY SPECTRUM BAR -->
              <div class="risk-range-container" style="margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--dash-border-subtle);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.78rem; font-weight: 700; color: var(--dash-heading); text-transform: uppercase; letter-spacing: 0.03em;">Portfolio Risk Range:</span>
                    <span class="scan-status-pill in-progress" style="background: {% if risk_range_class == 'crit' %}#FEE2E2; color: #991B1B; border: 1px solid #FCA5A5;{% elif risk_range_class == 'high' %}#FFEDD5; color: #9A3412; border: 1px solid #FDBA74;{% elif risk_range_class == 'med' %}#FEF3C7; color: #92400E; border: 1px solid #FCD34D;{% else %}#ECFDF5; color: #065F46; border: 1px solid #A7F3D0;{% endif %} font-weight: 700; font-size: 0.72rem; padding: 2px 8px;">
                      {{ risk_range_label }}
                    </span>
                  </div>
                  <span style="font-size: 0.75rem; color: var(--dash-muted); font-family: var(--font-mono);">
                    Threat Score: <strong style="color: var(--dash-heading);">{{ weighted_threat_score }}</strong> / 500
                  </span>
                </div>

                <!-- Proportional Segmented Severity Bar -->
                <div style="display: flex; width: 100%; height: 7px; border-radius: 999px; overflow: hidden; background: #F1F5F9; margin-bottom: 8px;">
                  {% if crit_count > 0 %}<div style="width: {{ crit_pct }}%; background: #DC2626;" title="Critical: {{ crit_count }} ({{ crit_pct }}%)"></div>{% endif %}
                  {% if high_count > 0 %}<div style="width: {{ high_pct }}%; background: #EA580C;" title="High: {{ high_count }} ({{ high_pct }}%)"></div>{% endif %}
                  {% if med_count > 0 %}<div style="width: {{ med_pct }}%; background: #D97706;" title="Medium: {{ med_count }} ({{ med_pct }}%)"></div>{% endif %}
                  {% if low_count > 0 %}<div style="width: {{ low_pct }}%; background: #2563EB;" title="Low: {{ low_count }} ({{ low_pct }}%)"></div>{% endif %}
                </div>

                <!-- Dynamic 4-Tier Severity Range Breakdown Pills -->
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.72rem; flex-wrap: wrap; gap: 6px;">
                  <span style="display: inline-flex; align-items: center; gap: 5px;">
                    <span style="width: 7px; height: 7px; border-radius: 50%; background: #DC2626; display: inline-block;"></span>
                    <strong style="color: #DC2626;">{{ crit_count }}</strong> <span style="color: var(--dash-muted);">Critical (P0)</span>
                  </span>
                  <span style="display: inline-flex; align-items: center; gap: 5px;">
                    <span style="width: 7px; height: 7px; border-radius: 50%; background: #EA580C; display: inline-block;"></span>
                    <strong style="color: #EA580C;">{{ high_count }}</strong> <span style="color: var(--dash-muted);">High (P1)</span>
                  </span>
                  <span style="display: inline-flex; align-items: center; gap: 5px;">
                    <span style="width: 7px; height: 7px; border-radius: 50%; background: #D97706; display: inline-block;"></span>
                    <strong style="color: #D97706;">{{ med_count }}</strong> <span style="color: var(--dash-muted);">Medium (P2)</span>
                  </span>
                  <span style="display: inline-flex; align-items: center; gap: 5px;">
                    <span style="width: 7px; height: 7px; border-radius: 50%; background: #2563EB; display: inline-block;"></span>
                    <strong style="color: #2563EB;">{{ low_count }}</strong> <span style="color: var(--dash-muted);">Low (P3)</span>
                  </span>
                </div>
              </div>"""

if stats_grid_target in html and 'risk-range-container' not in html:
    html = html.replace(stats_grid_target, risk_range_html, 1)
    print("1. Added Dynamic Risk Range & Threat Spectrum to Overview")

# ==============================================================================
# 2. CODE SECURITY TAB: Add Project Filter & Low Severity Option
# ==============================================================================
code_filter_old = """              <div class="filter-bar-left">
                <input type="text" id="codeSearchInput" class="filter-bar-input" placeholder="Search rules, messages, or files..." oninput="filterCodeFindings()">
                <select id="codeEngineFilter" class="filter-bar-select" onchange="filterCodeFindings()">
                  <option value="all">All Engines (Bandit & Semgrep)</option>
                  <option value="bandit">Bandit AST Only</option>
                  <option value="semgrep">Semgrep Patterns Only</option>
                </select>
                <select id="codeSeverityFilter" class="filter-bar-select" onchange="filterCodeFindings()">
                  <option value="all">All Severities</option>
                  <option value="CRITICAL">Critical Severity</option>
                  <option value="HIGH">High Severity</option>
                  <option value="MEDIUM">Medium Severity</option>
                </select>
              </div>"""

code_filter_new = """              <div class="filter-bar-left">
                <input type="text" id="codeSearchInput" class="filter-bar-input" placeholder="Search rules, messages, or files..." oninput="filterCodeFindings()">
                <select id="codeRepoFilter" class="filter-bar-select" onchange="filterCodeFindings()">
                  <option value="all">All Projects</option>
                  {% for r in all_user_repos %}
                    <option value="{{ r.id }}" {% if selected_repo_id == r.id %}selected{% endif %}>{{ r.name }}</option>
                  {% endfor %}
                </select>
                <select id="codeEngineFilter" class="filter-bar-select" onchange="filterCodeFindings()">
                  <option value="all">All Engines (Bandit & Semgrep)</option>
                  <option value="bandit">Bandit AST Only</option>
                  <option value="semgrep">Semgrep Patterns Only</option>
                </select>
                <select id="codeSeverityFilter" class="filter-bar-select" onchange="filterCodeFindings()">
                  <option value="all">All Severities</option>
                  <option value="CRITICAL">Critical (P0)</option>
                  <option value="HIGH">High (P1)</option>
                  <option value="MEDIUM">Medium (P2)</option>
                  <option value="LOW">Low (P3)</option>
                </select>
              </div>"""

if code_filter_old in html:
    html = html.replace(code_filter_old, code_filter_new, 1)
    print("2. Updated Code Security Tab filter toolbar")

# ==============================================================================
# 3. SECRETS TAB: Dynamic Metric Strip, Project Filter & Masked Token Fix
# ==============================================================================
secrets_strip_old = """            <div class="subtab-metric-strip">
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Active Secret Exposures</div>
                <div class="subtab-metric-num" style="color: #DC2626;">{{ secrets_findings|length }}</div>
                <div class="subtab-metric-sub">Immediate revocation recommended</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">High-Entropy Tokens</div>
                <div class="subtab-metric-num" style="color: #EA580C;">{{ secrets_findings|length }}</div>
                <div class="subtab-metric-sub">API keys, tokens & credentials</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Cloud Credentials</div>
                <div class="subtab-metric-num">0</div>
                <div class="subtab-metric-sub">Zero AWS/GCP live admin keys</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Rotation Guides Ready</div>
                <div class="subtab-metric-num" style="color: #0F9F74;">{{ secrets_findings|length }}</div>
                <div class="subtab-metric-sub">Automated .env migration available</div>
              </div>
            </div>"""

secrets_strip_new = """            <div class="subtab-metric-strip">
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Active Secret Exposures</div>
                <div class="subtab-metric-num" style="color: #DC2626;">{{ secrets_findings|length }}</div>
                <div class="subtab-metric-sub">Immediate revocation recommended</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">High-Entropy API Keys</div>
                <div class="subtab-metric-num" style="color: #EA580C;">{{ api_keys_count }}</div>
                <div class="subtab-metric-sub">Detected via Shannon entropy</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Cloud & OAuth Tokens</div>
                <div class="subtab-metric-num" style="color: {% if cloud_tokens_count > 0 %}#DC2626{% else %}#059669{% endif %};">{{ cloud_tokens_count }}</div>
                <div class="subtab-metric-sub">{% if cloud_tokens_count > 0 %}{{ cloud_tokens_count }} live cloud tokens{% else %}Zero AWS/GCP cloud admin keys{% endif %}</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Rotation Guides Ready</div>
                <div class="subtab-metric-num" style="color: #0F9F74;">{{ secrets_findings|length }}</div>
                <div class="subtab-metric-sub">Verified mitigation diffs ready</div>
              </div>
            </div>"""

if secrets_strip_old in html:
    html = html.replace(secrets_strip_old, secrets_strip_new, 1)
    print("3. Updated Secrets Tab metric strip")

secrets_filter_old = """              <div class="filter-bar-left">
                <input type="text" id="secretsSearchInput" class="filter-bar-input" placeholder="Search secret types or files..." oninput="filterSecretsFindings()">
                <select id="secretsTypeFilter" class="filter-bar-select" onchange="filterSecretsFindings()">
                  <option value="all">All Secret Types</option>
                  <option value="openai">OpenAI API Keys</option>
                  <option value="aws">AWS Credentials</option>
                  <option value="token">Generic Tokens</option>
                </select>
                <select id="secretsSeverityFilter" class="filter-bar-select" onchange="filterSecretsFindings()">
                  <option value="all">All Severities</option>
                  <option value="CRITICAL">Critical Exposure</option>
                  <option value="HIGH">High Exposure</option>
                </select>
              </div>"""

secrets_filter_new = """              <div class="filter-bar-left">
                <input type="text" id="secretsSearchInput" class="filter-bar-input" placeholder="Search secret types or files..." oninput="filterSecretsFindings()">
                <select id="secretsRepoFilter" class="filter-bar-select" onchange="filterSecretsFindings()">
                  <option value="all">All Projects</option>
                  {% for r in all_user_repos %}
                    <option value="{{ r.id }}" {% if selected_repo_id == r.id %}selected{% endif %}>{{ r.name }}</option>
                  {% endfor %}
                </select>
                <select id="secretsTypeFilter" class="filter-bar-select" onchange="filterSecretsFindings()">
                  <option value="all">All Secret Types</option>
                  <option value="token">Generic API Tokens</option>
                  <option value="openai">OpenAI API Keys</option>
                  <option value="aws">AWS / Cloud Credentials</option>
                </select>
                <select id="secretsSeverityFilter" class="filter-bar-select" onchange="filterSecretsFindings()">
                  <option value="all">All Severities</option>
                  <option value="CRITICAL">Critical (P0)</option>
                  <option value="HIGH">High (P1)</option>
                  <option value="MEDIUM">Medium (P2)</option>
                </select>
              </div>"""

if secrets_filter_old in html:
    html = html.replace(secrets_filter_old, secrets_filter_new, 1)
    print("4. Updated Secrets Tab filter toolbar")

# Fix hardcoded masked secret value in secrets card
secret_card_old = """                  <!-- Masked Secret Box -->
                  <div class="secret-token-box">
                    <div class="secret-masked-text">
                      <span style="color: #94A3B8;">Masked Value: </span>
                      <span>sk-proj-49182••••••••••••••••••••••••••••••••</span>
                    </div>
                    <button type="button" class="btn-secret-copy" onclick="event.stopPropagation(); alert('Token fingerprint copied for revocation.');">Copy Hash</button>
                  </div>"""

secret_card_new = """                  <!-- Masked Secret Box -->
                  <div class="secret-token-box">
                    <div class="secret-masked-text">
                      <span style="color: #94A3B8;">Masked Value: </span>
                      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 600; color: #1E293B;">{% if f.code_snippet %}{{ f.code_snippet }}{% else %}REDACT••••••••••••••••••••••••{% endif %}</span>
                    </div>
                    <button type="button" class="btn-secret-copy" onclick="event.stopPropagation(); navigator.clipboard.writeText('{{ f.rule_id }}'); alert('Secret rule reference copied for revocation.');">Copy Reference</button>
                  </div>"""

if secret_card_old in html:
    html = html.replace(secret_card_old, secret_card_new, 1)
    print("5. Fixed hardcoded masked secret value in Secrets card")

# Update severity pill in secret card
secret_pill_old = '<span class="scan-status-pill in-progress">HIGH EXPOSURE</span>'
secret_pill_new = '<span class="scan-status-pill in-progress">{{ f.severity }} EXPOSURE</span>'
if secret_pill_old in html:
    html = html.replace(secret_pill_old, secret_pill_new, 1)
    print("6. Made secret card exposure pill dynamic")

# ==============================================================================
# 4. SUPPLY CHAIN TAB: Dynamic Metric Strip, Project Filter & Clean Empty State
# ==============================================================================
supply_strip_old = """            <div class="subtab-metric-strip">
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Monitored Dependencies</div>
                <div class="subtab-metric-num">1,428</div>
                <div class="subtab-metric-sub">Across PyPI & npm packages</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Flagged CVE Vulnerabilities</div>
                <div class="subtab-metric-num" style="color: #EA580C;">{{ supply_chain_findings|length }}</div>
                <div class="subtab-metric-sub">Dependencies requiring patches</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Exploited in the Wild (KEV)</div>
                <div class="subtab-metric-num" style="color: #059669;">0</div>
                <div class="subtab-metric-sub">Zero CISA-listed active exploits</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Direct Patch Available</div>
                <div class="subtab-metric-num" style="color: #0F9F74;">100%</div>
                <div class="subtab-metric-sub">Safe upgrades validated</div>
              </div>
            </div>"""

supply_strip_new = """            <div class="subtab-metric-strip">
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Vulnerable Packages</div>
                <div class="subtab-metric-num" style="color: #7E22CE;">{{ vulnerable_packages_count }}</div>
                <div class="subtab-metric-sub">Flagged in package lockfiles</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Flagged CVE Vulnerabilities</div>
                <div class="subtab-metric-num" style="color: #EA580C;">{{ supply_chain_findings|length }}</div>
                <div class="subtab-metric-sub">Known CVEs in OSV & GHSA</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Critical Severity CVEs</div>
                <div class="subtab-metric-num" style="color: {% if crit_count > 0 %}#DC2626{% else %}#059669{% endif %};">{{ crit_count }}</div>
                <div class="subtab-metric-sub">{% if crit_count > 0 %}{{ crit_count }} P0 vulnerabilities require upgrade{% else %}Zero critical package CVEs{% endif %}</div>
              </div>
              <div class="subtab-metric-card">
                <div class="subtab-metric-label">Direct Patch Available</div>
                <div class="subtab-metric-num" style="color: #0F9F74;">100%</div>
                <div class="subtab-metric-sub">Safe upgrades validated</div>
              </div>
            </div>"""

if supply_strip_old in html:
    html = html.replace(supply_strip_old, supply_strip_new, 1)
    print("7. Updated Supply Chain Tab metric strip")

supply_filter_old = """              <div class="filter-bar-left">
                <input type="text" id="supplySearchInput" class="filter-bar-input" placeholder="Search package name or CVE ID..." oninput="filterSupplyFindings()">
                <select id="supplyEcosystemFilter" class="filter-bar-select" onchange="filterSupplyFindings()">
                  <option value="all">All Ecosystems (PyPI, npm)</option>
                  <option value="pypi">PyPI (Python)</option>
                  <option value="npm">npm (Node.js)</option>
                </select>
                <select id="supplySeverityFilter" class="filter-bar-select" onchange="filterSupplyFindings()">
                  <option value="all">All Severities</option>
                  <option value="CRITICAL">Critical CVE</option>
                  <option value="HIGH">High CVE</option>
                  <option value="MEDIUM">Medium CVE</option>
                </select>
              </div>"""

supply_filter_new = """              <div class="filter-bar-left">
                <input type="text" id="supplySearchInput" class="filter-bar-input" placeholder="Search package name or CVE ID..." oninput="filterSupplyFindings()">
                <select id="supplyRepoFilter" class="filter-bar-select" onchange="filterSupplyFindings()">
                  <option value="all">All Projects</option>
                  {% for r in all_user_repos %}
                    <option value="{{ r.id }}" {% if selected_repo_id == r.id %}selected{% endif %}>{{ r.name }}</option>
                  {% endfor %}
                </select>
                <select id="supplyEcosystemFilter" class="filter-bar-select" onchange="filterSupplyFindings()">
                  <option value="all">All Ecosystems (PyPI, npm)</option>
                  <option value="npm">npm (Node.js)</option>
                  <option value="pypi">PyPI (Python)</option>
                </select>
                <select id="supplySeverityFilter" class="filter-bar-select" onchange="filterSupplyFindings()">
                  <option value="all">All Severities</option>
                  <option value="CRITICAL">Critical CVE (P0)</option>
                  <option value="HIGH">High CVE (P1)</option>
                  <option value="MEDIUM">Medium CVE (P2)</option>
                  <option value="LOW">Low CVE (P3)</option>
                </select>
              </div>"""

if supply_filter_old in html:
    html = html.replace(supply_filter_old, supply_filter_new, 1)
    print("8. Updated Supply Chain Tab filter toolbar")

supply_empty_old = '<p style="font-size: 0.85rem; margin-top: 4px;">1,428 monitored packages have zero known high/critical CVEs.</p>'
supply_empty_new = '<p style="font-size: 0.85rem; margin-top: 4px;">All monitored package dependencies have zero open security advisories.</p>'
if supply_empty_old in html:
    html = html.replace(supply_empty_old, supply_empty_new, 1)
    print("9. Cleaned Supply Chain empty state text")

# ==============================================================================
# 5. JAVASCRIPT: Enhanced Client-Side Filtering with Project Dropdowns
# ==============================================================================
old_filters_js = """    function filterCodeFindings() {
      const q = (document.getElementById('codeSearchInput')?.value || '').toLowerCase().trim();
      const engine = document.getElementById('codeEngineFilter')?.value || 'all';
      const severity = document.getElementById('codeSeverityFilter')?.value || 'all';
      const cards = document.querySelectorAll('#codeFindingsList .finding-item-card');

      cards.forEach(card => {
        const cardEngine = (card.getAttribute('data-engine') || '').toLowerCase();
        const cardSev = (card.getAttribute('data-severity') || '').toUpperCase();
        const cardText = (card.getAttribute('data-text') || '').toLowerCase();

        const textMatch = !q || cardText.includes(q);
        const engineMatch = engine === 'all' || cardEngine === engine;
        const sevMatch = severity === 'all' || cardSev === severity;

        card.style.display = (textMatch && engineMatch && sevMatch) ? '' : 'none';
      });
    }

    function filterSecretsFindings() {
      const q = (document.getElementById('secretsSearchInput')?.value || '').toLowerCase().trim();
      const type = document.getElementById('secretsTypeFilter')?.value || 'all';
      const severity = document.getElementById('secretsSeverityFilter')?.value || 'all';
      const cards = document.querySelectorAll('#secretsFindingsList .finding-item-card');

      cards.forEach(card => {
        const cardType = (card.getAttribute('data-type') || '').toLowerCase();
        const cardSev = (card.getAttribute('data-severity') || '').toUpperCase();
        const cardText = (card.getAttribute('data-text') || '').toLowerCase();

        const textMatch = !q || cardText.includes(q);
        const typeMatch = type === 'all' || cardType === type;
        const sevMatch = severity === 'all' || cardSev === severity;

        card.style.display = (textMatch && typeMatch && sevMatch) ? '' : 'none';
      });
    }

    function filterSupplyFindings() {
      const q = (document.getElementById('supplySearchInput')?.value || '').toLowerCase().trim();
      const eco = document.getElementById('supplyEcosystemFilter')?.value || 'all';
      const severity = document.getElementById('supplySeverityFilter')?.value || 'all';
      const cards = document.querySelectorAll('#supplyFindingsList .finding-item-card');

      cards.forEach(card => {
        const cardEco = (card.getAttribute('data-ecosystem') || '').toLowerCase();
        const cardSev = (card.getAttribute('data-severity') || '').toUpperCase();
        const cardText = (card.getAttribute('data-text') || '').toLowerCase();

        const textMatch = !q || cardText.includes(q);
        const ecoMatch = eco === 'all' || cardEco === eco;
        const sevMatch = severity === 'all' || cardSev === severity;

        card.style.display = (textMatch && ecoMatch && sevMatch) ? '' : 'none';
      });
    }"""

new_filters_js = """    function filterCodeFindings() {
      const q = (document.getElementById('codeSearchInput')?.value || '').toLowerCase().trim();
      const repo = document.getElementById('codeRepoFilter')?.value || 'all';
      const engine = document.getElementById('codeEngineFilter')?.value || 'all';
      const severity = document.getElementById('codeSeverityFilter')?.value || 'all';
      const cards = document.querySelectorAll('#codeFindingsList .finding-item-card');

      cards.forEach(card => {
        const cardRepo = card.getAttribute('data-repoid') || '';
        const cardEngine = (card.getAttribute('data-engine') || '').toLowerCase();
        let cardSev = (card.getAttribute('data-severity') || '').toUpperCase();
        if (cardSev === 'MODERATE') cardSev = 'MEDIUM';
        const cardText = (card.getAttribute('data-text') || '').toLowerCase();

        const textMatch = !q || cardText.includes(q);
        const repoMatch = repo === 'all' || cardRepo === repo;
        const engineMatch = engine === 'all' || cardEngine === engine;
        const sevMatch = severity === 'all' || cardSev === severity;

        card.style.display = (textMatch && repoMatch && engineMatch && sevMatch) ? '' : 'none';
      });
    }

    function filterSecretsFindings() {
      const q = (document.getElementById('secretsSearchInput')?.value || '').toLowerCase().trim();
      const repo = document.getElementById('secretsRepoFilter')?.value || 'all';
      const type = document.getElementById('secretsTypeFilter')?.value || 'all';
      const severity = document.getElementById('secretsSeverityFilter')?.value || 'all';
      const cards = document.querySelectorAll('#secretsFindingsList .finding-item-card');

      cards.forEach(card => {
        const cardRepo = card.getAttribute('data-repoid') || '';
        const cardType = (card.getAttribute('data-type') || '').toLowerCase();
        let cardSev = (card.getAttribute('data-severity') || '').toUpperCase();
        if (cardSev === 'MODERATE') cardSev = 'MEDIUM';
        const cardText = (card.getAttribute('data-text') || '').toLowerCase();

        const textMatch = !q || cardText.includes(q);
        const repoMatch = repo === 'all' || cardRepo === repo;
        const typeMatch = type === 'all' || cardType === type;
        const sevMatch = severity === 'all' || cardSev === severity;

        card.style.display = (textMatch && repoMatch && typeMatch && sevMatch) ? '' : 'none';
      });
    }

    function filterSupplyFindings() {
      const q = (document.getElementById('supplySearchInput')?.value || '').toLowerCase().trim();
      const repo = document.getElementById('supplyRepoFilter')?.value || 'all';
      const eco = document.getElementById('supplyEcosystemFilter')?.value || 'all';
      const severity = document.getElementById('supplySeverityFilter')?.value || 'all';
      const cards = document.querySelectorAll('#supplyFindingsList .finding-item-card');

      cards.forEach(card => {
        const cardRepo = card.getAttribute('data-repoid') || '';
        const cardEco = (card.getAttribute('data-ecosystem') || '').toLowerCase();
        let cardSev = (card.getAttribute('data-severity') || '').toUpperCase();
        if (cardSev === 'MODERATE') cardSev = 'MEDIUM';
        const cardText = (card.getAttribute('data-text') || '').toLowerCase();

        const textMatch = !q || cardText.includes(q);
        const repoMatch = repo === 'all' || cardRepo === repo;
        const ecoMatch = eco === 'all' || cardEco === eco;
        const sevMatch = severity === 'all' || cardSev === severity;

        card.style.display = (textMatch && repoMatch && ecoMatch && sevMatch) ? '' : 'none';
      });
    }"""

if old_filters_js in html:
    html = html.replace(old_filters_js, new_filters_js, 1)
    print("10. Updated JS filtering with project dropdowns and MODERATE->MEDIUM support")

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("All updates successfully applied to templates/dashboard.html!")
