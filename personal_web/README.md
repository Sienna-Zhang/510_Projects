# Sienna Zhang — Personal Website

Personal portfolio page for Sienna Zhang (张献戈), AI entrepreneur and UW MSTI student.

## How to Run

No build step required. This is a static website using vanilla HTML, CSS, and JavaScript.

**Option 1 — Open directly in browser:**
```
Open index.html in any modern web browser (Chrome, Firefox, Safari, Edge).
```

**Option 2 — Local development server (recommended for accurate font loading):**
```bash
# Using Python (built-in, no install needed):
python -m http.server 8000
# Then open: http://localhost:8000
```

```bash
# Using Node.js (if installed):
npx serve .
# Then open the URL shown in terminal
```

## Project Structure

```
personal-web-Sienna-Zhang/
├── index.html             # Main page (single-page, all sections)
├── styles.css             # All styles (CSS custom properties + responsive)
├── script.js              # Language toggle, hamburger menu, active nav
├── background.jpg         # Subtle full-page background texture
├── thoth.png              # Thoth · T-Mobile Hackathon card image
├── planning.png           # Weekend Planning Agent card image
├── crystal ball.png       # Mars · Crystal Ball card image
├── forked_life.png        # Personalized Decision Simulator card image
├── AIGC generator.png     # AIGC Interior Design Generator card image
└── README.md              # This file
```

## Features

- **Bilingual (中/EN):** Click the language toggle in the nav to switch between Chinese and English instantly.
- **Responsive:** Adapts to mobile (< 640px), tablet (640–1024px), and desktop (> 1024px). Hamburger menu on mobile.
- **Accessible:** Keyboard navigable, ARIA labels, focus-visible styles, `prefers-reduced-motion` support, 44×44px minimum touch targets.
- **Dark mode:** `#0F0F0F` background with amber accent (`#FF6B35`). Single fixed theme.
- **No dependencies:** No frameworks, no build tools, no npm. Pure HTML5 + CSS3 + Vanilla JS.

## Sections

1. **Hero** — Name, identity tag, one-line tagline, scroll-down CTA.
2. **Background** — Vertical timeline of education and work experience.
3. **Works** — Grid of 5 AI projects with descriptions and tech tags.
4. **Footer** — Email and LinkedIn contact links.

## Design System

| Token | Value |
|-------|-------|
| Background | `#0F0F0F` |
| Surface | `#1A1A1A` |
| Text | `#F0F0F0` |
| Accent | `#FF6B35` (amber orange) |
| Headline font | Space Grotesk (Google Fonts) |
| Body font | DM Sans + Noto Sans SC |

## Customization

To update content, edit `index.html`:
- Every text element has `data-en="..."` and `data-zh="..."` attributes for bilingual content.
- LinkedIn URL: search for `href="#"` in the footer and replace with your actual LinkedIn URL.
- Project card images: update `.work-card__image--01` through `--05` in `styles.css`.
