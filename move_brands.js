const fs = require('fs');

const content = fs.readFileSync('index.html', 'utf-8');

// Extract the brands section using regex
const pattern = /(    <!-- ── BRAND LOGOS ── -->\r?\n    <section id="brands" class="reveal">\r?\n(?:[\s\S]*?)\n    <\/section>\r?\n)/;
const match = content.match(pattern);

if (!match) {
    console.error("Could not find brands section!");
    process.exit(1);
}

let brands_section = match[1];

// Remove the original brands section
let newContent = content.replace(brands_section, '');

// We need to transform the brands section to support marquee
const grid_pattern = /(<div class="brands-grid">)([\s\S]*?)(        <\/div>\r?\n      <\/div>\r?\n    <\/section>)/;
const grid_match = brands_section.match(grid_pattern);

if (grid_match) {
    const grid_items = grid_match[2];
    
    // Wrap in marquee structure
    const new_grid_content = `<div class="brands-marquee">
          <div class="brands-track">
${grid_items}${grid_items}          </div>
        </div>
      </div>
    </section>
`;
    brands_section = brands_section.replace(grid_match[0], new_grid_content);
}

// Insert it right before <!-- ── CATEGORIES ── -->
const insert_target = '    <!-- ── CATEGORIES ── -->';
newContent = newContent.replace(insert_target, brands_section + '\n' + insert_target);

fs.writeFileSync('index.html', newContent, 'utf-8');
console.log("Successfully moved and updated brands section!");
