# Pixel Reveal Splash Screen

A self-contained homepage splash screen prototype: a background image sits under a
solid overlay color, and moving the cursor erases square grid cells of the overlay
to reveal the image beneath, with a configurable trailing effect.

Open `index.html` in any browser — no build step or server needed.

## Controls (top-right panel)

- **Background** — drop or browse for your own image (e.g. V01.png). A procedural
  recreation of the V01 watercolor (indigo ring, teal centre, pink bloom) loads
  by default. Alternatively pick a solid background color; "Use image" switches
  back to the image.
- **Overlay** — color and opacity of the covering layer (e.g. V02's light gray).
- **Grid** — cell size in pixels, brush radius (how many cells the cursor
  reveals at once), and cell outline thickness and color (0 = no outlines).
- **Scatter** — random cells revealed around the cursor rather than strictly
  under it: radius sets how far they spread, density how many appear per move.
- **Trail** — *Fade back* mode restores the overlay after a configurable linger
  and fade duration; *Stay revealed* keeps erased cells open.
- **Tease** — while the cursor is idle, a random patch of the image pops through
  at the chosen interval and fades back, hinting that the page is interactive.
  Teaser reveals always fade, even in *Stay revealed* mode. 0 = off.
- **Reset** re-covers everything; **Reveal all** clears the overlay.

The panel can be hidden to preview the splash screen clean; the ✦ button brings
it back. All settings apply live.
