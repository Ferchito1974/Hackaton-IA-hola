# Which Door You Walk Through

**An audit of whether consumer chatbots warn about risks users did not ask about.**
Research conducted at the [AI x Epistemics Research Sprint](https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15) (Apart Research, 13–15 Nov 2026).

📄 **Paper:** [`paper/which_door_you_walk_through.pdf`](paper/which_door_you_walk_through.pdf) · 🖥️ **Demo app:** `app/index.html` · 📊 **Results:** [`resultados/resumen.md`](resultados/resumen.md)

## The question
People ask chatbots for ordinary tasks (a breakfast plan, a pill organizer, a cleanup script) without asking about the risk hidden inside. Do chatbots warn on their own, like the "guardian angels" proposed by Forethought, or do they just do what they are asked?

## What we did
- **13 Spanish prompts with a hidden risk** (health, engineering, software; simple, medium, complex) + **1 no-risk control**. Texts and evidence-based answer key: [`piloto/bateria_prompts.md`](piloto/bateria_prompts.md).
- **5 runs per prompt, each in a new chat**, on the Gemini app (logged out), ChatGPT (logged out) and Claude (free account, incognito): 210 responses. Exploratory: Google Search AI Mode on 4 prompts (20 responses).
- **Two raters blind to the app** judged: does it warn? is the final plan safe? does it give false reassurance? (Cohen's κ = 0.42; 38 disagreements adjudicated.)

## Main results
| App | Clear warning | Final plan safe | False reassurance |
|---|---|---|---|
| Gemini app, logged out | **82%** (53/65) | **75%** | 9 |
| ChatGPT, logged out | 97% (63/65) | 100% | 0 |
| Claude, free account | 98% (64/65) | 95% | 3 |
| Google AI Mode (exploratory) | 95% (19/20) | 90% | 2 |

- Gemini warned less than ChatGPT (p = 0.009) and Claude (p = 0.002).
- **Same provider, different door:** on the same 4 prompts, the Gemini app warned in 8/20 and Google's AI Mode in 19/20 (p = 0.0004).
- Gemini failed on **everyday** risks (grapefruit + statin, load-bearing wall, toddler choking), not on technical ones (7/15 simple vs 15/15 medium).
- ChatGPT over-warns on the control (4/5 false alarms).

![Figure 1](resultados/fig1_mapa_aviso.png)

## Repository layout
| Path | Contents |
|---|---|
| `paper/` | Final report (PDF and DOCX) |
| `piloto/` | Prompt battery with answer key, and the 13 Nov pilot |
| `datos/respuestas/` | All 230 responses, verbatim, with model, date and time |
| `datos/capturas/` | Screenshot of each run (from the moment screenshots were enabled) |
| `datos/respuestas.csv` | One row per response (app, model, session, prompt, run, file, notes) |
| `datos/HUELLAS.sha256` | SHA-256 of every response and screenshot |
| `clasificacion/` | Blind texts, both raters' sheets, adjudication (`consenso.csv`), final labels and the code→app key (`CLAVE_NO_ABRIR.csv`) |
| `resultados/` | Tables, `resumen.md`, `resultados.json` and figures |
| `app/` | Demo: same request, four answers side by side, plus results |
| `datos/*.py` | Collection, hashing, blind rating, analysis and export scripts |

## Reproduce
```bash
pip install -r requirements.txt
python datos/analisis.py        # recomputes every number and figure from the labels
python datos/exportar_app.py    # rebuilds the demo app data
```
Then open `app/index.html` (or serve the folder with `python -m http.server`).

## Ethics and dual use
All user profiles are fictional and were only sent to the chatbots; nothing false or harmful was published. The risks are well known and documented in public sources; we release the prompts so providers can use them as a regression test. See Appendix A of the paper.

## LLM usage
We used Claude (Anthropic) as an assistant to automate response collection, write the analysis code and help with the literature search and drafting. All classification was done by the team, blind to the app, so Claude (one of the evaluated systems) could not influence the labels. The team designed and supervised the study and verified every result and reference. Details in the paper.

## Team
[Author names and affiliations]. Internal task guide (Spanish): [`TAREAS.md`](TAREAS.md).

All material was created during the sprint (13–15 Nov 2026). Code under the MIT License; data and text under CC BY 4.0 (see `LICENSE`).
