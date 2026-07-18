# Read html content
with open("arc_preview.html", "r") as f:
    html = f.read()

# Define CSS target and replacement
css_target = """    .hud-avatar-wrapper {
      position: relative;
      width: 110px;
      height: 110px;
      margin-bottom: 52px;
      border-radius: 50%;
      background: #020306;
      /* Dual-ring metallic frame structure */
      border: 3px solid #141b2d;
      outline: 1.5px solid rgba(255, 255, 255, 0.08);
      outline-offset: -4.5px;
      box-shadow: 
        0 12px 30px rgba(0, 0, 0, 0.75),
        inset 0 4px 10px rgba(0, 0, 0, 0.95);
      padding: 0;
    }



    .hud-avatar-img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
      background-color: #0c0f1d;
      border: none;
      position: relative;
      z-index: 1;
    }

    .hud-badge-container {
      position: absolute;
      bottom: -6px;
      left: -6px;
      z-index: 3;
    }

    /* Arch-shaped border for the badge icon matching the Arc logo shape */
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

css_replacement = """    .hud-avatar-wrapper {
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
    }



    .hud-avatar-img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
      background-color: #0c0f1d;
      border: none;
      position: relative;
      z-index: 1;
    }

    .hud-badge-container {
      position: absolute;
      bottom: -6px;
      left: -6px;
      z-index: 3;
    }

    /* Arch-shaped border for the badge icon matching the Arc logo shape */
    .hud-badge-circle {
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
    }

    /* Centered Arc logo image with clean scaling and drop shadow */
    .hud-badge-logo-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)) drop-shadow(0 0 4px rgba(0, 240, 255, 0.4));
    }

    /* Redesigned Level badge: Circular steel bezel matching the logo frame, with a subtle glow */
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

# Apply CSS replacement
if css_target in html:
    html = html.replace(css_target, css_replacement)
    print("CSS replaced successfully!")
else:
    print("CSS target NOT found directly, attempting fallback replacement...")
    # fallback
    html = html.replace(css_target.replace("\r\n", "\n"), css_replacement)
    print("CSS replaced via newline fallback!")

# Save back the html
with open("arc_preview.html", "w") as f:
    f.write(html)
print("Finished!")
