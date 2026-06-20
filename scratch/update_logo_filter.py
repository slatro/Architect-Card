with open("arc_preview.html", "r") as f:
    html = f.read()

# 1. Initialize the role string in HTML to "Arc Initiate" to match Level 1 on load
html = html.replace('<span class="string" id="code-role-str">"Arc Ambassador"</span>', '<span class="string" id="code-role-str">"Arc Initiate"</span>')

# 2. Add level-specific CSS filters for the logo image to dynamically shift the blue bezel and glow to match the active level theme color
filter_css_target = """    .sci-fi-card.level-1 {
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
    }"""

filter_css_replacement = """    .sci-fi-card.level-1 {
      --theme-primary: #00f0ff; /* Turquoise / Cyan */
      --theme-glow-color: 0, 240, 255;
      --theme-bezel: linear-gradient(135deg, #a8703c 0%, #5e3a15 40%, #1c0e02 70%, #dca06c 100%); /* Bronze */
    }
    .sci-fi-card.level-1 .hud-badge-logo-img {
      filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)) drop-shadow(0 0 4px rgba(var(--theme-glow-color), 0.4)); /* Original blue/cyan */
    }
    .sci-fi-card.level-2 {
      --theme-primary: #c084fc; /* Purple */
      --theme-glow-color: 192, 132, 252;
      --theme-bezel: linear-gradient(135deg, #b0bec5 0%, #6d5b4b 40%, #201a14 70%, #a8886d 100%); /* Bronze-Silver */
    }
    .sci-fi-card.level-2 .hud-badge-logo-img {
      filter: hue-rotate(60deg) saturate(1.2) drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)); /* Shifts blue bezel to purple */
    }
    .sci-fi-card.level-3 {
      --theme-primary: #ff007f; /* Magenta / Pink */
      --theme-glow-color: 255, 0, 127;
      --theme-bezel: linear-gradient(135deg, #e2e8f0 0%, #64748b 40%, #1e293b 70%, #cbd5e1 100%); /* Silver */
    }
    .sci-fi-card.level-3 .hud-badge-logo-img {
      filter: hue-rotate(110deg) saturate(1.3) drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)); /* Shifts blue bezel to magenta/pink */
    }
    .sci-fi-card.level-4 {
      --theme-primary: #22c55e; /* Green */
      --theme-glow-color: 34, 197, 94;
      --theme-bezel: linear-gradient(135deg, #fef08a 0%, #6b7280 40%, #1f2937 70%, #d1d5db 100%); /* Silver-Gold */
    }
    .sci-fi-card.level-4 .hud-badge-logo-img {
      filter: hue-rotate(260deg) saturate(1.2) brightness(1.1) drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)); /* Shifts blue bezel to green */
    }
    .sci-fi-card.level-5 {
      --theme-primary: #eab308; /* Gold */
      --theme-glow-color: 234, 179, 8;
      --theme-bezel: linear-gradient(135deg, #ffe066 0%, #b38600 40%, #332600 70%, #ffd11a 100%); /* Gold */
    }
    .sci-fi-card.level-5 .hud-badge-logo-img {
      filter: hue-rotate(210deg) saturate(1.5) brightness(1.2) drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)); /* Shifts blue bezel to gold */
    }"""

if filter_css_target in html:
    html = html.replace(filter_css_target, filter_css_replacement)
    print("Logo hue filter classes added successfully!")
else:
    html = html.replace(filter_css_target.replace("\r\n", "\n"), filter_css_replacement)
    print("Logo hue filter classes added via newline normalization!")

with open("arc_preview.html", "w") as f:
    f.write(html)
print("Finished!")
