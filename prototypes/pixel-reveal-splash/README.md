# Pixel Reveal Splash Screen

A self-contained homepage splash screen prototype: a background image sits under a
solid overlay color, and moving the cursor erases square grid cells of the overlay
to reveal the image beneath, with a configurable trailing effect.

Open `index.html` in any browser — no build step or server needed.

## Controls (top-right panel)

- **Background** — drop or browse for your own image (e.g. V01.png). A procedural
  watercolor placeholder loads by default.
- **Overlay** — color and opacity of the covering layer (e.g. V02's light gray).
- **Grid** — cell size in pixels, and brush radius (how many cells the cursor
  reveals at once).
- **Trail** — *Fade back* mode restores the overlay after a configurable linger
  and fade duration; *Stay revealed* keeps erased cells open.
- **Reset** re-covers everything; **Reveal all** clears the overlay.

The panel can be hidden to preview the splash screen clean; the ✦ button brings
it back. All settings apply live.
