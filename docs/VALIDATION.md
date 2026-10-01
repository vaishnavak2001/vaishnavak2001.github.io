# Validation record

The redesign was built and reviewed locally, then approved by the owner for finalization. This record describes the pre-publication checks; repository history and GitHub Pages deployment status record publication.

## Build and content

- Real Jekyll 3.10.0 `Site#process` completed with strict front matter using a portable local Ruby 3.3 runtime and the installed rendering dependencies. Optional native live-reload dependencies were not used. Standard deployment remains `bundle exec jekyll build` on GitHub Pages/Linux.
- The separate Node/Liquid preview also rendered the same 15 page routes. It is a local convenience, not the production compiler.
- `npm test` passed local HTML link/asset targets, case-study presence, attribution, and outcome qualifications across all 15 pages.
- JavaScript syntax checks and `git diff --check` passed.

## Browser checks

Headless Chrome tested 1440×1000 desktop and 390×844 mobile layouts on Home, Work, a company case study, Lab, About, Resume, and 404. Checks passed for:

- No horizontal page overflow or local resource errors on tested routes.
- Axe WCAG 2 A/AA and WCAG 2.1 AA scan: no detected violations. This is automated evidence, not a claim of exhaustive accessibility certification.
- Mobile menu opening/closing, Escape behavior, project filters, walkthrough boundaries/replay, and PDF download.
- Reduced-motion initial state and useful no-JavaScript navigation and complete walkthrough transcripts.
- A separate motion check confirmed advancing canvas frames, stable frames while paused, shape changes while paused, correct project links, and runtime reduced-motion preference changes.

All valid captures and the browser report are under ignored `local_scratch/`. The preview and browser checks use port 4178 and verify the `X-Portfolio-Preview` header before capture or interaction. An initial capture against an occupied unrelated port was discarded; it is not validation evidence.

## Visual review

A separate finish reviewer identified and then scored corrections for sculpture density/framing, support and analytics diagrams, metadata placement, and tracking. The final verdict marked those listed fixes resolved. That verdict does not establish pixel-exact reproduction or full-surface certification.

The mechanical Impeccable detector returned no findings on the supplied files. It warned that a Liquid stylesheet reference could not be resolved automatically; the CSS was also supplied directly. Asset provenance scan found zero missing records across the new raster assets and mockups.

## Boundaries

No company reference source files were edited, no company source code was copied into the portfolio, and no live company integration is included. Company outcomes are explicitly attributed to supplied resume reporting. Voice latency is presented as a design target.

The deployment workflow checks pull requests and manual runs only. Publication remains a separate action.
