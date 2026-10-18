import sys
import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the client portal section from index.html
part_start = html.find('<!-- ==================== LOGGED-IN CLIENT DASHBOARD PORTAL ==================== -->')
part_end = html.find('<!-- ==================== WDES SIGNATURE HERO SECTION ==================== -->')
dashboard_code = html[part_start:part_end]
dashboard_code_visible = dashboard_code.replace('id="clientPortalSection" class="hidden', 'id="clientPortalSection" class="')

new_index = html[:part_start] + html[part_end:]
with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(new_index)

# Build dashboard.html
# Find the header end
header_end = html.find('</header>') + len('</header>\n')
header_part = html[:header_end]

# Find the scripts start (after the main sections)
# Let's just find the footer
footer_start = html.find('<!-- ==================== FOOTER ==================== -->')
footer_part = html[footer_start:]

# We need the modals too? Yes, we should keep the modals.
# But for now, we can just dump the dashboard_code_visible and the footer.
dashboard_page = header_part + '\n' + dashboard_code_visible + '\n' + footer_part

with open('app/static/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_page)

print("Split successful")
