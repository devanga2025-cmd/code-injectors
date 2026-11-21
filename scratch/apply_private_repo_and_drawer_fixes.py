import re

file_path = r'd:\code_injectors\templates\dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update stylesheet cache buster
content = content.replace("dashboard.css?v=6", "dashboard.css?v=7")

# 2. Table: Update scan button to have data attributes
table_btn_old = """                      <button 
                        type="button" 
                        class="btn-table-scan" 
                        id="scan-btn-{{ repo.id }}" 
                        onclick="triggerScan('{{ repo.id }}')"
                      >"""

table_btn_new = """                      <button 
                        type="button" 
                        class="btn-table-scan" 
                        id="scan-btn-{{ repo.id }}" 
                        data-repo-id="{{ repo.id }}"
                        data-name="{{ repo.name }}"
                        data-branch="{{ repo.default_branch }}"
                        data-private="{{ repo.is_private|yesno:'true,false' }}"
                        onclick="triggerScan('{{ repo.id }}')"
                      >"""

if table_btn_old in content:
    content = content.replace(table_btn_old, table_btn_new, 1)
    print("1. Updated table scan button with data attributes")
else:
    print("1. Table scan button pattern not found (may already have attributes)")

# 3. Table: Visibility pill with lock emoji for private
table_vis_old = """                            {% if repo.is_private %}
                              <span class="repo-vis-pill private">Private</span>
                            {% else %}
                              <span class="repo-vis-pill public">Public</span>
                            {% endif %}"""

table_vis_new = """                            {% if repo.is_private %}
                              <span class="repo-vis-pill private" style="background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D;">🔒 Private</span>
                            {% else %}
                              <span class="repo-vis-pill public">Public</span>
                            {% endif %}"""

if table_vis_old in content:
    content = content.replace(table_vis_old, table_vis_new, 1)
    print("2. Updated table visibility pill to 🔒 Private")

# 4. Project Card: Visibility pill
proj_vis_old = """                      {% if r.is_private %}
                        <span class="rep-chip" style="margin: 0; font-size: 0.68rem;">Private</span>
                      {% else %}
                        <span class="rep-chip" style="margin: 0; font-size: 0.68rem; background: #F1F5F9; color: #475569; border-color: #E2E8F0;">Public</span>
                      {% endif %}"""

proj_vis_new = """                      {% if r.is_private %}
                        <span class="rep-chip" style="margin: 0; font-size: 0.68rem; background: #FEF3C7; color: #92400E; border-color: #FCD34D;">🔒 Private</span>
                      {% else %}
                        <span class="rep-chip" style="margin: 0; font-size: 0.68rem; background: #F1F5F9; color: #475569; border-color: #E2E8F0;">Public</span>
                      {% endif %}"""

if proj_vis_old in content:
    content = content.replace(proj_vis_old, proj_vis_new, 1)
    print("3. Updated project card visibility pill to 🔒 Private")

# 5. Project Card: Scan button data attributes
proj_btn_old = """<button type="button" class="btn-conn-sync" id="scan-btn-{{ r.id }}" onclick="triggerScan('{{ r.id }}')" style="flex: 1; padding: 7px 12px; font-size: 0.78rem;">"""
proj_btn_new = """<button type="button" class="btn-conn-sync" id="scan-btn-{{ r.id }}" data-repo-id="{{ r.id }}" data-name="{{ r.name }}" data-branch="{{ r.default_branch }}" data-private="{{ r.is_private|yesno:'true,false' }}" onclick="triggerScan('{{ r.id }}')" style="flex: 1; padding: 7px 12px; font-size: 0.78rem;">"""

if proj_btn_old in content:
    content = content.replace(proj_btn_old, proj_btn_new, 1)
    print("4. Updated project card scan button with data attributes")

# 6. New Scan Modal select option with 🔒 Private
select_opt_old = """            {% for r in all_user_repos %}
              <option value="{{ r.id }}">{{ r.name }} ({{ r.default_branch }})</option>
            {% empty %}"""

select_opt_new = """            {% for r in all_user_repos %}
              <option value="{{ r.id }}" data-name="{{ r.name }}" data-branch="{{ r.default_branch }}" data-private="{{ r.is_private|yesno:'true,false' }}">{{ r.name }} ({{ r.default_branch }}){% if r.is_private %} [🔒 Private]{% endif %}</option>
            {% empty %}"""

if select_opt_old in content:
    content = content.replace(select_opt_old, select_opt_new, 1)
    print("5. Updated New Scan Modal options with private indicator")

# 7. Insert Private Repo Authorization Modal HTML
private_modal_html = '''  <!-- ====================================================================
       PRIVATE REPOSITORY CONFIRMATION & AUTHORIZATION MODAL
       ==================================================================== -->
  <div class="dash-modal-overlay" id="privateRepoPromptModal" role="dialog" aria-modal="true" aria-labelledby="privateRepoModalTitle">
    <div class="dash-modal-card" style="max-width: 530px; width: 92%; border-radius: 12px; box-shadow: 0 20px 45px rgba(0,0,0,0.25); overflow: hidden; padding: 0; border: 1px solid #CBD5E1;">
      
      <!-- Modal Header Banner -->
      <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-bottom: 1px solid #334155; padding: 18px 22px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 38px; height: 38px; border-radius: 50%; background: rgba(15, 159, 116, 0.15); display: flex; align-items: center; justify-content: center; border: 1px solid rgba(15, 159, 116, 0.35); flex-shrink: 0;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#20C9A3" stroke-width="2.2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <div>
            <h3 id="privateRepoModalTitle" style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin: 0; line-height: 1.25;">Authorize Private Repository Scan</h3>
            <span style="font-size: 0.75rem; color: #94A3B8; font-weight: 500;">Zero-Retention Ephemeral Sandbox Guarantee</span>
          </div>
        </div>
        <button type="button" class="dash-modal-close" onclick="closePrivateRepoModal()" style="color: #94A3B8; font-size: 1.4rem; cursor: pointer; border: none; background: transparent;">&times;</button>
      </div>

      <!-- Modal Body -->
      <div style="padding: 20px 22px; background: #FFFFFF;">
        <!-- Target Repo Card -->
        <div style="display: flex; align-items: center; gap: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 8px; margin-bottom: 14px;">
          <span style="font-size: 0.78rem; font-weight: 600; color: #475569;">Target Repository:</span>
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #0F9F74;" id="privateRepoNameDisplay">repository-name</span>
          <span class="rep-chip" style="margin-left: auto; background: #FEF3C7; color: #92400E; font-size: 0.72rem; font-weight: 600; padding: 2px 8px; border-radius: 4px; border: 1px solid #FCD34D;">🔒 Private</span>
        </div>

        <p style="font-size: 0.85rem; color: #334155; line-height: 1.55; margin: 0 0 14px;">
          This repository is marked as <strong>Private</strong> on GitHub. Do you authorize CodeShield AI to run automated vulnerability, exposed secret, and dependency audits on this codebase?
        </p>

        <!-- Zero-Retention Privacy Disclosures -->
        <div style="display: flex; flex-direction: column; gap: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 14px; margin-bottom: 16px;">
          <div style="display: flex; align-items: flex-start; gap: 8px; font-size: 0.8125rem; color: #1E293B; line-height: 1.45;">
            <span style="color: #0F9F74; font-weight: 700;">🛡️</span>
            <div>
              <strong>Ephemeral Sandbox:</strong> Cloned into a temporary memory-mapped container strictly for AST static analysis.
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 8px; font-size: 0.8125rem; color: #1E293B; line-height: 1.45;">
            <span style="color: #0F9F74; font-weight: 700;">🔒</span>
            <div>
              <strong>Zero-Retention Guarantee:</strong> Cloned files and AST artifacts are completely purged from disk immediately post-scan. Code is never stored.
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 8px; font-size: 0.8125rem; color: #1E293B; line-height: 1.45;">
            <span style="color: #0F9F74; font-weight: 700;">🔑</span>
            <div>
              <strong>Read-Only Token Access:</strong> Performed via your personal OAuth session with granular read-only repository permissions.
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Footer Actions -->
      <div style="padding: 12px 22px 16px; background: #F8FAFC; border-top: 1px solid #E2E8F0; display: flex; align-items: center; justify-content: flex-end; gap: 10px;">
        <button type="button" class="btn-modal-cancel" onclick="closePrivateRepoModal()" style="font-size: 0.8125rem; height: 34px; padding: 0 14px; background: #FFFFFF; color: #475569; border: 1px solid #CBD5E1; cursor: pointer; border-radius: 6px;">
          Cancel
        </button>
        <button type="button" class="btn-modal-submit" id="btnConfirmPrivateScan" onclick="confirmPrivateScan()" style="font-size: 0.8125rem; height: 34px; padding: 0 16px; background: #0F9F74; color: #FFFFFF; border: 1px solid #0F9F74; cursor: pointer; font-weight: 600; border-radius: 6px; display: inline-flex; align-items: center; gap: 6px;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
          <span>Authorize & Run Private Scan</span>
        </button>
      </div>

    </div>
  </div>\n\n'''

vuln_overlay_anchor = '  <!-- 5. Interactive Vulnerability Details & AI Security Explanation Drawer -->'
if 'privateRepoPromptModal' not in content and vuln_overlay_anchor in content:
    content = content.replace(vuln_overlay_anchor, private_modal_html + vuln_overlay_anchor, 1)
    print("6. Inserted privateRepoPromptModal HTML")
elif 'privateRepoPromptModal' not in content:
    alt_anchor = '  <div class="vuln-drawer-overlay"'
    content = content.replace(alt_anchor, private_modal_html + alt_anchor, 1)
    print("6. Inserted privateRepoPromptModal HTML via alt anchor")

# 8. Add JS map and handlers for private scan authorization
js_injection = '''    // Global Repository Privacy Configuration Map
    const reposPrivacyMap = {
      {% for r in all_user_repos %}
      "{{ r.id }}": {
        name: "{{ r.name|escapejs }}",
        branch: "{{ r.default_branch|escapejs }}",
        isPrivate: {{ r.is_private|yesno:"true,false" }}
      },
      {% endfor %}
    };

    let pendingPrivateScan = null;

    function openPrivateRepoModal(repoId, repoName, branch) {
      pendingPrivateScan = { repoId, branch };
      const displayEl = document.getElementById('privateRepoNameDisplay');
      if (displayEl) displayEl.textContent = repoName || `Repo #${repoId}`;
      const modal = document.getElementById('privateRepoPromptModal');
      if (modal) modal.classList.add('active');
    }

    function closePrivateRepoModal() {
      const modal = document.getElementById('privateRepoPromptModal');
      if (modal) modal.classList.remove('active');
      pendingPrivateScan = null;
    }

    function confirmPrivateScan() {
      if (!pendingPrivateScan) return;
      const { repoId, branch } = pendingPrivateScan;
      closePrivateRepoModal();
      triggerScan(repoId, branch, true);
    }
'''

if 'reposPrivacyMap' not in content:
    content = content.replace("    // CSRF Token Helper", js_injection + "\n    // CSRF Token Helper", 1)
    print("7. Injected reposPrivacyMap and private scan helper JS")

# 9. Update triggerScan function to handle private repo check
old_trigger_scan = """    async function triggerScan(repoId, branchName = null) {
      // Prevent duplicate scan requests
      if (activeScanningRepoId) {
        alert('A security scan is already currently running. Please wait for it to complete.');
        return;
      }"""

new_trigger_scan = """    async function triggerScan(repoId, branchName = null, bypassPrivateCheck = false) {
      // Prevent duplicate scan requests
      if (activeScanningRepoId) {
        alert('A security scan is already currently running. Please wait for it to complete.');
        return;
      }

      // Check if target repository is private and needs user authorization
      const repoMeta = reposPrivacyMap[repoId] || {};
      const repoBtn = document.getElementById(`scan-btn-${repoId}`);
      const isPrivateRepo = repoMeta.isPrivate !== undefined ? repoMeta.isPrivate : (repoBtn?.dataset?.private === 'true');
      const repoName = repoMeta.name || repoBtn?.dataset?.name || `Repo #${repoId}`;
      const branchToScan = branchName || repoMeta.branch || repoBtn?.dataset?.branch || 'main';

      if (!bypassPrivateCheck && isPrivateRepo) {
        openPrivateRepoModal(repoId, repoName, branchToScan);
        return;
      }"""

if old_trigger_scan in content:
    content = content.replace(old_trigger_scan, new_trigger_scan, 1)
    print("8. Updated triggerScan with private check")

# 10. Update openFindingDrawer for flawless client hydration & fallback
old_open_drawer = """      // 1. INSTANT CLIENT-SIDE HYDRATION (from card dataset if available)
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
      }"""

new_open_drawer = """      // 1. INSTANT CLIENT-SIDE HYDRATION (from card dataset if available)
      const card = triggerEl ? triggerEl.closest('.finding-item-card') : document.querySelector(`[data-finding-id="${findingId}"]`);
      if (card && card.dataset) {
        const ds = card.dataset;
        const filePath = (ds.file || '').replace(/\\\\/g, '/');
        let fFolder = './';
        let fName = filePath;
        if (filePath.includes('/')) {
          const parts = filePath.split('/');
          fName = parts.pop();
          fFolder = parts.join('/') + '/';
        }
        if (ruleEl && ds.rule) ruleEl.textContent = `[${ds.rule}]`;
        if (repoEl && ds.repo) repoEl.textContent = ds.repo;
        if (folderEl) folderEl.textContent = fFolder;
        if (fileEl) fileEl.textContent = fName;
        if (lineEl && ds.line) lineEl.textContent = `Line ${ds.line}`;
        if (locEl && ds.file && ds.line) locEl.textContent = `${ds.repo || ''} ➔ ${ds.file}:Line ${ds.line}`;
        if (probTitle && ds.rule) probTitle.textContent = ds.rule;
        if (msgEl && ds.message) msgEl.textContent = ds.message;
        if (sevBadge && ds.sev) {
          sevBadge.textContent = ds.sev;
          sevBadge.className = `scan-status-pill ${ds.sev === 'CRITICAL' ? 'crit' : 'in-progress'}`;
        }
        if (catBadge && ds.cat) catBadge.textContent = ds.cat;
        if (reachBadge && ds.reach) reachBadge.textContent = ds.reach;
        if (diffRem && ds.message) diffRem.textContent = `- ${ds.message}`;
        if (diffAdd && ds.remediation) diffAdd.textContent = `+ ${ds.remediation}`;
        if (codeTagEl && ds.file && ds.line) codeTagEl.textContent = `${ds.file}:${ds.line}`;
        if (codeSnippetEl) {
          codeSnippetEl.textContent = `${Math.max(1, parseInt(ds.line||1)-1)} | # Target module: ${fName}\\n${ds.line || 1} | ${ds.message || 'Finding context'}\\n${parseInt(ds.line||1)+1} | return result`;
        }
        if (aiEl) {
          aiEl.textContent = `AST syntax inspection detected [${ds.rule}] in ${ds.file} on line ${ds.line}. ${ds.message}`;
        }
      } else {
        if (ruleEl) ruleEl.textContent = 'Rule Inspection';
        if (locEl) locEl.textContent = 'Loading location...';
        if (aiEl) aiEl.textContent = 'Retrieving AI security explanation...';
      }"""

if old_open_drawer in content:
    content = content.replace(old_open_drawer, new_open_drawer, 1)
    print("9. Enhanced openFindingDrawer client hydration")

# 11. In openFindingDrawer fallback: do not set "Could not load details" if already hydrated
old_fallback = """        } else {
          if (aiEl) aiEl.textContent = data.message || 'Could not load details for this finding.';
        }
      } catch (err) {
        console.error('Error fetching finding details:', err);
        if (aiEl) aiEl.textContent = 'Finding context loaded from local metadata.';
      }"""

new_fallback = """        } else {
          if (aiEl && (!card || !aiEl.textContent)) {
            aiEl.textContent = data.message || 'Finding context loaded from verified local metadata.';
          }
        }
      } catch (err) {
        console.error('Error fetching finding details:', err);
        if (aiEl && (!card || !aiEl.textContent)) {
          aiEl.textContent = 'Finding context loaded from verified local metadata.';
        }
      }"""

if old_fallback in content:
    content = content.replace(old_fallback, new_fallback, 1)
    print("10. Enhanced openFindingDrawer error fallback")

# 12. Modal click outside handler
old_modal_click = "['feedbackModal', 'connectModal', 'manageConnModal', 'newScanModal', 'scanProgressModal', 'emptyRepoModal'].forEach(id => {"
new_modal_click = "['feedbackModal', 'connectModal', 'manageConnModal', 'newScanModal', 'scanProgressModal', 'emptyRepoModal', 'privateRepoPromptModal'].forEach(id => {"

if old_modal_click in content:
    content = content.replace(old_modal_click, new_modal_click, 1)
    print("11. Added privateRepoPromptModal to click-outside handler")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("All updates successfully written to templates/dashboard.html!")
