import re

with open("arc_preview.html", "r") as f:
    html = f.read()

# 1. Update the HTML card container class to include default level-1
html = html.replace('<div class="sci-fi-card" id="card-to-export">', '<div class="sci-fi-card level-1" id="card-to-export">')

# 2. Add level styling definitions inside the CSS block (e.g. right before .sci-fi-card wrapper style)
style_insert = """    /* Level specific themes defined directly on the card to survive html-to-image cloning */
    .sci-fi-card {
      /* Default level-1 values */
      --theme-primary: #00f0ff;
      --theme-glow-color: 0, 240, 255;
      --theme-bezel: linear-gradient(135deg, #a8703c 0%, #5e3a15 40%, #1c0e02 70%, #dca06c 100%); /* Bronze */
    }
    .sci-fi-card.level-1 {
      --theme-primary: #00f0ff; /* Turquoise / Cyan */
      --theme-glow-color: 0, 240, 255;
      --theme-bezel: linear-gradient(135deg, #a8703c 0%, #5e3a15 40%, #1c0e02 70%, #dca06c 100%); /* Bronze */
    }
    .sci-fi-card.level-2 {
      --theme-primary: #c084fc; /* Purple */
      --theme-glow-color: 192, 132, 252;
      --theme-bezel: linear-gradient(135deg, #b0bec5 0%, #6d5b4b 40%, #201a14 70%, #a8886d 100%); /* Bronze-Silver */
    }
    .sci-fi-card.level-3 {
      --theme-primary: #ff007f; /* Magenta / Pink */
      --theme-glow-color: 255, 0, 127;
      --theme-bezel: linear-gradient(135deg, #e2e8f0 0%, #64748b 40%, #1e293b 70%, #cbd5e1 100%); /* Silver */
    }
    .sci-fi-card.level-4 {
      --theme-primary: #22c55e; /* Green */
      --theme-glow-color: 34, 197, 94;
      --theme-bezel: linear-gradient(135deg, #fef08a 0%, #6b7280 40%, #1f2937 70%, #d1d5db 100%); /* Silver-Gold */
    }
    .sci-fi-card.level-5 {
      --theme-primary: #eab308; /* Gold */
      --theme-glow-color: 234, 179, 8;
      --theme-bezel: linear-gradient(135deg, #ffe066 0%, #b38600 40%, #332600 70%, #ffd11a 100%); /* Gold */
    }

    .sci-fi-card {"""

# Replace .sci-fi-card starting line to inject level styling overrides
html = html.replace("    .sci-fi-card {", style_insert)

# 3. Update the avatar frame to use the dynamic theme-bezel background
avatar_wrapper_target = """    .hud-avatar-wrapper {
      position: relative;
      width: 110px;
      height: 110px;
      margin-bottom: 52px;
      border-radius: 50%;
      background: #020306;
      /* Dual-ring metallic frame structure matching the custom logo frame */
      border: 3.5px solid #202738; /* Steel/gray metal outer ring */
      box-shadow: 
        0 8px 24px rgba(0, 0, 0, 0.7), /* Drop shadow */
        inset 0 0 0 1.5px #0a1128, /* Inner dark contrast gap */
        inset 0 0 0 3px #5b6782; /* Inner silver highlight line */
      padding: 0;
    }"""

avatar_wrapper_replacement = """    .hud-avatar-wrapper {
      position: relative;
      width: 110px;
      height: 110px;
      margin-bottom: 52px;
      border-radius: 50%;
      /* Dual-ring metallic frame structure matching the custom logo frame */
      background: var(--theme-bezel); /* Dynamic metal bezel */
      box-shadow: 
        0 8px 24px rgba(0, 0, 0, 0.7), /* Drop shadow */
        inset 0 0 0 1.5px #0a1128, /* Inner dark contrast gap */
        inset 0 0 0 3px rgba(255, 255, 255, 0.2); /* Inner highlight line */
      padding: 3.5px; /* Bezel thickness */
    }"""

html = html.replace(avatar_wrapper_target, avatar_wrapper_replacement)

# 4. Update the level badge container to use dynamic bezel and glow
num_pill_target = """    /* Redesigned Level badge: Circular steel bezel matching the logo frame, with a subtle glow */
    .hud-badge-num-pill {
      position: absolute;
      bottom: -4px;
      right: -4px;
      width: 22px;
      height: 22px;
      background: #0d1321; /* Cyber space dark background */
      border-radius: 50%; /* Perfect circular frame */
      border: 2px solid #202738; /* Steel/gray outer ring to match the logo style */
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 4;
      box-shadow: 
        0 2px 8px rgba(0, 0, 0, 0.8),
        0 0 8px rgba(0, 240, 255, 0.3); /* Subtle, non-distracting cyan glow */
    }

    /* Internal gap for the level badge */
    .hud-badge-num-pill::before {
      content: '';
      position: absolute;
      inset: 1px;
      background: #020306;
      border-radius: 50%;
      z-index: -1;
    }

    .hud-badge-num {
      font-size: 0.75rem; /* Highly legible */
      font-weight: 900;
      color: #00f0ff; /* Soft cyan text */
      font-family: 'Share Tech Mono', monospace;
      text-shadow: 0 0 4px rgba(0, 240, 255, 0.6);
      line-height: 1;
      transform: translateY(-0.5px);
    }"""

num_pill_replacement = """    /* Redesigned Level badge: Circular steel bezel matching the logo frame, with a subtle glow */
    .hud-badge-num-pill {
      position: absolute;
      bottom: -4px;
      right: -4px;
      width: 22px;
      height: 22px;
      background: var(--theme-bezel); /* Dynamic metal bezel */
      border-radius: 50%; /* Perfect circular frame */
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 4;
      padding: 2px; /* Bezel thickness */
      box-shadow: 
        0 2px 8px rgba(0, 0, 0, 0.8),
        0 0 8px rgba(var(--theme-glow-color), 0.3); /* Subtle, non-distracting cyan glow */
    }

    /* Internal gap for the level badge */
    .hud-badge-num-pill::before {
      content: '';
      position: absolute;
      inset: 2px; /* Matches padding */
      background: #020306;
      border-radius: 50%;
      z-index: -1;
    }

    .hud-badge-num {
      font-size: 0.75rem; /* Highly legible */
      font-weight: 900;
      color: var(--theme-primary); /* Soft dynamic text */
      font-family: 'Share Tech Mono', monospace;
      text-shadow: 0 0 4px rgba(var(--theme-glow-color), 0.6);
      line-height: 1;
      transform: translateY(-0.5px);
    }"""

html = html.replace(num_pill_target, num_pill_replacement)

# 5. Replace other hardcoded cyan/pink colors in the stylesheet
# Card outer border glow
html = html.replace("box-shadow: 0 40px 80px rgba(0, 240, 255, 0.2);", "box-shadow: 0 40px 80px rgba(var(--theme-glow-color), 0.2);")
html = html.replace("border-color: rgba(0, 240, 255, 0.4);", "border-color: rgba(var(--theme-glow-color), 0.4);")

# Top header strip and tech label
html = html.replace("border-bottom: 1px solid rgba(0, 240, 255, 0.1);", "border-bottom: 1px solid rgba(var(--theme-glow-color), 0.1);")
html = html.replace("color: rgba(0, 240, 255, 0.4);", "color: rgba(var(--theme-glow-color), 0.4);")

# Card outline bezel (reflective gradient border)
html = html.replace("rgba(0, 240, 255, 0.55) 0%,", "rgba(var(--theme-glow-color), 0.55) 0%,")
html = html.replace("rgba(0, 240, 255, 0.45) 100%", "rgba(var(--theme-glow-color), 0.45) 100%")

# Tech HUD lines
html = html.replace("border: 1px solid rgba(0, 240, 255, 0.2);", "border: 1px solid rgba(var(--theme-glow-color), 0.2);")

# Tech ID tag styling
html = html.replace("color: #00f0ff;", "color: var(--theme-primary);")
html = html.replace("background: rgba(0, 240, 255, 0.05);", "background: rgba(var(--theme-glow-color), 0.05);")
html = html.replace("border: 1px solid rgba(0, 240, 255, 0.3);", "border: 1px solid rgba(var(--theme-glow-color), 0.3);")
html = html.replace("inset 0 1px 3px rgba(0, 240, 255, 0.05),", "inset 0 1px 3px rgba(var(--theme-glow-color), 0.05),")
html = html.replace("rgba(0, 240, 255, 0.22) 20%,", "rgba(var(--theme-glow-color), 0.22) 20%,")
html = html.replace("rgba(0, 240, 255, 0.22) 80%,", "rgba(var(--theme-glow-color), 0.22) 80%,")

# Architect class label color
html = html.replace("color: #ff007f;", "color: var(--theme-primary);")

# Code editor highlighting number color
html = html.replace(".code-content span.number { color: #00f0ff; }", ".code-content span.number { color: var(--theme-primary); }")

# Custom logo drop-shadow glow
html = html.replace("drop-shadow(0 0 4px rgba(0, 240, 255, 0.4))", "drop-shadow(0 0 4px rgba(var(--theme-glow-color), 0.4))")

# 6. Update Javascript level buttons action to toggle the card classes
js_target = """    // Level buttons action
    document.querySelectorAll('.level-select-btn').forEach(btn => {
       btn.addEventListener('click', () => {
          document.querySelectorAll('.level-select-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');

          const lvl = parseInt(btn.getAttribute('data-level'));

          document.getElementById('badge-number').textContent = lvl;
          document.getElementById('code-level-num').textContent = lvl;
       });
     });"""

js_replacement = """    // Level buttons action
    document.querySelectorAll('.level-select-btn').forEach(btn => {
       btn.addEventListener('click', () => {
          document.querySelectorAll('.level-select-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');

          const lvl = parseInt(btn.getAttribute('data-level'));

          document.getElementById('badge-number').textContent = lvl;
          document.getElementById('code-level-num').textContent = lvl;

          // Dynamically toggle level classes on the card container
          const card = document.getElementById("card-to-export");
          card.classList.remove('level-1', 'level-2', 'level-3', 'level-4', 'level-5');
          card.classList.add('level-' + lvl);
       });
     });"""

html = html.replace(js_target, js_replacement)

# Write modified HTML back
with open("arc_preview.html", "w") as f:
    f.write(html)
print("Finished!")
