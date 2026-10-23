# Module content schema (one JSON file per module: content/m<go><n>.json, e.g. content/m11.json)

Write in plain, friendly English (short sentences, define each term at first use). Facts must come from the course
research notes (/home/claude/course3/research/*.md) or the three handbooks' sources; keep their verification flags.

```jsonc
{
  "id": "1.1",                       // go.module
  "go": 1,                           // 1, 2 or 3
  "slug": "what-is-an-iam",          // page file name: modules/<slug>.html
  "title": "What an integrated assessment model is",   // ≤ 60 chars, sentence case
  "minutes": 30,                     // study time
  "tag": "Big picture",              // ≤ 14 chars, sentence case, says what kind of module it is
  "systems": ["economy","energy"],   // which GCAM systems it touches: economy|energy|land|water|climate|policy (1-6)
  "summary": "…",                    // ≤ 220 chars, shown on cards
  "outcomes": ["…"],                 // 3-5 "you can …" statements, ≤ 110 chars each
  "narration_en": "…",               // 120-220 words, spoken overview read aloud by the browser; no symbols, no URLs
  "narration_ar": "…",               // faithful Modern Standard Arabic translation of narration_en
  "diagram": {                       // interactive diagram, canvas 900 x 520 units, (x,y) = box CENTRE
    "title": "…", "caption": "what to notice, ≤ 200 chars",
    "nodes": [ {"id":"gdp","label":"GDP","sub":"≤ 40 chars","x":120,"y":90,"w":170,"h":64,
                "sys":"economy",     // economy|energy|land|water|climate|policy|data|neutral (colour)
                "detail":"HTML ≤ 450 chars shown when the box is clicked"} ],
    "edges": [ {"from":"gdp","to":"energy","label":"≤ 24 chars","sys":"economy"} ],
    "tour":  [ {"focus":["gdp"],"edges":[["gdp","energy"]],"text":"≤ 220 chars caption for this step"} ]   // 4-8 steps
  },
  "components": {                    // optional table (3-9 rows)
    "caption": "…", "rows": [ {"name":"…","purpose":"…","analogy":"…"} ] },
  "sections": [ {"heading":"…","html":"…"} ],   // 3-7 sections; allowed tags: p ul ol li b strong i em code a table thead tbody tr th td sub sup br div.eq
                                                 // equations: <div class="eq">share<sub>i</sub> = …</div> (HTML + Unicode, no LaTeX)
  "callouts": [ {"after":0,"kind":"model|trap|gcam|research|try","title":"…","html":"…"} ],  // after = index of the section it follows
  "explorer": {"widget":"logit","intro":"what to do","predict":"a question to answer before touching it"},  // optional
  "code": [ {"title":"…","lang":"python|r|xml|bash",
             "file":"labs/go2/m23_logit.py",      // EITHER a file that exists in the site (see list below)…
             "source":"…",                        // …OR inline code (≤ 40 lines)
             "runnable":true,                     // python only, and only if it uses just numpy/scipy/pandas/matplotlib and no file reads
             "explain":"what it does / what to change", "expected":"short expected printed output"} ],
  "takeaways": ["…"],                // 3-6
  "quiz": [ {"q":"…","options":["…","…","…","…"],"answer":2,"explain":"…"} ],   // 3-5, vary the answer position
  "glossary": [ {"term":"…","def":"…"} ],      // 2-8 new terms
  "resources": [ {"title":"…","url":"https://…","why":"≤ 120 chars"} ],          // 2-6 verified links
  "downloads": [ {"label":"…","path":"downloads/…"} ]                             // optional; see list below
}
```

## Interactive explorer widgets available (use the id)
warming (emissions→warming via 0.45 °C/1000 Gt), budget (carbon budget bathtub), kaya (Kaya calculator),
market (toy market + carbon tax, lab 4 numbers), discount (discounting / DICE trade-off), matrix (SSP × RCP matrix),
logit (relative-cost logit shares, 3 techs + exponent), learning (learning curve → solar share), land (land for bioenergy,
profit-share), carbonprice (rising carbon price → cut on straight-line cost curve), lp (lab 11 linear program + shadow price),
disagree (two toy models disagree), ensemble (random ensemble + scenario-discovery box), cdr (carbon removal needed for a budget),
project (project planner), trncost (transport generalised cost incl. value of time + absolute-cost logit mode shares),
lmdi (LMDI decomposition of transport CO2 change), downscale (region→country convergence downscaling),
solver (watch a solver iterate prices until two linked markets clear), valuefactor (renewable value factor vs market share).

## Files available for code blocks (paths relative to site root)
labs/go2/m21_drivers.py|.R, m22_markets, m23_logit, m24_supply, m25_demand, m26_land, m27_water, m28_system, m28a_climate (each .py and .R);
labs/go2/gcam/read_gcam.py, read_gcam.R, go2_queries.xml;
labs/go3/toy/gcam_transport_toy.py|.R; labs/go3/xml/*.xml (trn_bev_cost_low, trn_loadfactor_up, trn_zev_shareweights,
trn_freight_truck_efficiency, policy_carbon_tax, policy_co2_constraint_netzero, policy_zev_standard), labs/go3/xml/scale_from_base.py;
labs/go3/config/batch_transport.xml, configuration_transport_snippet.xml; labs/go3/queries/transport_queries.xml;
labs/go3/analysis/{read_transport, decompose_lmdi, scenario_discovery}.py|.R, plot_transport.py, make_sample_data.py;
labs/go3/downscale/downscale_demo.py; labs/go3/templates/research_proposal.md, scenario_design_matrix.csv, reporting_checklist.md;
labs/iam-course/labs/lab1.R … lab14.R, labs/iam-course/solutions/lab9_solution.R … lab14_solution.R, labs/iam-course/gcam-files/*.

Python files that save figures with plt.savefig are fine to mark runnable (the page shows saved PNGs) IF they read no input
files: m21–m28a are pyodide-safe. Go 3 analysis scripts read CSVs → runnable:false (download instead), unless you paste a
self-contained inline version.

## Downloads available
downloads/Go1-Study-Guide-See-the-Whole-Picture.pdf, downloads/Go2-Component-Handbook-Open-the-Boxes.pdf,
downloads/Go3-Research-Handbook-GCAM-Transport.pdf, downloads/Course-Structure-3-Goes.pdf,
downloads/go2-kit.zip, downloads/go3-transport-kit.zip, downloads/iam-course-labs.zip,
downloads/slides/WeekNN-*.pdf/.pptx (15 weekly decks, e.g. downloads/slides/Week07-Inside-GCAM.pptx).

Validate with: python3 /home/claude/gcamsite/content/validate.py content/m11.json …
