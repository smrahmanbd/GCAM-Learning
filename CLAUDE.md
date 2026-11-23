# Notes for Claude

## Git
- After finishing a task, commit and push straight to `main` without asking. Pushing to `main` publishes the site through `.github/workflows/deploy.yml`.
- Write clear commit messages that say what changed and why.
- Never commit secrets (API keys, ecoinvent credentials, premise keys, `.env` files).

## Site
- Module pages, go pages, the toolkit, glossary, models and spiral pages are generated: edit `content/*.json` or `build.py`, then run `python3 build.py`. Do not hand-edit those HTML files.
- Paper studies live in `papers/` (hand-written HTML/JS), with downloads in `downloads/papers/` and code in `labs/papers/`. Link new ones from the "Paper studies" list in `build.py`.
- Explorers and toy models use illustrative numbers; say so on every page.

## Daily paper study (scheduled task)
- One peer-reviewed **journal article** per day on GCAM and transport (GCAM transport, vehicle electrification, freight, aviation/shipping fuels, mode choice, transport emissions or policy in GCAM). Prefer open access and easy-to-follow papers. Never repeat a DOI already in `papers/papers.json`. If no suitable GCAM paper is left, take a transport paper using another IAM and say so on the page.
- Read the article itself (open the DOI or publisher page) before writing. Summarise in your own words: no copied figures or tables, and quotes under 15 words.
- Output: `papers/<slug>/index.html`, self-contained, styled with `../../assets/css/site.css` and `../plca.css`, and it may reuse `../plca-common.js` (quiz, canvas helpers). Sections, in order: the paper in one minute; learning goals; words you need (plain glossary); the question; how the model works (animated diagram); an interactive explorer with a small illustrative toy model; what they found; predict-then-check; a worked mini-exercise with a reveal; a 5-question quiz with explanations; limitations; link to the course (module pages) and to GCAM; review questions from 2–3 earlier papers in `papers/papers.json`; sources.
- Add an entry to `papers/papers.json` (slug, date, title, citation, doi, iam, topics, level, pages, takeaways, review). Test the page in a headless browser for script errors, then commit and push to `main`.
