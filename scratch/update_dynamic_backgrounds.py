with open("arc_preview.html", "r") as f:
    html = f.read()

# 1. Update the background gradients for level-1 through level-5 to match their themes
bg_css_target = """    .sci-fi-card.level-1 {
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

bg_css_replacement = """    .sci-fi-card.level-1 {
      --theme-primary: #00f0ff; /* Turquoise / Cyan */
      --theme-glow-color: 0, 240, 255;
      --theme-bezel: linear-gradient(135deg, #a8703c 0%, #5e3a15 40%, #1c0e02 70%, #dca06c 100%); /* Bronze */
      --theme-card-bg: linear-gradient(145deg, rgba(4, 14, 25, 0.98) 0%, rgba(8, 12, 22, 0.96) 100%); /* Dark Blue space */
    }
    .sci-fi-card.level-1 .hud-badge-logo-img {
      filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)) drop-shadow(0 0 4px rgba(var(--theme-glow-color), 0.4)); /* Original blue/cyan */
    }
    .sci-fi-card.level-2 {
      --theme-primary: #c084fc; /* Purple */
      --theme-glow-color: 192, 132, 252;
      --theme-bezel: linear-gradient(135deg, #b0bec5 0%, #6d5b4b 40%, #201a14 70%, #a8886d 100%); /* Bronze-Silver */
      --theme-card-bg: linear-gradient(145deg, rgba(16, 6, 25, 0.98) 0%, rgba(12, 8, 20, 0.96) 100%); /* Deep Violet space */
    }
    .sci-fi-card.level-2 .hud-badge-logo-img {
      filter: hue-rotate(60deg) saturate(1.2) drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)); /* Shifts blue bezel to purple */
    }
    .sci-fi-card.level-3 {
      --theme-primary: #ff007f; /* Magenta / Pink */
      --theme-glow-color: 255, 0, 127;
      --theme-bezel: linear-gradient(135deg, #e2e8f0 0%, #64748b 40%, #1e293b 70%, #cbd5e1 100%); /* Silver */
      --theme-card-bg: linear-gradient(145deg, rgba(20, 2, 15, 0.98) 0%, rgba(14, 5, 12, 0.96) 100%); /* Deep Magenta space */
    }
    .sci-fi-card.level-3 .hud-badge-logo-img {
      filter: hue-rotate(110deg) saturate(1.3) drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)); /* Shifts blue bezel to magenta/pink */
    }
    .sci-fi-card.level-4 {
      --theme-primary: #22c55e; /* Green */
      --theme-glow-color: 34, 197, 94;
      --theme-bezel: linear-gradient(135deg, #fef08a 0%, #6b7280 40%, #1f2937 70%, #d1d5db 100%); /* Silver-Gold */
      --theme-card-bg: linear-gradient(145deg, rgba(2, 20, 10, 0.98) 0%, rgba(4, 14, 8, 0.96) 100%); /* Deep Green space */
    }
    .sci-fi-card.level-4 .hud-badge-logo-img {
      filter: hue-rotate(260deg) saturate(1.2) brightness(1.1) drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)); /* Shifts blue bezel to green */
    }
    .sci-fi-card.level-5 {
      --theme-primary: #eab308; /* Gold */
      --theme-glow-color: 234, 179, 8;
      --theme-bezel: linear-gradient(135deg, #ffe066 0%, #b38600 40%, #332600 70%, #ffd11a 100%); /* Gold */
      --theme-card-bg: linear-gradient(145deg, rgba(24, 18, 2, 0.98) 0%, rgba(16, 12, 4, 0.96) 100%); /* Rich Amber space */
    }
    .sci-fi-card.level-5 .hud-badge-logo-img {
      filter: hue-rotate(210deg) saturate(1.5) brightness(1.2) drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)); /* Shifts blue bezel to gold */
    }"""

if bg_css_target in html:
    html = html.replace(bg_css_target, bg_css_replacement)
    print("Background target variables injected successfully!")
else:
    html = html.replace(bg_css_target.replace("\r\n", "\n"), bg_css_replacement)
    print("Background target variables injected via newline normalization!")

# 2. Update card default background gradient definition to use the new --theme-card-bg variable
card_style_target = """    .sci-fi-card {
      width: 540px;
      height: 310px;
      background: 
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.99' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.09'/%3E%3C/svg%3E"),
        repeating-linear-gradient(rgba(var(--theme-glow-color), 0.02) 0px, rgba(var(--theme-glow-color), 0.02) 1px, transparent 1px, transparent 3px), /* CRT Scanlines dynamic */
        linear-gradient(145deg, rgba(4, 6, 15, 0.97) 0%, rgba(12, 17, 34, 0.94) 100%);
      border-radius: 24px;
      position: relative;
      padding: 32px 24px 24px 24px; /* Üst başlık için boşluk ayarı */
      display: flex;
      gap: 24px;
      border: 2px solid rgba(255, 255, 255, 0.08); /* Şık metalik çerçeve */
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.45);
      overflow: hidden;
      transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }"""

card_style_replacement = """    .sci-fi-card {
      width: 540px;
      height: 310px;
      background: 
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.99' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.09'/%3E%3C/svg%3E"),
        repeating-linear-gradient(rgba(var(--theme-glow-color), 0.02) 0px, rgba(var(--theme-glow-color), 0.02) 1px, transparent 1px, transparent 3px), /* CRT Scanlines dynamic */
        var(--theme-card-bg, linear-gradient(145deg, rgba(4, 6, 15, 0.97) 0%, rgba(12, 17, 34, 0.94) 100%));
      border-radius: 24px;
      position: relative;
      padding: 32px 24px 24px 24px; /* Üst başlık için boşluk ayarı */
      display: flex;
      gap: 24px;
      border: 2px solid rgba(255, 255, 255, 0.08); /* Şık metalik çerçeve */
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.45);
      overflow: hidden;
      transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }"""

if card_style_target in html:
    html = html.replace(card_style_target, card_style_replacement)
    print("Background template style updated to dynamic!")
else:
    html = html.replace(card_style_target.replace("\r\n", "\n"), card_style_replacement)
    print("Background template style updated via newline normalization!")

# 3. Update level selector buttons styles so active buttons dynamically shine in the respective level color
btn_active_target = """    .level-select-btn.active {
      background: rgba(15, 23, 42, 0.9);
      border-color: rgba(var(--theme-glow-color), 0.2);
      border-bottom: 2.5px solid rgba(var(--theme-glow-color), 0.95); /* Alttaki neon parlama çizgisi */
      color: #fff;
      text-shadow: 0 0 8px rgba(var(--theme-glow-color), 0.4);
      box-shadow: 
        inset 0 1px 1px rgba(255, 255, 255, 0.1),
        0 4px 15px rgba(var(--theme-glow-color), 0.1);
    }"""

# Dynamic button styles that inherit container colors (since active class button is outside card we target selector buttons directly via variables on container level in JS)
# We will update Javascript level switcher to also apply a global theme variable or color styles on page levels!
# Or we can simply add color style dynamically on active buttons in JS!
# Let's inspect the active buttons style in CSS to make it use the theme colors dynamically
# By wrapping buttons inside `.card-wrapper.level-1` we can theme them!
# Yes, let's update HTML card wrapper class so that wrapper handles level!
# Currently Javascript does:
# const card = document.getElementById("card-to-export");
# card.classList.remove('level-1', 'level-2', ...); card.classList.add('level-' + lvl);
# If we toggle it on the wrapper `.card-wrapper` instead, then BOTH the card AND the buttons can use the variables!
# Let's check wrapper id/class in HTML

with open("arc_preview.html", "w") as f:
    f.write(html)
print("Finished!")
