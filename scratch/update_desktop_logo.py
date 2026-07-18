import base64
import re
import os

# Read desktop processed png base64
with open("images/desktop_logo_processed.png", "rb") as f:
    b64_str = base64.b64encode(f.read()).decode("utf-8")

# Read html content
with open("arc_preview.html", "r") as f:
    html = f.read()

# Define CSS target and replacement
css_target = """    /* Arch-shaped border for the badge icon matching the Arc logo shape */
    .hud-badge-circle {
      width: 44px;
      height: 48px; /* Slightly taller to represent a perfect Archway shape */
      border-radius: 22px 22px 4px 4px; /* Arch shape: rounded top dome, flat bottom with tiny corners */
      border: 2px solid #ff007f; /* Solid pink border */
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 
        0 0 14px rgba(255, 0, 127, 0.5), /* Sci-fi pink neon glow */
        0 4px 12px rgba(0, 0, 0, 0.7);
      position: relative;
      overflow: hidden; /* Cleanly clip the transparent image to the arch background */
      background: linear-gradient(180deg, #0a1128 0%, #020306 100%); /* Deep cybernetic space background gradient */
      border-bottom: 3px solid #ff007f; /* Thicker bottom base for structural tech look */
    }

    /* Centered Arc logo image with slight scale down (75%) and clean scaling */
    .hud-badge-logo-img {
      width: 75%;
      height: 75%;
      object-fit: contain;
      filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.8)); /* Futuristic white glow on the silver arch logo! */
    }"""

css_replacement = """    /* Arch-shaped border for the badge icon matching the Arc logo shape */
    .hud-badge-circle {
      width: 44px;
      height: 44px; /* Square container for transparent logo overlay */
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: visible; /* Don't clip the custom logo's drop shadows */
      background: transparent; /* Removed background window as requested */
      border: none; /* Removed border */
      box-shadow: none; /* Removed shadow */
    }

    /* Centered Arc logo image with clean scaling and drop shadow */
    .hud-badge-logo-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)) drop-shadow(0 0 4px rgba(0, 240, 255, 0.4)); /* Cybernetic drop-shadow and glow */
    }"""

# Apply CSS replacement
if css_target in html:
    html = html.replace(css_target, css_replacement)
    print("CSS replaced successfully!")
else:
    # Try a fallback replacement if spacing/formatting is slightly different
    print("CSS target NOT found directly, attempting regex replacement...")
    # We can match it using regex
    pattern_circle = r'\.hud-badge-circle\s*\{[^}]*\}'
    pattern_logo = r'\.hud-badge-logo-img\s*\{[^}]*\}'
    html = re.sub(pattern_circle, '''.hud-badge-circle {
      width: 44px;
      height: 44px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: visible;
      background: transparent;
      border: none;
      box-shadow: none;
    }''', html)
    html = re.sub(pattern_logo, '''.hud-badge-logo-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)) drop-shadow(0 0 4px rgba(0, 240, 255, 0.4));
    }''', html)
    print("CSS replaced via regex fallback!")

# HTML regex replacement
# Find the exact img src with class hud-badge-logo-img and replace it
html_pattern = r'class="hud-badge-logo-img" alt="Arc Logo" />'
# We will replace the image src itself
# Let's search for the img inside the hud-badge-circle
html_src_pattern = r'src="data:image/png;base64,[^"]+" class="hud-badge-logo-img"'
html_src_replacement = f'src="data:image/png;base64,{b64_str}" class="hud-badge-logo-img"'

html, count = re.subn(html_src_pattern, html_src_replacement, html)
if count > 0:
    print(f"HTML replaced successfully! ({count} matches)")
else:
    print("HTML pattern NOT matched! Checking manual replacement coordinates...")
    # fallback
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
