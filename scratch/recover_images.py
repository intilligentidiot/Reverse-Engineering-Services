import os
import glob
import re

def fix_broken_imgs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. First, find "tags" that start with loading=, width=, title= but don't have <img
    # My script turned <img src=...> into loading="eager" title="..." width="..." src=...>
    # So I should look for those patterns and prepend <img
    
    # The broken tags in the view_file looked like:
    # loading="eager" title="..." width="..." height="..." src="..." ... >
    
    # Regex to find these broken segments
    # They usually start with loading=, width=, or title= and end with >
    # But wait, they are preceded by whitespace or a newline.
    
    # A safer way: just find everything between <div class="article-banner"> and </div>
    # and if it doesn't have <img, add it.
    
    def recover_img(match):
        inner = match.group(1)
        if '<img' not in inner and 'src=' in inner:
            return f'<div class="article-banner">\n            <img {inner.strip()}>\n        </div>'
        return match.group(0)

    content = re.sub(r'<div class="article-banner">\s*(.*?)\s*</div>', recover_img, content, flags=re.DOTALL)

    # Also check blog cards in js (if I broke it there)
    # Actually I used replace_file_content for js/script.js, which I manually checked or it was less likely to fail like the regex did.
    # Let me check js/script.js again too.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Run recovery on posts
posts = glob.glob('posts/*.html')
for p in posts:
    print(f"Recovering {p}...")
    fix_broken_imgs(p)

print("Recovery done!")
