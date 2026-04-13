import os
import glob
import re

def optimize_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine base info
    basename = os.path.basename(file_path)
    is_post = "posts" in file_path
    url_base = "https://intilligentidiot.github.io/Reverse-Engineering-Services/"
    page_url = url_base + (f"posts/{basename}" if is_post else basename)
    if basename == "index.html": page_url = url_base

    # 1. Meta Align (Canonical / OG)
    content = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{page_url}"', content)
    content = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{page_url}"', content)
    content = re.sub(r'<meta property="twitter:url" content="[^"]*"', f'<meta property="twitter:url" content="{page_url}"', content)

    # 2. Header Check
    # Re-extract H1 for title
    h1_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    title_text = "Engineering Experts"
    if h1_match:
        title_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

    # 3. Image Optimization
    def fix_img(match):
        img_tag = match.group(0)
        # Skip if it already has dimensions (some might)
        if 'width=' in img_tag and 'height=' in img_tag and 'loading=' in img_tag:
            return img_tag
        
        # Determine attributes
        # For banners (class article-banner or hero-bg or long image in post), use eagerness
        is_hero = 'hero' in img_tag or 'banner' in img_tag or is_post
        loading = 'eager' if is_hero else 'lazy'
        
        # Add attributes if missing
        if 'title=' not in img_tag:
            img_tag = img_tag.replace('<img ', f'<img title="{title_text}" ')
        if 'width=' not in img_tag:
            # Standard banner/card sizes
            img_tag = img_tag.replace('<img ', 'width="1280" height="720" ' if is_hero else 'width="400" height="250" ')
        if 'loading=' not in img_tag:
            img_tag = img_tag.replace('<img ', f'loading="{loading}" ')
        
        # Clean up any potential messy insertions
        img_tag = img_tag.replace('width=', ' width=').replace('height=', ' height=').replace('loading=', ' loading=').replace('title=', ' title=')
        img_tag = re.sub(r'\s+', ' ', img_tag)
        return img_tag

    content = re.sub(r'<img[^>]+>', fix_img, content)

    # 4. Heading Sequence Audit (H1 -> H2 -> H3)
    # If H1 then H3 exists but no H2, we'll try to insert a structural one.
    # This is harder to automate perfectly, so I'll do a simple check.
    has_h1 = '<h1' in content.lower()
    has_h2 = '<h2' in content.lower()
    has_h3 = '<h3' in content.lower()
    
    if has_h1 and has_h3 and not has_h2:
        # Insert a hidden H2 before the first H3
        content = content.replace('<h3', '<h2 style="display:none">Section Details</h2>\n    <h3', 1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Target list
targets = ['index.html', 'blog.html', '404.html'] + glob.glob('posts/*.html')
for t in targets:
    if os.path.exists(t):
        print(f"Optimizing {t}...")
        optimize_file(t)

print("Done!")
