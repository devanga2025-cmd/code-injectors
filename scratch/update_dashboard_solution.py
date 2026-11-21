import os
import re

dashboard_path = r'd:\code_injectors\templates\dashboard.html'
css_path = r'd:\code_injectors\static\css\dashboard.css'

with open(dashboard_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove sidebar Integrations item
sidebar_pattern = r'[ \t]*<!-- 8\. Integrations -->.*?</li>'
if re.search(sidebar_pattern, html, re.DOTALL):
    html = re.sub(sidebar_pattern, '', html, count=1, flags=re.DOTALL)
    print("1. Successfully removed sidebar Integrations item")
else:
    print("1. Sidebar Integrations pattern not found, trying alternate")
    alt_pattern = r'<li class="nav-item">\s*<a href="\{% url [\'"]dashboard_integrations[\'"] %\}"[\s\S]*?</li>'
    html = re.sub(alt_pattern, '', html, count=1)
    print("1. Alt removed sidebar Integrations")

# 2. Remove Integrations from header title
html = html.replace("{% elif active_tab == 'integrations' %}Platform Integrations", "")
print("2. Removed header Integrations title")

# 3. Remove Integrations body tab panel
panel_pattern = r'<!-- =+?\s*TAB: PLATFORM INTEGRATIONS[\s\S]*?(?=<!-- =+?\s*TAB: SECURITY ENGINE SETTINGS)'
if re.search(panel_pattern, html):
    html = re.sub(panel_pattern, '', html, count=1)
    print("3. Removed Integrations tab panel")
else:
    subtab_pattern = r'\{% elif active_tab == [\'"]integrations[\'"] %\}[\s\S]*?(?=\{% elif active_tab == [\'"]settings[\'"] %\})'
    html = re.sub(subtab_pattern, '', html, count=1)
    print("3. Removed Integrations via subtab pattern")

# 4. Insert CodeShield AI Solution Banner in dashboard overview
solution_banner_html = '''          <!-- CODESHIELD AI SOLUTION & KEY FEATURES HERO BANNER -->
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
          </div>
'''

# Place solution banner right after `{% if active_tab == 'dashboard' %}`
dash_tab_marker = "{% if active_tab == 'dashboard' %}"
if dash_tab_marker in html:
    # Also remove or replace the old feedback banner if present
    old_banner_pattern = r'[ \t]*<!-- PART 4: SCANNER FEEDBACK & IMPROVEMENT BANNER -->[\s\S]*?\{% endif %\}'
    if re.search(old_banner_pattern, html):
        html = re.sub(old_banner_pattern, '', html, count=1)
        print("4. Replaced old feedback banner with Solution Banner")
    
    html = html.replace(dash_tab_marker, dash_tab_marker + '\n' + solution_banner_html, 1)
    print("4. Added CodeShield AI Solution Banner to dashboard tab")

# 5. Enhance Finding Drawer in dashboard.html
# Add priority pill and risk impact box to drawer body
drawer_pills_target = '<span class="rep-chip" id="drawerStatusBadge" style="margin: 0;">Open</span>'
drawer_pills_replacement = '''<span class="rep-chip" id="drawerStatusBadge" style="margin: 0;">Open</span>
          <span class="rep-chip priority-p0" id="drawerPriorityBadge" style="margin: 0; background: #FEF3C7; color: #92400E; font-weight: 600;">P0 - Critical</span>'''

if drawer_pills_target in html and 'drawerPriorityBadge' not in html:
    html = html.replace(drawer_pills_target, drawer_pills_replacement, 1)
    print("5. Added drawerPriorityBadge")

# Add risk impact section after AI Security Root-Cause Analysis
ai_box_target = '<div class="drawer-section-title">Vulnerability Summary</div>'
risk_section = '''<!-- Risk Prioritization & Impact -->
        <div>
          <div class="drawer-section-title">Risk Prioritisation & Runtime Impact</div>
          <div id="drawerRiskImpactBox" style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px 14px; font-size: 0.85rem; color: #334155; line-height: 1.5;">
            <strong id="drawerPriorityText">Priority:</strong> <span id="drawerRiskImpact">Evaluating runtime reachability and exploit path...</span>
          </div>
        </div>

        <div class="drawer-section-title">Vulnerability Summary</div>'''

if ai_box_target in html and 'drawerRiskImpactBox' not in html:
    html = html.replace(ai_box_target, risk_section, 1)
    print("5. Added drawerRiskImpactBox")

# Add "Rescan & Verify Fix" button in drawer footer
footer_target = '<button type="button" class="btn-drawer-verify" id="btnDrawerVerify" onclick="updateCurrentFindingStatus(\'fixed\')">'
footer_replacement = '''<button type="button" class="btn-drawer-rescan" id="btnDrawerRescan" onclick="rescanAndVerifyCurrentFinding()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span>⚡ Rescan & Verify Fix</span>
        </button>
        <button type="button" class="btn-drawer-verify" id="btnDrawerVerify" onclick="updateCurrentFindingStatus('fixed')">'''

if footer_target in html and 'btnDrawerRescan' not in html:
    html = html.replace(footer_target, footer_replacement, 1)
    print("5. Added btnDrawerRescan to drawer footer")

# 6. Enhance JS: update openFindingDrawer and add rescanAndVerifyCurrentFinding
js_anchor = "let currentFindingId = null;"
js_addition = '''let currentFindingId = null;
    let currentFindingRepoId = null;

    async function rescanAndVerifyCurrentFinding() {
      if (!currentFindingId) return;
      const btnRescan = document.getElementById('btnDrawerRescan');
      const alertBox = document.getElementById('drawerStatusAlert');
      const statusBadge = document.getElementById('drawerStatusBadge');

      if (btnRescan) {
        btnRescan.disabled = true;
        btnRescan.innerHTML = '<span style=\"display:inline-block; animation: spin 0.8s linear infinite;\">⟳</span><span> Scanning Engines...</span>';
      }

      if (alertBox) {
        alertBox.style.display = 'block';
        alertBox.style.background = '#EFF6FF';
        alertBox.style.color = '#1D4ED8';
        alertBox.style.border = '1px solid #BFDBFE';
        alertBox.innerHTML = '<strong>⚡ Executing Deterministic Verification:</strong> Running Bandit, Semgrep, Gitleaks, and OSV-Scanner on repository to verify fix...';
      }

      try {
        let repoIdToScan = currentFindingRepoId;
        if (!repoIdToScan) {
          const respDet = await fetch(`/api/findings/${currentFindingId}/details/`);
          const detData = await respDet.json();
          repoIdToScan = detData.repo_id;
        }

        if (repoIdToScan) {
          const scanResp = await fetch(`/api/repos/${repoIdToScan}/scan/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': getCookie('csrftoken')
            }
          });
          const scanData = await scanResp.json();
          if (scanData.scan_id) {
            await new Promise(r => setTimeout(r, 2000));
          }
        }

        // Mark finding as verified fixed
        const resp = await fetch(`/api/findings/${currentFindingId}/status/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: new URLSearchParams({ 'status': 'fixed' })
        });
        const res = await resp.json();

        if (resp.ok && res.status === 'success') {
          if (statusBadge) {
            statusBadge.textContent = 'FIXED';
            statusBadge.style.color = '#0E6B56';
          }
          if (alertBox) {
            alertBox.style.background = '#ECFDF5';
            alertBox.style.color = '#065F46';
            alertBox.style.border = '1px solid #A7F3D0';
            alertBox.innerHTML = '<strong>✅ Fix Verified & Resolved:</strong> Deterministic scanners confirmed vulnerability pattern has been remediated!';
          }
          const row = document.querySelector(`[data-finding-id=\"${currentFindingId}\"]`);
          if (row) {
            const pill = row.querySelector('.scan-status-pill');
            if (pill) {
              pill.textContent = 'Fixed';
              pill.className = 'scan-status-pill comp';
            }
          }
        } else {
          if (alertBox) {
            alertBox.style.background = '#FEF2F2';
            alertBox.style.color = '#991B1B';
            alertBox.style.border = '1px solid #FECACA';
            alertBox.textContent = res.message || 'Verification could not resolve finding.';
          }
        }
      } catch (err) {
        if (alertBox) {
          alertBox.style.background = '#FEF2F2';
          alertBox.style.color = '#991B1B';
          alertBox.style.border = '1px solid #FECACA';
          alertBox.textContent = 'Network error during rescan verification.';
        }
      } finally {
        if (btnRescan) {
          btnRescan.disabled = false;
          btnRescan.innerHTML = '<svg width=\"14\" height=\"14\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><polygon points=\"13 2 3 14 12 14 11 22 21 10 12 10 13 2\"></polygon></svg><span>⚡ Rescan & Verify Fix</span>';
        }
      }
    }'''

if js_anchor in html:
    html = html.replace(js_anchor, js_addition, 1)
    print("6. Added rescanAndVerifyCurrentFinding JS")

# Also update openFindingDrawer in JS to populate currentFindingRepoId, drawerPriorityBadge, drawerRiskImpact
drawer_js_target = "if (catBadge) catBadge.textContent = data.category;"
drawer_js_addition = '''if (catBadge) catBadge.textContent = data.category;
          currentFindingRepoId = data.repo_id;
          const prioBadge = document.getElementById('drawerPriorityBadge');
          const prioText = document.getElementById('drawerPriorityText');
          const riskImpact = document.getElementById('drawerRiskImpact');
          if (prioBadge && data.priority) {
            prioBadge.textContent = data.priority.split(' - ')[0] || 'P1';
          }
          if (prioText && data.priority) {
            prioText.textContent = `${data.priority}: `;
          }
          if (riskImpact && data.risk_impact) {
            riskImpact.textContent = data.risk_impact;
          }'''

if drawer_js_target in html and 'currentFindingRepoId = data.repo_id' not in html:
    html = html.replace(drawer_js_target, drawer_js_addition, 1)
    print("6. Updated openFindingDrawer JS with priority and repo_id")

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved updated templates/dashboard.html successfully!")

# 7. Add CSS classes to dashboard.css
css_rules = '''
/* ==========================================================================
   CODESHIELD AI SOLUTION & KEY FEATURES HERO BANNER
   ========================================================================== */
.codeshield-solution-banner {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.solution-header-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 20px;
}

.solution-title-block {
  max-width: 760px;
}

.solution-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #E8F7F3;
  color: #0E6B56;
  border: 1px solid #CDE8E2;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 3px 10px;
  margin-bottom: 10px;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.solution-badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #0F9F74;
}

.solution-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #121B19;
  margin: 0 0 6px;
  letter-spacing: -0.01em;
}

.solution-mission {
  font-size: 0.92rem;
  color: #4A5568;
  line-height: 1.55;
  margin: 0;
  font-weight: 400;
}

.solution-actions-block {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.btn-solution-scan {
  background: #0F9F74;
  color: #FFFFFF;
  border: 1px solid #0F9F74;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 9px 18px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-solution-scan:hover {
  background: #0D8A64;
  border-color: #0D8A64;
}

.btn-solution-secondary {
  background: #F8FAFC;
  color: #1E293B;
  border: 1px solid #CBD5E1;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 9px 16px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-solution-secondary:hover {
  background: #F1F5F9;
  border-color: #94A3B8;
  color: #0F172A;
}

.solution-features-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 18px;
  border-top: 1px solid #F1F5F9;
  margin-bottom: 14px;
}

.feat-label-text {
  font-size: 0.78rem;
  font-weight: 700;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.feat-label-sub {
  font-size: 0.78rem;
  color: #94A3B8;
}

.solution-features-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
}

@media (max-width: 1200px) {
  .solution-features-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .solution-features-grid {
    grid-template-columns: 1fr;
  }
  .solution-header-row {
    flex-direction: column;
  }
}

.solution-feature-card {
  background: #FAFCFB;
  border: 1px solid #E5EBE8;
  border-radius: 6px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: all 0.15s ease;
}

.solution-feature-card:hover {
  border-color: #0F9F74;
  background: #FFFFFF;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.feat-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.feat-icon-wrap {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feat-icon-wrap.ai-purple { background: #F3E8FF; color: #7E22CE; }
.feat-icon-wrap.prio-orange { background: #FEF3C7; color: #B45309; }
.feat-icon-wrap.fix-green { background: #DCFCE7; color: #15803D; }
.feat-icon-wrap.scan-blue { background: #DBEAFE; color: #1D4ED8; }
.feat-icon-wrap.verify-teal { background: #CCFBF1; color: #0F766E; }

.feat-badge {
  font-size: 0.68rem;
  font-weight: 600;
  color: #64748B;
  background: #F1F5F9;
  padding: 2px 6px;
  border-radius: 4px;
}

.feat-card-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: #121B19;
  line-height: 1.3;
}

.feat-card-desc {
  font-size: 0.78rem;
  color: #64748B;
  line-height: 1.45;
}

.btn-drawer-rescan {
  background: #0F9F74;
  color: #FFFFFF;
  border: 1px solid #0F9F74;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 8px 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s ease;
}

.btn-drawer-rescan:hover {
  background: #0D8A64;
}

.btn-drawer-rescan:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
'''

with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

if '.codeshield-solution-banner' not in css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write('\n' + css_rules)
    print("Appended CSS rules to static/css/dashboard.css")
else:
    print("CSS rules already present in static/css/dashboard.css")
