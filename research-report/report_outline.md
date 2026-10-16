# Group Research Report: Outline

> **Assignment:** [Group Research Assignment](../requirements/group_research_assignment.md); professor's answers in [group_research_clarifications.md](../requirements/group_research_clarifications.md).
> **Group:** CST8912 011 - 1 (David Yin, Hye Ran (Lannie) Yoo, Naol Meherete, Peng (Frank) Wang, Tao Lu).
> **Due:** first draft Week 9, second draft Week 12. 6 to 10 pages of text, 12 pt, 1.15 spacing, academic tone, APA references.
> **Status (2026-10-16):** outline only. Trend literature and public case studies not started.

## Working title

*AI and the Cloud in Job Search: Trends in Cloud Solutioning, with offer2pr as a Case Study*

## Research structure

| Layer | Question | Place in the report |
|---|---|---|
| Main line: AI in job search | How are AI and cloud services changing the way people search and apply for jobs? | Sections 3, 5, 7 |
| Extension: AI career pathway planning | How can AI plan the path program → school → skills → job → permanent residence, judged by employment outcomes? | Section 8 |
| Analytics: labour market | How do regional jobs, wages and living costs support job decisions? | Sections 3, 8 |

Every extension point is tied back to an employment outcome. Professor ratings are left out (privacy, site terms).

## Sections

| # | Section | Content | Assignment requirement | Pages |
|---|---|---|---|---|
| 1 | Introduction | Topic, why it matters in the cloud services workplace, offer2pr in one paragraph | Importance of the topic | 0.5 |
| 2 | Principles of solution architecture | Azure Well-Architected pillars, each with an offer2pr example | Key principles of solution architecture | 1 |
| 3 | Trends in cloud solutioning for job search | (a) AI search and matching: intent search, semantic and multilingual search, résumé matching; (b) AI job-seeker assistants and agents: résumé analysis and rewriting, cover letters, auto-apply, mock interviews; (c) platform agents for data collection; (d) serverless containers; (e) security, privacy and data residency | Top trends; technology developments | 2.5 |
| 4 | Market and adoption | Cloud and HR-tech market growth; 2 to 3 public cases (vendor case studies, engineering blogs, news) | Market dynamics; adoption patterns; case studies | 1.5 |
| 5 | Case study: offer2pr | Today (Render + on-premises), the Azure design, service choices on cost and performance, Azure AI services per feature | Case study; technology analysis | 2 |
| 6 | From CapEx to OpEx | $6,670 hardware + $255/month vs about $215/month on Azure; sunk cost; move when revenue covers the bill; FinOps | CapEx to OpEx | 1 |
| 7 | Challenges | Site terms and anti-bot limits, data quality (57% incomplete), AI accuracy and bias, privacy (PIPEDA), token cost, skills | Emerging challenges | 1 |
| 8 | Opportunities and outlook | AI career pathway planning; labour market analytics by region (jobs, wages, rent, population, GDP, well-being, environment); what comes next | Emerging opportunities; future outlook | 1 |
| 9 | Conclusion | Main findings | Conclusion required | 0.5 |
| | References | APA, alphabetical | References | |

## Challenge register (for Section 7)

> One list of challenges for Section 7. Presentation 1 (slide 7) shows C1, D1, C2 and S1. Level = impact × likelihood. Numbers come from offer2pr's Job Bank data; Oct 15 and Oct 16 counts use different scopes, so cite the date. ID letters: S security, D data, C collection and sources, M migration to Azure, P price and cost, A AI, L legal and business.

| ID | Challenge | Evidence | Level | How the design handles it |
|---|---|---|---|---|
| S1 | Security and privacy | Every application holds an email and a résumé | High | Front Door WAF; private database; Key Vault with managed identity; personal data masked in the app |
| S2 | Privacy law (PIPEDA, data residency) | Users and their data are in Canada | High | Canada Central only; collect the minimum; set retention periods |
| S3 | No built-in data masking in PostgreSQL | Azure SQL has dynamic data masking; PostgreSQL does not | Medium | Mask personal data in the application |
| D1 | Incomplete data | 34,957 of 61,006 Job Bank postings (57%) miss a key field; apply email 32,721 (Oct 16) | High | Blob keeps every posting; only complete postings go live |
| D2 | Duplicate data | Job Bank does not de-duplicate: 6,667 duplicates removed from 63,840; 30,705 postings copied from other boards (Oct 15) | High | De-duplicate in processing; later AI Search for near-duplicates |
| D3 | Incomplete coverage | Job Bank listed 74,579; we keep 57,173; territories not covered; about 10,700 unexplained (Oct 15) | High | State coverage honestly; add sources one by one |
| D4 | Postings expire fast | 149,320 closed postings, far more than the live ones | Medium | Daily scheduled updates; expired postings removed automatically |
| D5 | Inconsistent formats | Salary hourly, yearly or as a range; locations and job types written many ways | Medium | One common job format; AI-assisted normalisation |
| D6 | Occupation codes (NOC) | Many postings have no NOC or a wrong one | Medium | Automatic classification (Foundry or AI Language) |
| D7 | Two official languages | Most Quebec postings are in French | Medium | Translator; de-duplication across languages |
| D8 | Immigration rules change often | Provincial nominee rules are updated frequently | Medium | Re-collect and check official sources on a schedule |
| C1 | Fragmented sources (root cause) | Job Bank, GC Jobs, Jobillico, Jobboom, CareerBeacon, company careers pages, LinkedIn, Indeed; each with its own format and rules | High | One pipeline per source type into the same Blob layers; common format; cross-source de-duplication; AI agents for new formats |
| C2 | Blocked collection | Cloud IPs blocked more often; some sites need a human check; site terms limit robots | High | Slow, polite crawling; NAT Gateway fixed IP; manual fallback |
| C3 | No company directory | Employers post on their own sites or on Workday, Greenhouse, Lever; no free directory | Medium | Build our own: search APIs and an AI agent find careers pages |
| C4 | Data moats | Large boards built their data early and now restrict automated access | High | Official feeds and partner APIs; discussed as market structure in the report |
| M1 | Cloud IPs blocked more often | Data-centre addresses are easier to block than home networks | High | As C2; keep a small manual or on-premises fallback |
| M2 | Headful browser in the cloud | The crawler needs Chromium with saved sign-ins | Medium | Dedicated image; browser profile on Azure Files |
| M3 | Shared local folder | All tasks share one local data folder | Medium | Move to Blob Storage and Azure Files |
| M4 | Student subscription quotas | No GPU quota; 6 vCPUs per region | Medium | AI on Foundry; Container Apps billed by use |
| M5 | External callback URLs | Google sign-in, Stripe and Resend need new URLs | Low | Update them in the migration checklist |
| P1 | Moving now costs more | Staying costs about $70 a month (hardware paid); Azure about $215 | Medium | Move when paying users or data grow |
| P2 | Costs grow with users | AI token costs rise with every user | High | Budgets and alerts; limit calls per user |
| A1 | Wrong or invented AI answers | Errors about jobs or immigration hurt users | High | Answers cite official sources (RAG); spot checks |
| A2 | Bias in matching | Recommendations and screening can be unfair | High | No sensitive fields; review results regularly |
| A3 | Auto-apply against site terms | Automatic applications may break job-site rules | Medium | Only allowed channels; user confirms each application |
| L1 | Copyright and terms of job text | Republishing other sites' job descriptions | Medium | Show only needed fields and link to the original |
| L2 | Cold start | No data means no users; no users means no revenue | High | Start from public data; focus on newcomers to Canada |
| L3 | Running about 60 tasks | A small team must monitor and fix them | Medium | Azure Monitor alerts; managed services |

Summary: 13 high, 14 medium, 1 low.

## Sources to find (2024 to 2026)

- Cloud market and adoption: Flexera State of the Cloud, Gartner and IDC public summaries.
- AI in recruitment and job search: Microsoft Work Trend Index, LinkedIn reports, engineering blogs of job platforms.
- Public cases: Microsoft, AWS and Google Cloud customer stories for recruitment platforms; news on LinkedIn and Azure.
- Regional data: Statistics Canada, CMHC, Environment and Climate Change Canada, IRCC.
- Azure services: Microsoft Learn (already used in Presentation 1).
