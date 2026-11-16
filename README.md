# Which Door You Walk Through

**An audit of whether consumer chatbots warn about risks users did not ask about.**
Research conducted at the [AI x Epistemics Research Sprint](https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15) (Apart Research, 13–15 Nov 2026).

| | |
|---|---|
| 📄 **Report** | [`paper/Which_Door_You_Walk_Through.pdf`](paper/Which_Door_You_Walk_Through.pdf) |
| 🎬 **Video** | [Watch on Google Drive](https://drive.google.com/file/d/1Pg6qI049v33_d9O3NYGFV2K9Lnt-O5zX/view) · also in [`video/`](video/Which_Door_You_Walk_Through.mp4) |
| 🖥️ **Demo page** | **https://ferchito1974.github.io/which-door-you-walk-through/** (or open [`app/web/which-door.html`](app/web/which-door.html) locally) |
| 📊 **Results** | [`resultados/resumen.md`](resultados/resumen.md) and figures in [`resultados/`](resultados/) |

## The question
People ask chatbots for ordinary tasks (a breakfast plan, a pill organizer, a cleanup script) without asking about the risk hidden inside. Do chatbots warn on their own, like the "guardian angels" proposed by Forethought, or do they just do what they are asked?

## What we did
- **13 Spanish prompts with a hidden risk** (health, engineering, software; simple, medium, complex) + **1 no-risk control**. Original texts and answer key: [`piloto/bateria_prompts.md`](piloto/bateria_prompts.md) (Spanish); **English translations: [`piloto/prompts_en.md`](piloto/prompts_en.md)**.
- **5 runs per prompt, each in a new chat**, on the Gemini app (logged out), ChatGPT (logged out) and Claude (free account, incognito): 210 responses. Exploratory: Google Search AI Mode on 4 prompts (20 responses).
- **Two raters blind to the app** judged: does it warn? is the final plan safe? does it give false reassurance? (89–91% raw agreement, Cohen's κ = 0.42; 38 disagreements adjudicated.)

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

## Language
The study was run in Spanish (Mexico), so prompts and responses are in Spanish. English translations of every prompt are in `piloto/prompts_en.md`, and machine translations of every response are in `datos/respuestas_en/` (offline, Argos Translate). The Spanish originals in `datos/respuestas/` are the evidence; translations are for reading only.

## Repository layout
| Path | Contents |
|---|---|
| `paper/` | Final report (PDF) |
| `video/` | Demo video (MP4) |
| `piloto/` | Prompt battery with answer key, and the 13 Nov pilot |
| `datos/respuestas/` | All 230 responses, verbatim (in Spanish, as answered), with model, date and time |
| `datos/respuestas_en/` | Machine translations (Argos Translate) of every response, for reading only; the Spanish originals are the evidence |
| `datos/capturas/` | Screenshot of each run (from the moment screenshots were enabled) |
| `datos/respuestas.csv` | One row per response (app, model, session, prompt, run, file, notes) |
| `datos/HUELLAS.sha256` | SHA-256 of every response and screenshot |
| `clasificacion/` | Blind texts, both raters' sheets, adjudication (`consenso.csv`), final labels and the code→app key (`CLAVE_NO_ABRIR.csv`) |
| `resultados/` | Tables, `resumen.md`, `resultados.json` and figures |
| `app/web/which-door.html` | Demo page: the same request answered by every app, with verdicts, plus all results (built by `datos/construir_web.py`) |
| `app/index.html` | Earlier internal viewer (Spanish) |
| `docs/internal/` | Video script and original project proposal (Spanish) |
| `datos/*.py` | Collection, hashing, blind rating, analysis and export scripts |

## Reproduce
```bash
pip install -r requirements.txt
python datos/analisis.py        # recomputes every number and figure from the labels
python datos/exportar_app.py    # rebuilds the internal viewer data
python datos/construir_web.py   # rebuilds the demo page app/web/which-door.html
```
Then open `app/web/which-door.html` in a browser.

## Ethics and dual use
All user profiles are fictional and were only sent to the chatbots; nothing false or harmful was published. The risks are well known and documented in public sources; we release the prompts so providers can use them as a regression test. See Appendix A of the paper.

## LLM usage
We used Claude (Anthropic) as an assistant to automate response collection, write the analysis code, run an initial literature search and produce a first draft. All classification was done by the team, blind to the app, so Claude (one of the evaluated systems) could not influence the labels. The team designed and supervised the study, carried out the literature review, verified every result and reference, and rewrote the final report. Details in the paper.

## Team
Universidad Politécnica de Yucatán, Mexico, with Apart Research:
- Ianina Priscila Moo Sosa
- Fernando Patricio Euan Maas
- Karol Guadalupe Coral Tolosa
- Zalleth del Pilar Peraza Alpuche
- Jorge Alexis Aké Medina

The video script and the original project proposal (Spanish) are in `docs/internal/`.

All material was created during the sprint (13–15 Nov 2026). Code under the MIT License; data and text under CC BY 4.0 (see `LICENSE`).
