# Vaishnav AK — Portfolio

A Jekyll portfolio for data science and AI engineering, with a procedural animated homepage, detailed project stories, interactive architecture walkthroughs, and a dedicated résumé viewer. Published site: https://vaishnavak2001.github.io.

## Local preview

Requires Node.js 22 or newer. This path works without installing Ruby on Windows:

```sh
npm ci
npm run preview
```

Open http://127.0.0.1:4178. Stop with Ctrl+C. After editing content or templates, run `npm run build:preview` in another terminal and refresh the browser. The preview renders only the Liquid/Jekyll features used by this project; the production build remains Jekyll.

## Production build

With Ruby and Bundler installed:

```sh
bundle install
bundle exec jekyll build --strict_front_matter
npm run serve:built
```

`serve:built` serves the existing `_site` output without re-rendering it. Publishing uses the repository’s existing GitHub Pages configuration. Local preview and validation commands do not publish changes.

## Checks

```sh
npm test
npm run test:browser
```

Build first and run the preview server for browser checks. Browser tests require an installed Google Chrome and verify a portfolio-specific response header before interacting with the local server. They cover desktop/mobile layouts, local request failures, accessibility, filters, step navigation, résumé download, reduced motion, and no-JavaScript content. Captures and reports are written to ignored `local_scratch/`.

The check workflow runs a real Jekyll build and link/content checks on pull requests or manual dispatch. It does not deploy.

## Updating content

- `_data/portfolio.json`: biography, career, qualifications, contact links, and the default résumé path.
- `_data/case_studies.json`: curated case studies, attribution, project diagrams, and evidence context. Each entry needs a matching `_work/<slug>.md` with `title`, `project`, and `description` front matter.
- `_data/repositories.json`: the complete public GitHub collection, with descriptions, technologies, format labels, and optional case-study links. Work search matches titles, repository names, descriptions, and technologies locally, without an API request. Set `home_personal: true` on a case study to include it in the homepage’s personal-project selection.
- `_data/walkthroughs.json`: fictional lab scenarios and step descriptions. These are visual explanations, with no company API or live AI connection.
- `resume/Vaishnav_AK_DS_AI_ATS.pdf`: the public résumé. See [the Overleaf workflow](docs/RESUME_WORKFLOW.md) for source editing and publication.
- [Content sources](docs/CONTENT_SOURCES.md) records provenance and the distinction between reported outcomes and design targets.
- [GitHub review](docs/GITHUB_REVIEW.md) records the 38-repository inventory, sampled implementation evidence, and treatment of early concepts.

Company projects are credited as team work at chargeMOD, with Vaishnav as a contributing AI engineer. Preserve outcome qualifications and do not add private operational details.

## Design and assets

[DESIGN.md](DESIGN.md) records colors, type, layout, and motion. The homepage sculpture is browser-rendered geometry with selectable states, pause controls, and reduced-motion support. It stops rendering when out of view or when the tab is hidden. The rest of the site remains usable without JavaScript.

Fonts are self-hosted under `assets/fonts/` with their open-source licenses. The portrait derives from the existing owner-provided image. The generated mockups under `.impeccable/mocks/` are references, not runtime assets. `npm run capture:social` regenerates the social preview from the local site using Chrome.

Earlier project data, layouts, and the legacy résumé PDF remain in the repository for reference and existing file links. New pages use the portfolio layout and curated data above.
