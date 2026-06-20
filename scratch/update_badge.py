import base64
import re
import os

# Ensure scratch directory exists
os.makedirs("scratch", exist_ok=True)

# Read transparent png base64
with open("images/arc_logo_transparent_small.png", "rb") as f:
    b64_str = base64.b64encode(f.read()).decode("utf-8")

# Read html content
with open("arc_preview.html", "r") as f:
    html = f.read()

# Define CSS target and replacement
css_target = """    /* Arch-shaped border for the badge icon matching the Arc logo shape */
    .hud-badge-circle {
      width: 42px;
      height: 42px;
      border-radius: 21px 21px 4px 4px; /* Arch shape: rounded top, slightly curved bottom corners */
      border: 1.5px solid #ff007f;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 
        0 0 10px rgba(255, 0, 127, 0.4),
        0 4px 12px rgba(0, 0, 0, 0.6);
      position: relative;
      overflow: visible;
      background: #020306;
    }

    /* Centered Arc logo image with slight scale down (88%) and corresponding arch rounding */
    .hud-badge-logo-img {
      width: 88%;
      height: 88%;
      border-radius: 18px 18px 2px 2px;
      object-fit: cover;
    }

    /* Stylized hexagonal/octagonal tech sub-badge for the level number */
    .hud-badge-num-pill {
      position: absolute;
      bottom: -5px;
      right: -5px;
      width: 18px;
      height: 18px;
      background: #00f0ff;
      /* Octagonal clip path */
      clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 4;
      box-shadow: 0 3px 8px rgba(0, 240, 255, 0.4);
    }

    /* Since clip-path cuts off normal borders, we create a border wrapper effect using a shadow/glow */
    .hud-badge-num-pill::before {
      content: '';
      position: absolute;
      inset: 1px;
      background: #020306; /* Dark background inside the level badge */
      clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%);
      z-index: -1;
    }

    .hud-badge-num {
      font-size: 0.65rem;
      font-weight: 950;
      color: #00f0ff; /* Glowing cyan text instead of dark text */
      font-family: 'Share Tech Mono', monospace;
      text-shadow: 0 0 4px rgba(0, 240, 255, 0.6);
      line-height: 1;
    }"""

css_replacement = """    /* Arch-shaped border for the badge icon matching the Arc logo shape */
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
    }

    /* Stylized hexagonal/octagonal tech sub-badge for the level number */
    .hud-badge-num-pill {
      position: absolute;
      bottom: -6px;
      right: -6px;
      width: 22px; /* Slightly larger for clearer details */
      height: 22px;
      background: #00f0ff; /* Neon cyan accent border */
      /* Sharp hexagonal clip path: horizontal pointing hexagon */
      clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 4;
      box-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
    }

    /* Since clip-path cuts off normal borders, we create a border wrapper effect using a shadow/glow */
    .hud-badge-num-pill::before {
      content: '';
      position: absolute;
      inset: 1.5px; /* Thinner border for high-tech look */
      background: #020306; /* Dark background inside the level badge */
      clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
      z-index: -1;
    }

    .hud-badge-num {
      font-size: 0.72rem; /* Slightly larger text */
      font-weight: 900;
      color: #00f0ff; /* Glowing cyan text */
      font-family: 'Share Tech Mono', monospace;
      text-shadow: 0 0 6px rgba(0, 240, 255, 0.9);
      line-height: 1;
      transform: translateY(-0.5px); /* Fine-tune center alignment */
    }"""

# Apply CSS replacement
if css_target in html:
    html = html.replace(css_target, css_replacement)
    print("CSS replaced successfully!")
else:
    print("CSS target NOT found!")

# HTML regex replacement
# Locate the badge HTML blocks dynamically
html_pattern = r'(<!-- Architect Circular Icon Overlapping bottom-left -->\s*<div class="hud-badge-container">\s*<div class="hud-badge-circle">\s*<img src="data:image/jpeg;base64,[^"]+" class="hud-badge-logo-img" alt="Arc Logo" />\s*<!-- Separate overlapping cyan circular badge for the level number \(1, 2, 3, 4, 5\) -->\s*<div class="hud-badge-num-pill">\s*<span class="hud-badge-num" id="badge-number">1</span>\s*</div>\s*</div>\s*</div>)'

html_replacement = f"""<!-- Architect Circular Icon Overlapping bottom-left -->
            <div class="hud-badge-container">
              <div class="hud-badge-circle">
                <img src="data:image/png;base64,{b64_str}" class="hud-badge-logo-img" alt="Arc Logo" />
              </div>
              <!-- Separate overlapping cyan circular badge for the level number (1, 2, 3, 4, 5) -->
              <div class="hud-badge-num-pill">
                <span class="hud-badge-num" id="badge-number">1</span>
              </div>
            </div>"""

html, count = re.subn(html_pattern, html_replacement, html)
if count > 0:
    print(f"HTML replaced successfully! ({count} matches)")
else:
    print("HTML pattern NOT matched! Trying dynamic replacement...")
    # fallback to a simpler regex or replace
    simple_pattern = r'class="hud-badge-logo-img"[^>]*>'
    # let's find the exact block and replace it
    start_tag = '<!-- Architect Circular Icon Overlapping bottom-left -->'
    end_tag = '<!-- Profil ve detaylar arası geçişli çizgi -->'
    start_idx = html.find(start_tag)
    end_idx = html.find(end_tag)
    if start_idx != -1 and end_idx != -1:
        before = html[:start_idx]
        after = html[end_idx:]
        middle = f"""{start_tag}
            <div class="hud-badge-container">
              <div class="hud-badge-circle">
                <img src="data:image/png;base64,{b64_str}" class="hud-badge-logo-img" alt="Arc Logo" />
              </div>
              <!-- Separate overlapping cyan circular badge for the level number (1, 2, 3, 4, 5) -->
              <div class="hud-badge-num-pill">
                <span class="hud-badge-num" id="badge-number">1</span>
              </div>
            </div>
            
        """
        html = before + middle + after
        print("HTML block replaced via coordinates successfully!")
    else:
        print("Could not find start/end tags in HTML!")

# Save back the html
with open("arc_preview.html", "w") as f:
    f.write(html)
print("Finished!")
