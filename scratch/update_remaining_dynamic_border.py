with open("arc_preview.html", "r") as f:
    html = f.read()

# 1. Update the reflective card border gradient to use the dynamic metal bezel variable
card_border_target = """    /* Premium reflective gradient border */
    .sci-fi-card::before {
      content: '';
      position: absolute;
      inset: 0;
      border-radius: 24px;
      padding: 1.5px; /* Border thickness */
      background: linear-gradient(135deg, 
        rgba(var(--theme-glow-color), 0.55) 0%, 
        rgba(255, 255, 255, 0.12) 30%, 
        rgba(255, 255, 255, 0.03) 70%, 
        rgba(var(--theme-glow-color), 0.45) 100%
      );
      -webkit-mask: 
        linear-gradient(#fff 0 0) content-box, 
        linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      pointer-events: none;
      z-index: 10;
    }"""

card_border_replacement = """    /* Premium reflective gradient border matching the level-specific metal bezel */
    .sci-fi-card::before {
      content: '';
      position: absolute;
      inset: 0;
      border-radius: 24px;
      padding: 2px; /* Border thickness */
      background: var(--theme-bezel); /* Dynamic metal frame for the entire card! */
      -webkit-mask: 
        linear-gradient(#fff 0 0) content-box, 
        linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      pointer-events: none;
      z-index: 10;
    }"""

if card_border_target in html:
    html = html.replace(card_border_target, card_border_replacement)
    print("Card outer border updated to dynamic metal bezel!")
else:
    # Try direct newline normalized replace
    html = html.replace(card_border_target.replace("\r\n", "\n"), card_border_replacement)
    print("Card outer border updated via newline normalization!")

# 2. Update JavaScript level action to dynamically change the role string inside the card code area
js_target = """    // Level buttons action
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

js_replacement = """    // Level buttons action
    document.querySelectorAll('.level-select-btn').forEach(btn => {
       btn.addEventListener('click', () => {
          document.querySelectorAll('.level-select-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');

          const lvl = parseInt(btn.getAttribute('data-level'));

          document.getElementById('badge-number').textContent = lvl;
          document.getElementById('code-level-num').textContent = lvl;

          // Dynamically update the role string in the card code editor area
          const roles = {
             1: '"Arc Initiate"',
             2: '"Arc Specialist"',
             3: '"Arc Master"',
             4: '"Arc Commander"',
             5: '"Arc Creator"'
          };
          document.getElementById('code-role-str').textContent = roles[lvl];

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
