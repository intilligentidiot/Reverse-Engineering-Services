import os
import glob

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Branding Header/Footer
    content = content.replace('<h4>Precision Engineering Experts</h4>', '<h4>Tesla Mechanical Designs</h4>')
    content = content.replace('&copy; 2026 Precision Engineering Experts. All Rights Reserved.', '&copy; 2026 Tesla Mechanical Designs. All Rights Reserved.')
    
    # 2. Contact Info
    content = content.replace('<p>Email: contact@engineeringexperts.com</p>', 
                             '<p>USA, 1 Dayton Dr #5D, Edison, New Jersey, 0882</p>\n                <p>Phone: +1 510 680 3390</p>')
    
    # 3. Schema Organization Name
    content = content.replace('"name": "Precision Engineering Experts"', '"name": "Tesla Mechanical Designs"')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Target all HTML files in posts directory
posts = glob.glob('posts/*.html')
for post in posts:
    print(f"Updating {post}...")
    update_file(post)

print("Done!")
