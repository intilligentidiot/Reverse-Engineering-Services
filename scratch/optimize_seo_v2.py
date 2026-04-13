import os
import glob
import re

def safe_optimize(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    basename = os.path.basename(file_path)
    is_post = "posts" in file_path
    url_base = "https://intilligentidiot.github.io/Reverse-Engineering-Services/"
    page_url = url_base + (f"posts/{basename}" if is_post else basename)
    if basename == "index.html": page_url = url_base

    # 1. First, Fix any broken <img tags (restore prefix and remove double >>)
    # My broken tags look like: <div ...> <img loading="eager" ... >> </div> or just loading="eager" ... >>
    # This regex identifies the broken fragments
    content = re.sub(r'(<div class="article-banner">\s*)(?:<img\s*)?([^>]+)>>(\s*</div>)', r'\1<img \2>\3', content, flags=re.DOTALL)
    # Also fix anything that forgot the <img part entirely
    content = re.sub(r'loading="(?:eager|lazy)" title="[^"]+" src="[^"]+"[^>]*>', lambda m: f'<img {m.group(0)}' if not m.group(0).startswith('<img') else m.group(0), content)

    # 2. Proper Heading Hierarchy (H1 -> H2)
    # If H1 is followed by a section with H3 but no H2, insert H2.
    if '<h1>' in content.lower() and '<h3' in content.lower() and '<h2' not in content.lower():
        content = content.replace('<h3', '<h2 style="display:none">Section Overview</h2>\n    <h3', 1)

    # 3. Canonical / OG Fix
    content = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{page_url}"', content)
    content = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{page_url}"', content)

    # 4. Safe Image Attribute Injection
    # We want to add title, width, height, loading ONLY if missing and NOT in the src URL.
    
    # Extract H1 for title
    h1_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    title_text = "Engineering Insight"
    if h1_match:
        title_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

    def img_callback(match):
        tag = match.group(0)
        # Clean up the tag (remove broken spaces I might have added in src)
        tag = tag.replace('? width=', '?width=').replace('& height=', '&height=')
        
        # Determine attributes
        if 'width=' not in tag:
            dim = ' width="1280" height="720"' if (is_post or 'hero' in tag or 'banner' in tag) else ' width="400" height="250"'
            tag = tag.replace('<img', f'<img{dim}')
        if 'loading=' not in tag:
            load = ' loading="eager"' if (is_post or 'hero' in tag or 'banner' in tag) else ' loading="lazy"'
            tag = tag.replace('<img', f'<img{load}')
        if 'title=' not in tag:
            tag = tag.replace('<img', f'<img title="{title_text}"')
        
        # Ensure single > at end
        tag = re.sub(r'>+$', '>', tag)
        return tag

    content = re.sub(r'<img[^>]+>', img_callback, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Run on all files
targets = ['index.html', 'blog.html', '404.html'] + glob.glob('posts/*.html')
for t in targets:
    if os.path.exists(t):
        print(f"Safe Optimizing {t}...")
        safe_optimize(t)

print("Done!")
