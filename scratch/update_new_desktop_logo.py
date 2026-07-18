import base64
from PIL import Image
import re
import os

# Open the new desktop logo.png
desktop_path = '/Users/emreoktem/Desktop/logo.png'
img = Image.open(desktop_path)
# Resize it to 80x80 using high-quality Lanczos resampling
img_small = img.resize((80, 80), Image.Resampling.LANCZOS)
# Save it
img_small.save('images/desktop_logo_processed.png', 'PNG')

# Read transparent png base64
with open("images/desktop_logo_processed.png", "rb") as f:
    b64_str = base64.b64encode(f.read()).decode("utf-8")

# Read html content
with open("arc_preview.html", "r") as f:
    html = f.read()

# HTML regex replacement
# We will replace the image src itself
html_src_pattern = r'src="data:image/png;base64,[^"]+" class="hud-badge-logo-img"'
html_src_replacement = f'src="data:image/png;base64,{b64_str}" class="hud-badge-logo-img"'

html, count = re.subn(html_src_pattern, html_src_replacement, html)
if count > 0:
    print(f"HTML replaced successfully! ({count} matches)")
else:
    print("HTML pattern NOT matched! Trying coordinate replacement...")
    start_tag = '<div class="hud-badge-circle">'
    end_tag = '</div>\n              <!-- Separate overlapping cyan circular'
    start_idx = html.find(start_tag)
    end_idx = html.find(end_tag)
    if start_idx != -1 and end_idx != -1:
        before = html[:start_idx]
        after = html[end_idx:]
        middle = f"""<div class="hud-badge-circle">
                <img src="data:image/png;base64,{b64_str}" class="hud-badge-logo-img" alt="Arc Logo" />"""
        html = before + middle + after
        print("HTML block replaced via coordinates successfully!")
    else:
        print("Could not find start/end HTML tags!")

# Save back the html
with open("arc_preview.html", "w") as f:
    f.write(html)
print("Finished!")
