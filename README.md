# CST8912 Group 1: Cloud-Based Job Search and Analytics Platform

CST8912 Cloud Solutions Architecture, Section 011, Professor Ragini Madaan.

**Group CST8912 011 - 1:** David Yin, Hye Ran (Lannie) Yoo, Naol Meherete, Peng (Frank) Wang, Tao Lu.

**Topic (approved by email in September):** Cloud-Based Job Search and Analytics Platform on Microsoft Azure. Our use case is offer2pr, a real job platform run by one of us, moved to Azure.

## Deadlines

| Week | Date | Deliverable | Weight |
|---|---|---|---|
| 7 | Thu 2026-10-22, upload by 12:00 | Group Presentation #1 (in class) | 2.5% |
| 9 | Sunday of Week 9, 23:59 | Group Research Report #1 (first draft) | 5% |
| 10 | Thu 2026-11-12, upload by 12:00 | Group Presentation #2 (in class) | 2.5% |
| 12 | Sunday of Week 12, 23:59 | Group Research Report, second draft | 5% |
| 15 | Week 15 | Final Group Project (proof of concept) | 20% |

Source: CST8912 course schedule and the Brightspace dropboxes.

## What is in this repo

| Folder | What it holds |
|---|---|
| [`requirements/`](requirements/) | The professor's handouts: [Group Presentation](requirements/group_presentation.md) (with rubric), [Group Research Assignment](requirements/group_research_assignment.md), [professor's clarifications](requirements/group_research_clarifications.md), [Group Final Project](requirements/group_final_project.md), plus the original Word files and the report template |
| [`presentation-1/`](presentation-1/) | Presentation 1: [`presentation1.md`](presentation-1/presentation1.md) has every slide's text, figure, speaker notes, the quiz and the bibliography; `fig_*.png` are the figures |
| [`research-report/`](research-report/) | [Report outline](research-report/report_outline.md): sections, page budget and the full challenge register |

## Presentation 1: pick your slides

Ten slides, two per person. Presenters are not chosen yet: pick two slides in the table at the top of [`presentation1.md`](presentation-1/presentation1.md) and tell the group chat. Each slide's speaker notes are already written; change them to your own words.

| # | Slide |
|---|---|
| 1 | Cloud-Based Job Search and Analytics Platform (title) |
| 2 | Research Progress |
| 3 | Today's System |
| 4 | Cloud Architecture and Services |
| 5 | Service Recommendation: Cost and Performance |
| 6 | Components in Every Phase |
| 7 | Key Challenges |
| 8 | Lessons Learned |
| 9 | Quiz (Kahoot) |
| 10 | Bibliography |

## Editing the figures

Figures are drawn in code so they stay consistent. Each `fig_*.drawio` opens in [draw.io](https://www.drawio.com/); the PNGs are exported from them.

To rebuild all figures (needs Python 3 and draw.io desktop):

```bash
cd presentation-1
python build_figures.py
python build_slide_figures.py
```

`build_figures.py` draws the two architecture diagrams (today and on Azure); `build_slide_figures.py` draws the rest. Prices come from the Azure Retail Prices API (Canada Central, USD, Oct 16 2026).

## Credits

Azure icons: Microsoft Azure Architecture Icons. Brand logos in `presentation-1/icons/`: Simple Icons (CC0) and the Healthchecks project. Cat reaction GIFs in `presentation-1/memes/`: Tenor (tenor.com), used for a class presentation.
