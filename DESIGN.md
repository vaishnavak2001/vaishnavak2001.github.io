---
name: Vaishnav AK - Spatial AI studio
description: Computational geometry above a warm editorial portfolio of team-built AI and data systems.
colors:
  paper: "#f1efe7"
  ink: "#152823"
  muted: "#596760"
  dark: "#101b19"
  mint: "#c0eddb"
  accent: "#d6ed8e"
  light-muted: "#aebfb6"
  line: "#c8cec4"
  dark-line: "#344740"
typography:
  display:
    fontFamily: "Space, 'Helvetica Neue', sans-serif"
    fontSize: "clamp(4.8rem,7.7vw,6rem)"
    fontWeight: 500
    lineHeight: 0.99
    letterSpacing: "-.04em"
  headline:
    fontFamily: "Space, 'Helvetica Neue', sans-serif"
    fontSize: "clamp(2.7rem,5vw,4.5rem)"
    fontWeight: 500
    lineHeight: 1.08
    letterSpacing: "-.04em"
  title:
    fontFamily: "Space, 'Helvetica Neue', sans-serif"
    fontSize: "clamp(1.6rem,2.6vw,2.3rem)"
    fontWeight: 500
    lineHeight: 1.08
    letterSpacing: "-.04em"
  body:
    fontFamily: "Space, 'Helvetica Neue', sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Space, 'Helvetica Neue', sans-serif"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: ".015em"
  expressive:
    fontFamily: "Instrument, Georgia, serif"
    fontWeight: 400
    letterSpacing: "-.025em"
rounded:
  diagram-small: "4px"
  diagram-node: "8px"
  media: "12px"
  filter: "30px"
  circle: "50%"
spacing:
  gutter: "clamp(24px,5vw,88px)"
  gutter-mobile: "24px"
  section: "100px"
  section-mobile: "65px"
  control-gap: "24px"
  heading-gap: "40px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    padding: "14px 22px"
  text-link:
    padding: "0 0 3px"
  contact-link:
    padding: "9px 16px"
  contact-link-hover:
    backgroundColor: "{colors.mint}"
    textColor: "{colors.ink}"
  filter:
    textColor: "{colors.ink}"
    rounded: "{rounded.filter}"
    padding: "8px 18px"
  filter-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.filter}"
    padding: "8px 18px"
  navigation:
    textColor: "{colors.paper}"
  tag:
    textColor: "{colors.muted}"
    padding: "0 0 3px"
  project-media:
    rounded: "{rounded.media}"
    padding: "34px"
  walkthrough-step:
    backgroundColor: "{colors.dark}"
    textColor: "{colors.light-muted}"
    rounded: "{rounded.circle}"
    size: "48px"
  walkthrough-step-selected:
    backgroundColor: "{colors.mint}"
    textColor: "{colors.ink}"
    rounded: "{rounded.circle}"
    size: "48px"
---

# Design System: Vaishnav AK

## Overview

**Creative North Star: "Spatial AI studio"**

A dark spatial AI studio connects to warm editorial reading surfaces. Large grotesk headlines, expressive italic serif words, mint geometry, and restrained citron active states make the work approachable while preserving a technical character. Borders and generous space give the narrative structure.

The accepted first concept establishes the dark hero, light work, and dark lab sequence. The user's request for more modern, attractive animation informs the denser procedural sculpture. Conventional links and readable project evidence remain central. Company work retains visible team attribution; conceptual diagrams and fictional lab scenarios must not suggest company screenshots or live connections.

**Key Characteristics:**
- Dark animated introduction, warm editorial work, dark walkthrough lab.
- Self-hosted grotesk type with selective italic serif emphasis.
- Ruled project layouts and diagrams that explain systems.
- Optional motion with accessible static content and conventional navigation.

This record is extracted from `assets/css/portfolio.css`, `assets/js/scene.js`, `_layouts/portfolio.html`, and `index.html`, reconciled with `PRODUCT.md` and the existing design direction. The original `.impeccable/mocks/home-concept.png` is the accepted structural reference; `.impeccable/mocks/home-bold-concept.png` is the refinement reference. No measured comp-diff or separate pixel-spec approval is claimed; `.impeccable/direction-contract.md` records those limitations.

## Colors

Warm paper and green-black ink anchor a muted botanical palette, with mint geometry and citron selection accents.

The sidecar's eight-step OKLCH ramps are synthesized preview metadata, not additional colors used by the stylesheet.

### Primary

- **Mint:** Expressive words on dark surfaces, selected walkthrough nodes, contact hover, and text selection. The canvas uses its own depth-dependent translucent green mixture, not a literal fill of this token.
- **Citron accent:** Pressed scene labels, signal dots, dark-surface focus, and wordmark punctuation.

### Neutral

- **Paper / Ink:** Reading background and foreground, inverted for primary actions and dark surfaces.
- **Dark:** Hero, lab, navigation on dark pages, and footer ground.
- **Muted / Light muted:** Supporting copy on light / dark surfaces respectively.
- **Line / Dark line:** Section divisions and quiet structural boundaries on their matching surfaces.

**The Surface Pairing Rule.** Use the matching foreground, secondary text, and rule colors for each surface; the dark surface swaps its muted and line roles together.

## Typography

**Display and body font:** Self-hosted Space Grotesk variable (CSS family alias `Space`), with Helvetica Neue and sans-serif fallbacks. The local face exposes weights 300 through 700.

**Expressive font:** Self-hosted Instrument Serif italic (CSS family alias `Instrument`), with Georgia and serif fallbacks. Italic is supplied by the face and semantic emphasis, not a separate schema token.

The pairing gives headings a precise grotesk structure and a softer expressive finish. Headlines use medium weight and tight tracking; body copy uses normal weight and an open line height.

### Hierarchy

- **Display:** The frontmatter records the hero headline. Its italic word grows to 1.18em with a .95 line height. At widths up to 1100px the hero is 5rem; up to 760px it uses `clamp(3.55rem,10.5vw,5.5rem)`.
- **Headline / Title:** The shared h2 / h3 ramp is recorded above. Work-index titles are 25px with 1.25 line height; case narrative headings are 36px, reducing to 30px on mobile.
- **Body:** Base copy is 16px, with 15px project summaries and 14px walkthrough detail. Paragraphs cap at 70ch.
- **Label:** Project metadata is 11px, reducing to 10px on mobile. Navigation is 14px and text links are 15px. Labels use normal case.

**The Expressive Word Rule.** Reserve Instrument Serif for emphasis within headings; keep body copy, navigation, metadata, and controls in Space Grotesk.

## Layout

Page sections are centered within a 1600px maximum width and use the gutter and section spacing tokens. The declared `--max:1440px` is unused in the inspected stylesheet and is not a container rule. Breakpoints are 760px for mobile, 1100px for the intermediate layout, and 1600px for large hero adjustments.

The desktop header is 100px tall. The hero uses a left copy layer and an absolutely positioned scene beginning at 32% of its width; it is viewport-height aware, with 700px minimum and 950px maximum height. At mobile widths the header wraps, the hero becomes a vertical sequence, and the sculpture occupies a 425px-tall block after the copy. Mobile hero minimum height is 970px.

Featured projects use a 1fr / 1.15fr split with a 70px gap, reducing to equal columns and a 35px gap at the intermediate breakpoint, then one column on mobile. The work index uses two columns with 64px row and 40px column gaps before becoming a single column. Case studies pair a 230px sticky aside with the narrative; mobile removes the sticky behavior and hides the aside navigation. Reading content remains in document order.

## Elevation & Depth

The stylesheet has no box-shadow vocabulary. Tonal surfaces, fine borders, overlapping point geometry, and perspective create depth. Media hover uses color and small transforms; the lab diagram lifts by 8px. The canvas supplies authored depth through projected points, connecting strokes, and varying alpha.

**The Ruled Surface Rule.** Separate reading sections with tonal contrast and fine rules; preserve the flat editorial treatment of project content.

## Shapes

Media and portraits use the media radius. Diagram nodes use the smaller node radii; project filters are rounded pills. Scene pause controls, signals, and walkthrough nodes use circles. Main rectangular actions and text links retain square edges. Diagram paths and orbit ellipses are native to the visual world and are not prohibited as decorative geometry.

## Components

### Buttons and links

The primary filled action uses ink on paper, compact 14px type, a matching 1px border, and the recorded padding. Hover changes its background to `#315044`. Text links carry a 1px underline and a 44px minimum height; their SVG arrow moves 6px horizontally on hover. Contact navigation uses a fine outline and switches to mint with ink text on hover. Global focus is a 2px `#49876b` outline with 6px offset, switching to citron on dark surfaces. Disabled buttons retain the shared .42 opacity and default cursor.

### Filters and tags

Filters are 44px minimum-height pill buttons. Pressed filters invert to ink and paper; hover strengthens the border. Technology tags are quiet 11px text with individual bottom rules, not filled chips. Company attribution remains adjacent to project headings and summaries.

### Project media and containers

Projects on the homepage are open ruled rows; the index uses image-led entries. Their rounded media contains abstract diagrams. Default media uses `#dfe5d8` with `#2b4d40` drawing color, shifting to `#d2ddca` on hover. Forecast and pipeline illustrations have their own muted surface variations. Desktop media has a 310px minimum height, reducing on smaller screens; these diagram-specific colors are not additional global brand accents.

### Navigation

The wordmark is 26px and the desktop navigation has a 36px gap. Hover and current-page states reveal a fine underline. At mobile widths JavaScript enables a 44px-minimum-height Menu control and a vertical dropdown; without enhancement, navigation wraps and stays available. Contact, Work, and Resume remain conventional links.

### Procedural scene

Data is a lattice, Prediction a patterned sphere, Agent a twisted toroidal shell, and Action a flowing sheet. Each pressed state updates explanatory text and its related project link. Rendering uses 7200 points, or 3200 when the initial viewport is at most 760px; device pixel ratio caps at 1.75. Pointer tilt ignores touch and reduced motion. Pause stops the loop; offscreen and hidden tabs stop rendering. Reduced motion starts paused and applies shape changes immediately. CSS orbit geometry supplies the static fallback.

The hero headline enters over 1.3s using the shared ease; walkthrough details use .5s. Diagram hover transitions range from .6s to .8s, and the lab dashed path loops over 20s. Reduced motion removes CSS animations and transitions, disables smooth scrolling, and suppresses the lab and forecast hover transforms.

### Walkthrough and resume

Walkthrough step controls use connected circular nodes with mint pressed states. Details sit below the sequence; explicit previous/next controls and a complete text transcript support linear reading. The dark scenario panel uses the media radius with `#1b2b24` fill. Resume actions use the shared action styles above a bordered PDF viewer and an HTML summary. No text-input component is present in the inspected system.

## Do's and Don'ts

### Do:

- **Do** retain the dark hero, light editorial work, and dark lab sequence.
- **Do** keep team attribution and outcome context visible beside project evidence.
- **Do** use self-hosted Space Grotesk and Instrument Serif in their established roles.
- **Do** retain visible focus, conventional links, static fallback content, and reduced-motion behavior.
- **Do** label conceptual diagrams and fictional walkthroughs honestly.

### Don't:

- **Don't** introduce live AI, company connections, or game navigation into the portfolio.
- **Don't** add scroll hijacking, forced loading sequences, custom cursors, or text hidden pending animation.
- **Don't** replace editorial project rows with repeated dashboard cards or decorative shadows.
- **Don't** treat generated mockup wording or incidental imagery as evidence of real work.
- **Don't** represent the refinement mockup as a separately approved pixel specification.
