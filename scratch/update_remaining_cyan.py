import re

# Read current html content
with open("arc_preview.html", "r") as f:
    html = f.read()

# Define replacement for Level styles containing CRT lines background using the theme color variables
css_target = """    .sci-fi-card {
      width: 540px;
      height: 310px;
      background: 
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.99' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.09'/%3E%3C/svg%3E"),
        repeating-linear-gradient(rgba(0, 240, 255, 0.02) 0px, rgba(0, 240, 255, 0.02) 1px, transparent 1px, transparent 3px), /* CRT Scanlines */
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

css_replacement = """    .sci-fi-card {
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

if css_target in html:
    html = html.replace(css_target, css_replacement)
    print("Background CRT Scanlines variable updated successfully!")
else:
    # Try direct newline normalized replace
    html = html.replace(css_target.replace("\r\n", "\n"), css_replacement)
    print("Background CRT Scanlines variable updated via newline normalization!")

# Replace all level button borders/glows so they match the dynamic theme variables instead of hardcoded cyan
# Active levels button border-bottom and text-shadow
html = html.replace("border-bottom: 2.5px solid rgba(0, 240, 255, 0.95); /* Alttaki neon parlama çizgisi */", "border-bottom: 2.5px solid rgba(var(--theme-glow-color), 0.95); /* Alttaki neon parlama çizgisi */")
html = html.replace("text-shadow: 0 0 8px rgba(0, 240, 255, 0.4);", "text-shadow: 0 0 8px rgba(var(--theme-glow-color), 0.4);")
html = html.replace("0 4px 15px rgba(0, 240, 255, 0.1);", "0 4px 15px rgba(var(--theme-glow-color), 0.1);")
html = html.replace("border-color: rgba(0, 240, 255, 0.2);", "border-color: rgba(var(--theme-glow-color), 0.2);")
html = html.replace("border-bottom-color: rgba(0, 240, 255, 0.7);", "border-bottom-color: rgba(var(--theme-glow-color), 0.7);")

# Action download button border-bottom and shadows
html = html.replace("border-bottom: 2.5px solid rgba(0, 240, 255, 0.95);", "border-bottom: 2.5px solid rgba(var(--theme-glow-color), 0.95);")
html = html.replace("box-shadow: 0 4px 15px rgba(0, 240, 255, 0.2);", "box-shadow: 0 4px 15px rgba(var(--theme-glow-color), 0.2);")
html = html.replace("border-bottom-color: rgba(0, 240, 255, 0.9);", "border-bottom-color: rgba(var(--theme-glow-color), 0.9);")
html = html.replace("box-shadow: 0 4px 15px rgba(0, 240, 255, 0.15);", "box-shadow: 0 4px 15px rgba(var(--theme-glow-color), 0.15);")

# Also let's make sure the custom logo has a dynamic neon glow shadow to match the level!
logo_img_style_target = """    /* Centered Arc logo image with clean scaling and drop shadow */
    .hud-badge-logo-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8)) drop-shadow(0 0 4px rgba(var(--theme-glow-color), 0.4));
    }"""

# Write modified HTML back
with open("arc_preview.html", "w") as f:
    f.write(html)
print("Finished!")
