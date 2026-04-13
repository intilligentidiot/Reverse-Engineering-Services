import os
import glob
import re

def strict_cleanup(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. First, remove ANY double <img <img
    content = re.sub(r'<img\s+<img', '<img', content)
    
    # 2. Ensure exactly one > at end of tags
    # This matches <img ... >> or <img ... >>> and simplifies to <img ... >
    content = re.sub(r'(<img[^>]+)>+', r'\1>', content)

    # 3. Fix the specific posts that missed attributes
    # I'll just re-run a simplified attribute injection that handles duplicates
    
    h1_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    title_text = "Engineering Insight"
    if h1_match:
        title_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

    is_post = "posts" in file_path

    def img_fixer(match):
        tag = match.group(0)
        # Ensure title, loading, width, height are there and not duplicated
        is_hero = is_post or 'banner' in tag or 'hero' in tag
        
        if 'title=' not in tag:
            tag = tag.replace('<img', f'<img title="{title_text}"')
        if 'loading=' not in tag:
            l = 'eager' if is_hero else 'lazy'
            tag = tag.replace('<img', f'<img loading="{l}"')
        if 'width=' not in tag:
            w, h = ('1280', '720') if is_hero else ('400', '250')
            tag = tag.replace('<img', f'<img width="{w}" height="{h}"')
            
        return tag

    content = re.sub(r'<img[^>]+>', img_fixer, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Targets
targets = glob.glob('posts/*.html') + ['index.html', 'blog.html', '404.html']
for t in targets:
    if os.path.exists(t):
        print(f"Cleanup {t}...")
        strict_cleanup(t)

print("Final Cleanup Done!")
