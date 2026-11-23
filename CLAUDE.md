# Notes for Claude

## Git
- After finishing a task, commit and push straight to `main` without asking. Pushing to `main` publishes the site through `.github/workflows/deploy.yml`.
- Write clear commit messages that say what changed and why.
- Never commit secrets (API keys, ecoinvent credentials, premise keys, `.env` files).

## Site
- Module pages, go pages, the toolkit, glossary, models and spiral pages are generated: edit `content/*.json` or `build.py`, then run `python3 build.py`. Do not hand-edit those HTML files.
- Paper studies live in `papers/` (hand-written HTML/JS), with downloads in `downloads/papers/` and code in `labs/papers/`. Link new ones from the "Paper studies" list in `build.py`.
- Explorers and toy models use illustrative numbers; say so on every page.
