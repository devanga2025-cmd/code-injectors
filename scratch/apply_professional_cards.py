import re

dashboard_path = r'd:\code_injectors\templates\dashboard.html'
css_path = r'd:\code_injectors\static\css\dashboard.css'

# ==============================================================================
# 1. UPDATE templates/dashboard.html (Drawer Footer & Cards)
# ==============================================================================
with open(dashboard_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace drawer-footer
old_footer_pattern = r'<!-- Drawer Footer Actions -->[\s\S]*?<div class="drawer-footer">[\s\S]*?</div>\s*</aside>'

new_footer_html = '''<!-- Drawer Footer Actions -->
      <div class="drawer-footer">
        <div class="drawer-footer-actions">
          <div class="drawer-footer-left">
            <button type="button" class="btn-drawer-status-pill" onclick="updateCurrentFindingStatus('in_progress')">Mark In Progress</button>
            <button type="button" class="btn-drawer-status-pill muted" onclick="updateCurrentFindingStatus('ignored')">False Positive</button>
          </div>
          <div class="drawer-footer-right">
            <button type="button" class="btn-drawer-outline" id="btnDrawerVerify" onclick="updateCurrentFindingStatus('fixed')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="20 6 9 17 4 12"></polyline></svg>
              <span>Resolve</span>
            </button>
            <button type="button" class="btn-drawer-rescan" id="btnDrawerRescan" onclick="rescanAndVerifyCurrentFinding()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
              <span>Rescan & Verify Fix</span>
            </button>
          </div>
        </div>
      </div>
    </aside>'''

if re.search(old_footer_pattern, html):
    html = re.sub(old_footer_pattern, new_footer_html, html)
    print("1. Replaced drawer-footer in templates/dashboard.html")
else:
    print("1. Could not match old_footer_pattern directly, trying fallback")
    alt_pattern = r'<div class="drawer-footer">[\s\S]*?</aside>'
    html = re.sub(alt_pattern, new_footer_html.split('<!-- Drawer Footer Actions -->\n      ')[1], html)
    print("1. Replaced drawer-footer via fallback")

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(html)


# ==============================================================================
# 2. UPDATE static/css/dashboard.css (Professional Card & Footer Styling)
# ==============================================================================
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .vuln-drawer max-width from 580px to 660px
css = re.sub(r'\.vuln-drawer\s*\{[^}]*max-width:\s*580px;', '.vuln-drawer {\n  width: 100%;\n  max-width: 660px;', css)

# Replace .drawer-footer styles
old_df_pattern = r'\.drawer-footer\s*\{[\s\S]*?(?=\.scans-table-wrap|/\* =+?\s*SCAN HISTORY)'

new_drawer_footer_css = '''.drawer-footer {
  padding: 14px 24px;
  border-top: 1px solid #E2E8F0;
  background-color: #FAFCFB;
  box-sizing: border-box;
}

.drawer-footer-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 12px;
}

.drawer-footer-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.drawer-footer-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-drawer-status-pill {
  background: #FFFFFF;
  color: #475569;
  border: 1px solid #CBD5E1;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 500;
  padding: 7px 12px;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.btn-drawer-status-pill:hover {
  background: #F1F5F9;
  color: #1E293B;
  border-color: #94A3B8;
}

.btn-drawer-status-pill.muted {
  color: #64748B;
}

.btn-drawer-outline {
  background: #FFFFFF;
  color: #0F9F74;
  border: 1px solid #0F9F74;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 7px 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.btn-drawer-outline:hover {
  background: #E8F7F3;
}

.btn-drawer-rescan {
  background: #0F9F74;
  color: #FFFFFF;
  border: 1px solid #0F9F74;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 7px 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s ease;
  white-space: nowrap;
  box-shadow: 0 1px 2px rgba(15, 159, 116, 0.15);
}

.btn-drawer-rescan:hover {
  background: #0D8A64;
  border-color: #0D8A64;
}

.btn-drawer-rescan:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

'''

if re.search(old_df_pattern, css):
    css = re.sub(old_df_pattern, new_drawer_footer_css, css)
    print("2. Replaced .drawer-footer CSS in dashboard.css")
else:
    print("2. Appending new_drawer_footer_css")
    css += '\n' + new_drawer_footer_css

# Refine professional card styling for .drawer-path-card, .problem-card, .code-viewer-container
card_refinements = '''
/* ==========================================================================
   PROFESSIONAL ENTERPRISE CARDS SYSTEM
   ========================================================================== */
.drawer-path-card {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 12px 16px;
}

@media (max-width: 640px) {
  .drawer-path-card {
    grid-template-columns: 1fr 1fr;
  }
}

.path-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.path-label {
  font-size: 0.68rem;
  font-weight: 700;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.path-val {
  font-size: 0.84rem;
  color: #1E293B;
  word-break: break-all;
}

.path-val.line-pill {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  padding: 2px 7px;
  background: #FEE2E2;
  color: #DC2626;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
}

/* Problem Card */
.problem-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.problem-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #0F172A;
  line-height: 1.35;
}

.problem-desc {
  font-size: 0.86rem;
  color: #334155;
  line-height: 1.55;
}

.attack-vector-box {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  border-left: 3px solid #DC2626;
  border-radius: 6px;
  padding: 10px 14px;
  font-size: 0.82rem;
  color: #991B1B;
  line-height: 1.5;
}

/* Code Viewer IDE Box */
.code-viewer-container {
  background: #0D1117;
  border: 1px solid #30363D;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.code-viewer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #161B22;
  padding: 8px 14px;
  border-bottom: 1px solid #30363D;
  font-size: 0.72rem;
}

.code-badge-lang {
  color: #58A6FF;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.code-line-indicator {
  background: #381518;
  color: #F85149;
  border: 1px solid #6E2225;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.72rem;
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
}

.code-file-tag {
  font-size: 0.75rem;
  color: #64748B;
  font-family: 'JetBrains Mono', monospace;
  margin-left: 8px;
}

.code-viewer-pre {
  margin: 0;
  padding: 14px 16px;
  overflow-x: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  line-height: 1.6;
  color: #E6EDF3;
  background: transparent;
}

/* Professional Finding Item Card on Page */
.finding-item-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-left: 3px solid #0F9F74;
  border-radius: 8px;
  padding: 14px 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: all 0.15s ease;
}

.finding-item-card:hover {
  border-color: #0F9F74;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.finding-item-card.crit {
  border-left-color: #DC2626;
}

.finding-item-card.high {
  border-left-color: #EA580C;
}
'''

# Replace previous dynamic drawer styles if present
if '/* DYNAMIC DRAWER PATH' in css:
    css = re.sub(r'/\* =+?\s*DYNAMIC DRAWER PATH[\s\S]*', card_refinements, css)
    print("3. Replaced dynamic drawer styles with refined card system")
else:
    css += '\n' + card_refinements
    print("3. Appended card refinements")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("All card updates and footer fixes applied successfully!")
