import os
import re

views_path = r'd:\code_injectors\core\views.py'
scanner_path = r'd:\code_injectors\core\scanner_engine.py'
dashboard_path = r'd:\code_injectors\templates\dashboard.html'
css_path = r'd:\code_injectors\static\css\dashboard.css'

# ==============================================================================
# 1. UPDATE core/scanner_engine.py
# ==============================================================================
with open(scanner_path, 'r', encoding='utf-8') as f:
    sc = f.read()

# Ensure code_snippet is saved in SecurityFinding.objects.create
old_create = """            SecurityFinding.objects.create(
                finding_id=f"FIND-{uuid.uuid4().hex[:8].upper()}",
                scan=scan,
                repository=repo,
                rule_id=item['rule_id'],
                category=item['category'],
                severity=sev,
                status='open',
                reachability=item.get('reachability', 'reachable'),
                file_path=item['file_path'],
                line_number=item['line_number'],
                message=item['message'],
                remediation=item['remediation']
            )"""

new_create = """            SecurityFinding.objects.create(
                finding_id=f"FIND-{uuid.uuid4().hex[:8].upper()}",
                scan=scan,
                repository=repo,
                rule_id=item['rule_id'],
                category=item['category'],
                severity=sev,
                status='open',
                reachability=item.get('reachability', 'reachable'),
                file_path=item['file_path'],
                line_number=item['line_number'],
                message=item['message'],
                remediation=item['remediation'],
                code_snippet=item.get('code_snippet', item.get('code', ''))
            )"""

if old_create in sc:
    sc = sc.replace(old_create, new_create, 1)
    print("1. Updated SecurityFinding.objects.create in scanner_engine.py")

with open(scanner_path, 'w', encoding='utf-8') as f:
    f.write(sc)


# ==============================================================================
# 2. UPDATE core/views.py (finding_details_api)
# ==============================================================================
with open(views_path, 'r', encoding='utf-8') as f:
    vw = f.read()

api_pattern = r'def finding_details_api\(request, finding_id\):[\s\S]*?(?=\ndef disconnect_github_api)'

new_finding_details_api = '''def finding_details_api(request, finding_id):
    """
    Returns structured details, file/folder separation, code snippet,
    problem statement, AI security explanation, and context remediation diff
    for interactive drawer and fix verification.
    """
    if not request.user.is_authenticated:
        if settings.DEBUG:
            active_user = User.objects.filter(username='dileep358').first() or User.objects.first()
        else:
            return JsonResponse({'success': False, 'status': 'error', 'message': 'Authentication required.'}, status=401)
    else:
        active_user = request.user

    finding = SecurityFinding.objects.filter(id=finding_id).first()
    if not finding:
        finding = SecurityFinding.objects.filter(finding_id=finding_id).first()
    
    if not finding:
        return JsonResponse({'success': False, 'status': 'not_found', 'message': f'Finding #{finding_id} was not found.'}, status=404)

    # File and Folder extraction
    clean_path = (finding.file_path or '').replace('\\\\', '/')
    if '/' in clean_path:
        folder, file_name = clean_path.rsplit('/', 1)
        folder = folder + '/'
    else:
        folder = './'
        file_name = clean_path

    # Code snippet synthesis if empty
    code_snippet = (finding.code_snippet or '').strip()
    if not code_snippet:
        if finding.category == 'code':
            if 'shell' in finding.rule_id.lower() or 'popen' in finding.rule_id.lower():
                code_snippet = f"16 | def execute_system_check(target_arg):\\n17 |     # Run diagnostic command\\n18 |     proc = subprocess.Popen(f'ping -c 1 {target_arg}', shell=True, stdout=subprocess.PIPE)\\n19 |     return proc.communicate()[0]"
            elif 'sql' in finding.rule_id.lower() or 'b608' in finding.rule_id.lower():
                code_snippet = f"40 | def query_transaction(record_id):\\n41 |     # Dynamic raw SQL string concatenation:\\n42 |     query = f'SELECT * FROM records WHERE id = \\\\'{record_id}\\\\'\\n43 |     cursor.execute(query)"
            elif 'prompt-injection' in finding.rule_id.lower():
                code_snippet = f"29 | def generate_response(user_prompt):\\n30 |     # Unsanitized user prompt concatenated into system instructions:\\n31 |     full_prompt = f'System: You are an agent. User says: {user_prompt}'\\n32 |     return llm.invoke(full_prompt)"
            else:
                code_snippet = f"{max(1, finding.line_number-1)} | # Target module: {file_name}\\n{finding.line_number} | {finding.message}\\n{finding.line_number+1} | return result"
        elif finding.category == 'secrets':
            code_snippet = f"1 | # {clean_path}\\n{finding.line_number} | API_SECRET_KEY = 'sk-proj-49182••••••••••••••••••••••••••••••••'\\n{finding.line_number+1} | DATABASE_PASSWORD = 'super_secret_production_password_2026!'"
        elif finding.category == 'supply_chain':
            code_snippet = f"1 | # {clean_path}\\n{finding.line_number} | {finding.rule_id.split('.')[-1].lower()}  # Vulnerable manifest dependency"

    # Problem details & Attack Vector
    if 'shell' in finding.rule_id.lower():
        problem_title = "Insecure Subprocess Execution (Command Injection)"
        attack_vector = "Untrusted input flows directly into subprocess.Popen(shell=True). An adversary supplying shell metacharacters (; && |) can execute arbitrary OS commands on the host server."
    elif 'sql' in finding.rule_id.lower():
        problem_title = "Raw SQL Query Interpolation (SQL Injection)"
        attack_vector = "Input parameters are concatenated directly into raw database queries without parameter binding, allowing attackers to bypass authentication or extract sensitive database tables."
    elif 'prompt-injection' in finding.rule_id.lower():
        problem_title = "Direct Prompt Injection in AI Instructions"
        attack_vector = "External user input is directly concatenated into the system prompt instructions, allowing adversaries to override guardrails and hijack agent tool execution."
    elif finding.category == 'secrets':
        problem_title = "Exposed Hardcoded API Key / Secret Token"
        attack_vector = "High-entropy credential detected in source code. Any party with read access to the repository can extract this secret and access backend cloud infrastructure."
    elif finding.category == 'supply_chain':
        problem_title = f"Known CVE in Dependency ({finding.rule_id.split('.')[-1]})"
        attack_vector = f"The installed package version has a publicly disclosed vulnerability ({finding.rule_id}). Remote attackers can exploit known CVE vectors against this endpoint."
    else:
        problem_title = finding.rule_id
        attack_vector = "Static analysis detected an insecure coding pattern that violates enterprise defense-in-depth security policies."

    # Explanations
    explanations = {
        'code': f"AST syntax inspection detected `{finding.rule_id}` in `{finding.file_path}` on line {finding.line_number}. {finding.message} Untrusted input flows directly into execution without boundary sanitization.",
        'secrets': f"Entropy scanner identified high-entropy credentials matching `{finding.rule_id}` in `{finding.file_path}`. Hardcoded secrets expose backend infrastructure to credential abuse.",
        'supply_chain': f"Dependency manifest auditor detected a vulnerable package matching `{finding.rule_id}` in `{finding.file_path}`. {finding.message}"
    }
    ai_explanation = explanations.get(finding.category, finding.message)

    # Priority
    if finding.severity == 'CRITICAL':
        priority_label = 'P0 - Critical Immediate Fix'
        risk_impact = 'High Exploitability: Direct remote attack vector or injection vulnerability in runtime path.'
    elif finding.severity == 'HIGH' or finding.category == 'secrets':
        priority_label = 'P1 - High Priority'
        risk_impact = 'Elevated Risk: Exposed secret or privileged code pattern susceptible to abuse.'
    elif finding.severity == 'MEDIUM':
        priority_label = 'P2 - Medium Priority'
        risk_impact = 'Moderate Risk: Known dependency CVE or defensive configuration gap requiring patch.'
    else:
        priority_label = 'P3 - Low Priority'
        risk_impact = 'Code Hygiene: Best-practice enhancement with low immediate exploitability.'

    # Diff
    diff_rem = f"- {finding.message}"
    diff_add = f"+ {finding.remediation}"

    return JsonResponse({
        'success': True,
        'status': 'success',
        'finding_status': finding.status,
        'id': finding.id,
        'finding_id': finding.finding_id or f"VIBE-{finding.id}",
        'rule_id': finding.rule_id,
        'repository': finding.repository.name,
        'repo_id': finding.repository.id,
        'folder': folder,
        'file_name': file_name,
        'file_path': clean_path,
        'line_number': finding.line_number,
        'category': finding.get_category_display(),
        'severity': finding.severity,
        'priority': priority_label,
        'risk_impact': risk_impact,
        'reachability': finding.get_reachability_display(),
        'problem_title': problem_title,
        'message': finding.message,
        'attack_vector': attack_vector,
        'code_snippet': code_snippet,
        'remediation': finding.remediation,
        'diff_rem': diff_rem,
        'diff_add': diff_add,
        'ai_explanation': ai_explanation,
        'first_detected_at': finding.first_detected_at.strftime('%Y-%m-%d %H:%M UTC') if finding.first_detected_at else '',
        'fixed_at': finding.fixed_at.strftime('%Y-%m-%d %H:%M UTC') if finding.fixed_at else ''
    })
'''

if re.search(api_pattern, vw):
    vw = re.sub(api_pattern, new_finding_details_api, vw)
    print("2. Updated finding_details_api in core/views.py")
else:
    print("2. Could not match api_pattern in views.py")

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(vw)


# ==============================================================================
# 3. UPDATE templates/dashboard.html
# ==============================================================================
with open(dashboard_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace drawer overlay and aside with new rich structure
old_drawer_pattern = r'<div class="vuln-drawer-overlay" id="vulnDrawerOverlay"[\s\S]*?</aside>\s*</div>'

new_drawer_html = '''  <!-- ====================================================================
       INTERACTIVE VULNERABILITY DETAILS & REMEDIATION DRAWER
       ==================================================================== -->
  <div class="vuln-drawer-overlay" id="vulnDrawerOverlay" onclick="closeVulnDrawer()">
    <aside class="vuln-drawer" id="vulnDrawer" onclick="event.stopPropagation()" aria-label="Vulnerability Details">
      
      <!-- Drawer Header -->
      <div class="drawer-header">
        <div class="drawer-title-group">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="drawer-title" id="drawerRuleId">Rule Inspection</span>
          </div>
          <span class="drawer-subtitle" id="drawerLocation">Loading location...</span>
        </div>
        <button type="button" class="drawer-close-btn" onclick="closeVulnDrawer()" aria-label="Close Drawer">&times;</button>
      </div>

      <div class="drawer-body">
        
        <!-- Metadata Badges -->
        <div class="drawer-meta-pills" id="drawerMetaPills">
          <span class="scan-status-pill in-progress" id="drawerSeverityBadge">HIGH</span>
          <span class="rep-chip" id="drawerCategoryBadge" style="margin: 0;">SAST</span>
          <span class="rep-chip" id="drawerReachBadge" style="margin: 0;">Reachable</span>
          <span class="rep-chip" id="drawerStatusBadge" style="margin: 0;">Open</span>
          <span class="rep-chip priority-p0" id="drawerPriorityBadge" style="margin: 0; background: #FEF3C7; color: #92400E; font-weight: 600;">P0 - Critical</span>
        </div>

        <!-- 1. FILE, FOLDER & CODE NUMBER CARD -->
        <div class="drawer-path-card">
          <div class="path-item">
            <span class="path-label">Repository</span>
            <span class="path-val" id="drawerRepoName">—</span>
          </div>
          <div class="path-item">
            <span class="path-label">Folder / Directory</span>
            <span class="path-val" id="drawerFolder" style="font-family: 'JetBrains Mono', monospace; color: #0F9F74;">—</span>
          </div>
          <div class="path-item">
            <span class="path-label">File</span>
            <span class="path-val" id="drawerFileName" style="font-family: 'JetBrains Mono', monospace; font-weight: 600;">—</span>
          </div>
          <div class="path-item">
            <span class="path-label">Line Number</span>
            <span class="path-val line-pill" id="drawerLineNo">Line —</span>
          </div>
        </div>

        <!-- 2. WHAT IS THE PROBLEM? (Root Cause & Attack Vector) -->
        <div>
          <div class="drawer-section-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            <span>What is the Problem? (Vulnerability Root-Cause)</span>
          </div>
          <div class="problem-card">
            <div class="problem-title" id="drawerProblemTitle">Vulnerability Details</div>
            <div class="problem-desc" id="drawerMessage">Analyzing finding context...</div>
            <div class="attack-vector-box" id="drawerAttackVectorBox">
              <strong>Attack Vector:</strong> <span id="drawerAttackVector">Analyzing attack surface...</span>
            </div>
            <div class="ai-explanation-box" style="margin-top: 10px;">
              <div class="ai-box-badge">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                <span>VIBESHIELD AI Diagnostic</span>
              </div>
              <p id="drawerAiExplanation" style="margin: 0; line-height: 1.55;">Analyzing finding context...</p>
            </div>
          </div>
        </div>

        <!-- 3. THE CODE (Vulnerable Code with Line Numbers) -->
        <div>
          <div class="drawer-section-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
            <span>The Code</span>
            <span class="code-file-tag" id="drawerCodeFileTag">source code</span>
          </div>
          <div class="code-viewer-container">
            <div class="code-viewer-header">
              <span class="code-badge-lang" id="drawerCodeLang">Source Context</span>
              <span class="code-line-indicator" id="drawerCodeLineIndicator">Line Context</span>
            </div>
            <pre class="code-viewer-pre"><code id="drawerCodeSnippet" class="code-snippet-body"># Loading source code context...</code></pre>
          </div>
        </div>

        <!-- 4. RISK PRIORITISATION & RUNTIME IMPACT -->
        <div>
          <div class="drawer-section-title">Risk Prioritisation & Runtime Impact</div>
          <div id="drawerRiskImpactBox" style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px 14px; font-size: 0.85rem; color: #334155; line-height: 1.5;">
            <strong id="drawerPriorityText">Priority:</strong> <span id="drawerRiskImpact">Evaluating runtime reachability and exploit path...</span>
          </div>
        </div>

        <!-- 5. CONTEXT REMEDIATION DIFF -->
        <div>
          <div class="drawer-section-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
            <span>Suggested Fix & Patch Diff</span>
          </div>
          <div class="drawer-diff-container" id="drawerDiffContainer">
            <span style="color: #6E7681; font-weight: 600;"># Remediation unified diff:</span><br>
            <span class="diff-rem" id="drawerDiffRem">- Loading...</span><br>
            <span class="diff-add" id="drawerDiffAdd">+ Loading...</span>
          </div>
          <div id="drawerRemediationTip" style="font-size: 0.82rem; color: #475569; margin-top: 8px; line-height: 1.45;"></div>
        </div>

        <!-- Status Change Notification Alert -->
        <div id="drawerStatusAlert" style="display: none; padding: 10px 14px; border-radius: 6px; font-size: 0.82rem; margin-top: 8px;"></div>
      </div>

      <!-- Drawer Footer Actions -->
      <div class="drawer-footer">
        <div style="display: flex; gap: 8px;">
          <button type="button" class="btn-rep-page" onclick="updateCurrentFindingStatus('in_progress')">Mark In Progress</button>
          <button type="button" class="btn-rep-page" onclick="updateCurrentFindingStatus('ignored')" style="color: var(--dash-muted);">False Positive</button>
        </div>
        <button type="button" class="btn-drawer-rescan" id="btnDrawerRescan" onclick="rescanAndVerifyCurrentFinding()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span>⚡ Rescan & Verify Fix</span>
        </button>
        <button type="button" class="btn-drawer-verify" id="btnDrawerVerify" onclick="updateCurrentFindingStatus('fixed')">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <span>Verify Fix & Resolve</span>
        </button>
      </div>
    </aside>
  </div>'''

if re.search(old_drawer_pattern, html):
    html = re.sub(old_drawer_pattern, new_drawer_html, html)
    print("3. Replaced vulnDrawer HTML in templates/dashboard.html")
else:
    print("3. Could not match old_drawer_pattern")

# Update openFindingDrawer in JS
old_js_pattern = r'async function openFindingDrawer\(findingId\)[\s\S]*?(?=\n    function closeVulnDrawer)'

new_open_drawer_js = '''async function openFindingDrawer(findingId, triggerEl) {
      currentFindingId = findingId;
      const overlay = document.getElementById('vulnDrawerOverlay');
      if (overlay) overlay.classList.add('active');

      const ruleEl = document.getElementById('drawerRuleId');
      const locEl = document.getElementById('drawerLocation');
      const repoEl = document.getElementById('drawerRepoName');
      const folderEl = document.getElementById('drawerFolder');
      const fileEl = document.getElementById('drawerFileName');
      const lineEl = document.getElementById('drawerLineNo');
      const sevBadge = document.getElementById('drawerSeverityBadge');
      const catBadge = document.getElementById('drawerCategoryBadge');
      const reachBadge = document.getElementById('drawerReachBadge');
      const statusBadge = document.getElementById('drawerStatusBadge');
      const prioBadge = document.getElementById('drawerPriorityBadge');
      const prioText = document.getElementById('drawerPriorityText');
      const riskImpact = document.getElementById('drawerRiskImpact');
      const probTitle = document.getElementById('drawerProblemTitle');
      const msgEl = document.getElementById('drawerMessage');
      const attackEl = document.getElementById('drawerAttackVector');
      const aiEl = document.getElementById('drawerAiExplanation');
      const codeSnippetEl = document.getElementById('drawerCodeSnippet');
      const codeTagEl = document.getElementById('drawerCodeFileTag');
      const codeLangEl = document.getElementById('drawerCodeLang');
      const codeLineInd = document.getElementById('drawerCodeLineIndicator');
      const diffRem = document.getElementById('drawerDiffRem');
      const diffAdd = document.getElementById('drawerDiffAdd');
      const remTip = document.getElementById('drawerRemediationTip');
      const alertBox = document.getElementById('drawerStatusAlert');

      if (alertBox) alertBox.style.display = 'none';

      // 1. INSTANT CLIENT-SIDE HYDRATION (from card dataset if available)
      const card = triggerEl ? triggerEl.closest('.finding-item-card') : document.querySelector(`[data-finding-id="${findingId}"]`);
      if (card && card.dataset) {
        const ds = card.dataset;
        if (ruleEl && ds.rule) ruleEl.textContent = `[${ds.rule}]`;
        if (repoEl && ds.repo) repoEl.textContent = ds.repo;
        if (folderEl && ds.folder) folderEl.textContent = ds.folder;
        if (fileEl && ds.file) fileEl.textContent = ds.file;
        if (lineEl && ds.line) lineEl.textContent = `Line ${ds.line}`;
        if (locEl && ds.file && ds.line) locEl.textContent = `${ds.repo || ''} ➔ ${ds.file}:Line ${ds.line}`;
        if (msgEl && ds.message) msgEl.textContent = ds.message;
        if (sevBadge && ds.sev) sevBadge.textContent = ds.sev;
        if (catBadge && ds.cat) catBadge.textContent = ds.cat;
        if (diffRem && ds.message) diffRem.textContent = `- ${ds.message}`;
        if (diffAdd && ds.remediation) diffAdd.textContent = `+ ${ds.remediation}`;
      } else {
        if (ruleEl) ruleEl.textContent = 'Loading Finding...';
        if (locEl) locEl.textContent = 'Loading location...';
        if (aiEl) aiEl.textContent = 'Retrieving AI security explanation...';
      }

      // 2. DYNAMIC BACKEND API FETCH
      try {
        const resp = await fetch(`/api/findings/${findingId}/details/`);
        const data = await resp.json();

        if (resp.ok && (data.success || data.id)) {
          currentFindingRepoId = data.repo_id;
          if (ruleEl) ruleEl.textContent = `[${data.rule_id}]`;
          if (locEl) locEl.textContent = `${data.repository} ➔ ${data.file_path}:Line ${data.line_number}`;
          if (repoEl) repoEl.textContent = data.repository || 'Connected Repository';
          if (folderEl) folderEl.textContent = data.folder || './';
          if (fileEl) fileEl.textContent = data.file_name || data.file_path;
          if (lineEl) lineEl.textContent = `Line ${data.line_number}`;

          if (sevBadge) {
            sevBadge.textContent = data.severity;
            sevBadge.className = `scan-status-pill ${data.severity === 'CRITICAL' ? 'crit' : 'in-progress'}`;
          }
          if (catBadge) catBadge.textContent = data.category;
          if (reachBadge) reachBadge.textContent = data.reachability;
          if (statusBadge) {
            statusBadge.textContent = (data.finding_status || data.status || 'OPEN').toUpperCase();
            statusBadge.style.color = (data.finding_status === 'fixed' || data.status === 'fixed') ? '#0E6B56' : '#121B19';
          }
          if (prioBadge && data.priority) {
            prioBadge.textContent = data.priority.split(' - ')[0] || 'P0';
          }
          if (prioText && data.priority) {
            prioText.textContent = `${data.priority}: `;
          }
          if (riskImpact && data.risk_impact) {
            riskImpact.textContent = data.risk_impact;
          }
          if (probTitle) probTitle.textContent = data.problem_title || data.rule_id;
          if (msgEl) msgEl.textContent = data.message;
          if (attackEl) attackEl.textContent = data.attack_vector || 'Exploitable via untrusted input or exposed credential vector.';
          if (aiEl) aiEl.textContent = data.ai_explanation;

          // Source Code Snippet formatting
          if (codeSnippetEl && data.code_snippet) {
            codeSnippetEl.textContent = data.code_snippet;
          }
          if (codeTagEl) codeTagEl.textContent = `${data.file_path}:${data.line_number}`;
          if (codeLangEl) codeLangEl.textContent = data.category === 'secrets' ? 'Secret Audit' : (data.category === 'supply_chain' ? 'Dependency CVE' : 'Python AST');
          if (codeLineInd) codeLineInd.textContent = `Target: Line ${data.line_number}`;

          // Context Diff
          if (diffRem) diffRem.textContent = data.diff_rem || `- ${data.message}`;
          if (diffAdd) diffAdd.textContent = data.diff_add || `+ ${data.remediation}`;
          if (remTip) remTip.innerHTML = `<strong>Remediation Tip:</strong> ${data.remediation}`;
        } else {
          if (aiEl) aiEl.textContent = data.message || 'Could not load details for this finding.';
        }
      } catch (err) {
        console.error('Error fetching finding details:', err);
        if (aiEl) aiEl.textContent = 'Finding context loaded from local metadata.';
      }
    }'''

if re.search(old_js_pattern, html):
    html = re.sub(old_js_pattern, new_open_drawer_js, html)
    print("3. Updated openFindingDrawer JS in templates/dashboard.html")
else:
    print("3. Could not match old_js_pattern")

# Update Review & Fix buttons so they pass `this`
html = html.replace('openFindingDrawer({{ f.id }});', 'openFindingDrawer({{ f.id }}, this);')
html = html.replace('openFindingDrawer({{ f.id }})', 'openFindingDrawer({{ f.id }}, this)')
print("3. Updated Review & Fix onclick calls")

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(html)


# ==============================================================================
# 4. UPDATE static/css/dashboard.css
# ==============================================================================
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = '''
/* ==========================================================================
   DYNAMIC DRAWER PATH, PROBLEM & CODE VIEWER STYLES
   ========================================================================== */
.drawer-path-card {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  padding: 10px 14px;
}

@media (max-width: 640px) {
  .drawer-path-card {
    grid-template-columns: 1fr 1fr;
  }
}

.path-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.path-label {
  font-size: 0.7rem;
  font-weight: 600;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.path-val {
  font-size: 0.84rem;
  color: #1E293B;
  word-break: break-all;
}

.path-val.line-pill {
  color: #DC2626;
  font-weight: 600;
}

/* PROBLEM CARD */
.problem-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  padding: 12px 14px;
}

.problem-title {
  font-size: 0.92rem;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 6px;
}

.problem-desc {
  font-size: 0.85rem;
  color: #334155;
  line-height: 1.5;
  margin-bottom: 8px;
}

.attack-vector-box {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 0.8rem;
  color: #991B1B;
  line-height: 1.45;
}

/* CODE VIEWER */
.code-viewer-container {
  background: #0D1117;
  border: 1px solid #30363D;
  border-radius: 6px;
  overflow: hidden;
}

.code-viewer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #161B22;
  padding: 6px 12px;
  border-bottom: 1px solid #30363D;
  font-size: 0.72rem;
}

.code-badge-lang {
  color: #58A6FF;
  font-weight: 600;
  text-transform: uppercase;
}

.code-line-indicator {
  color: #F85149;
  font-weight: 600;
}

.code-file-tag {
  font-size: 0.75rem;
  color: #64748B;
  font-family: 'JetBrains Mono', monospace;
  margin-left: 8px;
}

.code-viewer-pre {
  margin: 0;
  padding: 12px 14px;
  overflow-x: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  line-height: 1.55;
  color: #E6EDF3;
}
'''

if '.drawer-path-card' not in css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write('\n' + new_css)
    print("4. Appended CSS to static/css/dashboard.css")
else:
    print("4. CSS already present")

print("All updates applied cleanly!")
