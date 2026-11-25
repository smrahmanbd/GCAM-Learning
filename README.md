# GCAM in three goes

An open, interactive course on the **Global Change Analysis Model (GCAM)**, taught three times over, each time deeper:

| Go | Name | What you do |
| --- | --- | --- |
| 1 | Foundations | Click-through diagrams and predict-then-check explorers: what an integrated assessment model is, the climate chain, energy and emissions, prices, scenarios, and a tour of GCAM. |
| 2 | Build and Implement | Each GCAM component, its rule and its links to the others, with small models you run in the browser (Python) or in R. |
| 3 | Research Frontier | A research brief for each step of a GCAM transport study: model structure, literature, scenario design, add-on XML, analysis, downscaling and write-up. |

**Live site:** https://smrahmanbd.github.io/GCAM-Learning/

The **GCAM family** page (`gcam-family.html`) teaches the component models around the core (Hector, Xanthos, Tethys, Demeter, moirai, the land module, the economy and gcamdata) as beginner-friendly decks: one sentence, an animated step-through, an orbitable 3D scene (three.js), inputs and outputs, where it plugs in, a toy explorer and a quiz.

Every module has an interactive system diagram with a walkthrough, a spoken overview (English and Arabic, using the browser's voices), an explorer, code, a short quiz and further reading. Each go has an entry check, an exit check and a zooming mind map (with a PDF of the zoom path that can be imported into Prezi).

## Structure

- `index.html`, `go1.html`–`go3.html`, `modules/*.html`, `mindmap-go*.html`, `toolkit.html`, `glossary.html` — the site (plain HTML, CSS and JavaScript; no build step needed to host it).
- `content/family.py` — the GCAM family decks; `assets/js/family3d.js` draws their animations, 3D scenes and explorers (three.js r128 is vendored in `assets/js/vendor/`).
- `content/*.json` — the source of every module; `build.py` regenerates the pages (`python3 build.py`).
- `papers/` — paper studies: interactive pages, a study guide and an implementation guide. First study: Šimaitis et al. (2025) on car carbon footprints across 1.5–3 °C pathways (`papers/bev-plca-basics.html`, `papers/bev-plca.html`); slides and study guide PDF in `downloads/papers/`, teaching model in `labs/papers/`.
- `study-guide/` — *GCAM from Zero*, a beginner study guide (Markdown and web page) built from all course materials and the 2025 GCAM training notebooks.
- `labs/` — Go 2 toy models (Python and R), the Go 3 transport research kit, and the original R labs.
- `downloads/` — handbooks for each go, code kits, mind-map PDFs and weekly slides.
- `.github/workflows/deploy.yml` — publishes the site with GitHub Pages on every push to `main`.

## Notes

GCAM facts follow the GCAM v8.2 documentation and the gcam-core v9.1 source (released 2 June 2026). Explorers and toy models are teaching versions with illustrative numbers. The GCAM XML templates and reader scripts have not yet been run against a live GCAM installation. GCAM is developed by the Joint Global Change Research Institute (PNNL); this course is independent teaching material.
