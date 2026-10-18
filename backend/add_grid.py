with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject the HTML section right after the hero section (which ends with </section>)
hero_end = html.find('</section>') + 10
grid_html = """
    <!-- ==================== VISUAL SERVICES GRID ==================== -->
    <section class="py-16 px-2 sm:px-6 lg:px-8 max-w-[1200px] mx-auto w-full" id="visualServicesSection">
      <div id="beautifulServicesGrid" class="flex flex-wrap justify-center gap-3 sm:gap-4 mx-auto">
        <!-- JS will render this -->
      </div>
    </section>
"""
if 'beautifulServicesGrid' not in html:
    html = html[:hero_end] + '\n' + grid_html + html[hero_end:]

# 2. Inject the JS function before the DOMContentLoaded
js_func = """
      function renderBeautifulGrid() {
        const grid = document.getElementById("beautifulServicesGrid");
        if (!grid) return;
        
        let uniqueServices = [];
        let seenIcons = new Set();
        
        for (let s of ALL_SERVICES) {
           if (!seenIcons.has(s.icon)) {
               seenIcons.add(s.icon);
               uniqueServices.push(s);
           }
        }
        
        let html = '';
        uniqueServices.forEach(s => {
          let shortName = s.name.replace(' Checker', '').replace(' Account', '').replace(' Verification', '').replace(' Validation', ' Valid.');
          // Ensure short names look clean
          if (shortName.includes('Age & Gender')) shortName = s.icon.charAt(0).toUpperCase() + s.icon.slice(1);
          if (shortName.length > 15) shortName = shortName.substring(0, 15) + '..';
          
          html += `
            <a href="/dashboard" class="flex flex-col items-center justify-center bg-white rounded-2xl border border-slate-200 shadow-[0_2px_8px_rgba(0,0,0,0.04)] hover:shadow-[0_8px_16px_rgba(0,0,0,0.08)] hover:-translate-y-1 hover:border-[#435ebf] transition-all duration-300 w-24 h-24 sm:w-28 sm:h-28 group text-decoration-none">
              <div class="mb-2.5 transition-transform duration-300 group-hover:scale-110 flex items-center justify-center">
                ${getBrandSvg(s.icon, 40)}
              </div>
              <span class="text-[10px] sm:text-[11px] font-bold text-slate-600 text-center px-1 leading-tight line-clamp-1 group-hover:text-slate-900">${shortName}</span>
            </a>
          `;
        });
        grid.innerHTML = html;
      }
"""
if 'renderBeautifulGrid()' not in html:
    # insert function
    insert_pos = html.find('function toggleFaq(')
    html = html[:insert_pos] + js_func + '\n      ' + html[insert_pos:]
    
    # insert call inside DOMContentLoaded
    dom_load = html.find('document.addEventListener("DOMContentLoaded", () => {')
    dom_load_inner = html.find('renderPricingVolumeTable();', dom_load)
    html = html[:dom_load_inner] + 'renderBeautifulGrid();\n        ' + html[dom_load_inner:]

with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Beautiful grid added!")
