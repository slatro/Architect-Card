# 🧾 Arc Architect Card

> Your on-chain identity, forged in steel.

A sci-fi developer ID card generator for the [Arc Network](https://x.com/arc) community. Enter your X username, pick your Architect tier, and download a high-res PNG card stamped with your unique serial number.

**Live:** [architect-card.vercel.app](https://architect-card.vercel.app/)

---

## Features

- 🪪 **Auto-syncs your X profile picture** via username input
- 🏆 **5 Architect tiers** — each with a distinct metallic theme
  - `I` Bronze · `II` Iron · `III` Silver · `IV` Gilded · `V` Gold
- 🔢 **Unique serial number per card** — globally shared counter (AC-001, AC-002…)
- 🎨 **CRT scanline & noise overlay** — retro-neon sci-fi aesthetic
- 📥 **Export as high-res PNG** (3× pixel ratio)
- 🐦 **One-click Share to X** with pre-filled tweet

---

## Tiers

| # | Label | Theme |
|---|-------|-------|
| Architect I | Arc Initiate | Bronze |
| Architect II | Arc Specialist | Iron |
| Architect III | Arc Master | Silver |
| Architect IV | Arc Commander | Gilded |
| Architect V | Arc Legend | Gold |

---

## Tech Stack

- Vanilla HTML / CSS / JavaScript
- [`html-to-image`](https://github.com/bubkoo/html-to-image) for PNG export
- [`counterapi.dev`](https://counterapi.dev) for shared serial numbering
- [`unavatar.io`](https://unavatar.io) + `images.weserv.nl` proxy for X avatars

---

## Local Development

No build step required — just open the file:

```bash
git clone https://github.com/slatro/Architect-Card.git
cd Architect-Card
open arc_preview.html
```

---

## Deploy

Deployable to any static host (Vercel, Netlify, GitHub Pages). The project is a single `arc_preview.html` file with no dependencies to install.

---

Built with 🖤 for the Arc community.
