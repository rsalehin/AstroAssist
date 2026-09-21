# UI / UX

## Model
A **workbench**, not a chat window: Jupyter + Aladin + research chat. Desktop-first (≥ 1280 px). Dark theme default; light theme supported. WCAG-AA contrast, full keyboard navigation, colorblind-safe plot palettes.

## Layout
```
┌────────────────────────────────────────────────────────────────────────┐
│ ▣ Workspace: AD Leo flare study   ⌘K Search/commands       ⚙ Settings  │
├──────────────┬─────────────────────────────────┬───────────────────────┤
│ WORKSPACE    │ CHAT                            │ ARTIFACT VIEWER       │
│ Objects      │  user message                   │ tabs: Table · Plot ·  │
│  ● AD Leo    │  ↳ answer with inline cards     │ FITS · Sky (Aladin) · │
│ Data         │    [ScientificValue] [Plot]     │ Query · Code · Paper  │
│  ▦ Gaia DR3  │    [Query ▸ View ADQL]          │                       │
│  ▦ TESS S45  │  approval dialog (when needed)  │ toolbar: export ·     │
│ Plots        │                                 │ rerun · show code ·   │
│ Calculations │ composer: NL + /commands + @refs│ pin                   │
│ Papers       │                                 │                       │
│ Jobs         │                                 │                       │
├──────────────┴─────────────────────────────────┴───────────────────────┤
│ RESEARCH TRACE  Resolved SIMBAD 243 ms · Gaia 1.4 s · …   JOBS: 1 run  │
└────────────────────────────────────────────────────────────────────────┘
```
Panels are resizable and collapsible; the viewer can pop out. Clicking a rail item opens it in the viewer and offers "insert reference into chat".

## Card types (inline in chat, expandable in viewer)
| Card | Content | Actions |
|---|---|---|
| Object | name, type, spectral type, RA/Dec (sexagesimal + deg), distance, aliases chip list | open in Sky, resolve query, pin |
| Scientific value | `4.965 ± 0.010 pc` · method · source chip · lineage link | convert unit, view query, copy |
| Table | paged grid, column units/UCDs, sort, filter, row count, source | export (FITS/ECSV/VOTable/CSV/Parquet/LaTeX), plot column, crossmatch |
| Query | source, protocol, ADQL/URL (collapsed), status, runtime, rows, bytes | copy, edit & rerun, view raw response |
| Plot | SVG (or Plotly), caption, version | show code, show data, edit (NL or spec), export SVG/PNG/PDF, regenerate |
| Paper | title, authors, year, journal, abstract (collapsed), citations, ADS/arXiv links, origin badge (ADS / LOCAL) | cite, open, find related |
| Citation | claim → sources | copy BibTeX |
| Observation | mission, instrument, band, exposure, obs id, proprietary flag, size | download (with confirm), preview, footprint on Sky |
| Code | proposed/executed code, stdout/stderr, outputs | Run / Edit / Cancel (proposal); rerun (executed) |
| Fit | model, parameters ± unc, χ²/red χ², residual thumbnail | plot residuals, export |
| Job | kind, status, progress, elapsed | cancel, open result |
| Disagreement banner | per-source values with uncertainties, likely reason | choose preferred, keep both |
| Fallback notice | unavailable source, fallback used, what was NOT retrieved | retry |
| Capability notice | missing extra / platform limit | install hint |

## Interaction rules
- Natural language is the default; slash commands are accelerators: `/resolve /query /cone /plot /fit /cite /export /plan`.
- `@` mentions reference workspace artifacts (`@AD Leo`, `@TESS S45`).
- Approvals appear inline in chat and block only the affected branch; chat stays usable.
- Every number rendered in an answer is a hover target showing unit, uncertainty, source; click opens the artifact.
- Long jobs move to the Jobs panel; a toast announces completion.
- Keyboard: `⌘/Ctrl+K` palette, `⌘/Ctrl+Enter` send/run, `Esc` close viewer, `[`/`]` toggle rails.

## Settings
Model provider + profile per role; credentials (keyring-backed, masked); risk thresholds; cache mode (online / prefer cache / offline); plot theme; LangSmith opt-in; kernel resource limits.

## Figma research plan
Audit six products before drawing: **ADS** (dense faceted search, paper scanning), **Aladin Lite** (layered spatial exploration), **ESASky** (source → sky → mission data), **Jupyter / Jupyter AI** (code/output adjacency, kernel state), **Perplexity** (inline citation placement), **Elicit** (paper-centric research workflow). For each: capture 5–8 screens, note the strongest interaction concept, the weakest, and what transfers.

Deliverables in Figma:
1. Component library: cards above, chips (source, unit, quality), disagreement banner, approval dialog, trace row, job row.
2. Workbench frames: empty state, day-one story mid-flight, approval pending, job running, disagreement, export.
3. Two themes with token set (color, type scale, spacing) exported for Tailwind.
4. Prototype of the AD Leo story click-through.

Design tokens are mirrored in `frontend/src/theme/tokens.ts`.
