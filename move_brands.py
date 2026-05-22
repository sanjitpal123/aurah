import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the brands section using regex
# From <!-- ── BRAND LOGOS ── --> to the closing </section> of brands
pattern = r'(    <!-- ── BRAND LOGOS ── -->\n    <section id="brands" class="reveal">\n(?:.*?)\n    </section>\n)'
match = re.search(pattern, content, re.DOTALL)
if not match:
    print("Could not find brands section!")
    exit(1)

brands_section = match.group(1)

# Remove the original brands section
content = content.replace(brands_section, '')

# We need to transform the brands section to support marquee
# We will duplicate the contents of .brands-grid so it can scroll seamlessly
brands_grid_pattern = r'(<div class="brands-grid">)(.*?)(        </div>\n      </div>\n    </section>)'
grid_match = re.search(brands_grid_pattern, brands_section, re.DOTALL)

if grid_match:
    grid_start = grid_match.group(1)
    grid_items = grid_match.group(2)
    grid_end = grid_match.group(3)
    
    # Wrap in marquee structure
    # We will rename brands-grid to brands-track, and wrap it in brands-marquee
    new_grid_content = f"""<div class="brands-marquee">
          <div class="brands-track">
{grid_items}{grid_items}          </div>
        </div>
      </div>
    </section>
"""
    brands_section = brands_section.replace(grid_match.group(0), new_grid_content)

# Insert it right before <!-- ── CATEGORIES ── -->
insert_target = '    <!-- ── CATEGORIES ── -->'
content = content.replace(insert_target, brands_section + '\n' + insert_target)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully moved and updated brands section!")
