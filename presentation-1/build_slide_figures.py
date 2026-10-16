"""Build the other Presentation 1 figures: progress (2), services (5), challenges (7), phases (8), lessons (9).

Run:  python build_slide_figures.py   (needs draw.io desktop for the PNG export)
"""
import base64
import os

from drawio_lib import FONT, HERE, add, box, card, edge, icon, save, text

GREEN, AMBER, GREY, RED, BLUE = "#107C10", "#C19C00", "#8A8886", "#C00000", "#0078D4"
FILL = {GREEN: "#DFF6DD", AMBER: "#FFF4CE", GREY: "#F3F2F1", RED: "#FDE7E9", BLUE: "#EAF3FC"}


def panel(title, x, y, w, h, color=BLUE):
    """Dashed region box with a coloured title."""
    style = (f"rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#999999;strokeWidth=1.5;"
             f"dashed=1;dashPattern=6 4;verticalAlign=top;align=center;spacingTop=10;fontStyle=1;"
             f"fontSize=20;fontFamily={FONT};fontColor={color};")
    return add(title, style, x, y, w, h)


def chevron(label, x, y, w, h, color, first=False):
    shape = "mxgraph.arrows2.arrow;dy=0;dx=30;notch=0" if first else "step;perimeter=stepPerimeter;fixedSize=1;size=30"
    style = (f"shape={shape};whiteSpace=wrap;html=1;fillColor={FILL[color]};strokeColor={color};strokeWidth=2;"
             f"fontSize=17;fontFamily={FONT};fontColor=#222222;fontStyle=1;")
    return add(label, style, x, y, w, h)


def pill(label, x, y, w, color, h=32):
    style = (f"rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor={FILL[color]};strokeColor={color};strokeWidth=2;"
             f"fontSize=15;fontFamily={FONT};fontColor={color};fontStyle=1;")
    return add(label, style, x, y, w, h)


def bar(x, y, w, h, color, label=""):
    style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={color};strokeColor=none;"
             f"fontSize=18;fontFamily={FONT};fontColor=#FFFFFF;fontStyle=1;")
    return add(label, style, x, y, w, h)


def point(x, y):
    """Invisible anchor for a free-standing arrow."""
    return add("", "text;html=1;", x, y, 1, 1)


# ============ Slide 2: research progress as a timeline: what we researched (W2 to W7) and will research (W9 to W14),
# spread evenly by week in the order we do them ============
def wx(w):
    return 60 + (w - 1) * 1160 / 14


AXIS, BW, BH = 150, 162, 100
add("", "rounded=0;fillColor=#D2D0CE;strokeColor=none;", wx(1), AXIS - 4, wx(15) - wx(1), 8)
add("", f"rounded=0;fillColor={GREEN};strokeColor=none;", wx(1), AXIS - 4, wx(7) - wx(1), 8)
add("Break", f"rounded=0;fillColor=#FFFFFF;strokeColor=#D2D0CE;dashed=1;fontSize=12;fontFamily={FONT};fontColor=#8A8886;",
    wx(7.6), AXIS - 12, wx(8.4) - wx(7.6), 24)
for w in range(1, 16):
    text(f"W{w}", wx(w) - 20, AXIS + 12, 40, 20, size=13, color="#8A8886")
for n, (w, title, detail, color) in enumerate([
        (2, "Topic approved", "Job search and analytics on Azure", GREEN),
        (3, "Old system mapped", "Render website; ~60 tasks and an AI server on premises", GREEN),
        (4, "Job platforms surveyed", "Job Bank, GC Jobs, Jobillico, Jobboom, CareerBeacon", GREEN),
        (5, "Job Bank data quality", "57% of 61,006 postings miss a key field", GREEN),
        (6, "Azure components", "Use and monthly cost of 40 options", GREEN),
        (7, "Challenges found", "Scattered sources, blocked crawling, duplicates, privacy", AMBER),
        (9, "AI job search", "Semantic, multilingual, one-sentence search", GREY),
        (10, "Résumé matching", "Match résumés to jobs with embeddings", GREY),
        (11, "AI career agents", "Résumé rewriting, cover letters, mock interviews", GREY),
        (12, "Public case studies", "2 to 3 job platforms on the cloud", GREY),
        (13, "AI cost at scale", "Token cost per user; CapEx to OpEx", GREY),
        (14, "Proof of concept", "Website + one AI feature on Azure", GREY)]):
    x, up = wx(w), n % 2 == 0
    lx = min(max(x - BW / 2, 6), 1274 - BW)
    if up:
        ly = 10
        add("", f"rounded=0;fillColor={color};strokeColor=none;", x - 1, ly + BH, 2, AXIS - 13 - ly - BH)
    else:
        ly = AXIS + 50
        add("", f"rounded=0;fillColor={color};strokeColor=none;", x - 1, AXIS + 34, 2, ly - AXIS - 34)
    add("", f"ellipse;fillColor={FILL[color]};strokeColor={color};strokeWidth=3;", x - 12, AXIS - 12, 24, 24)
    add(f"<b>{title}</b><br><span style=\"font-size:13px;color:#444444\">{detail}</span>",
        f"rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor={FILL[color]};strokeColor={color};strokeWidth=2;"
        f"fontSize=15;fontFamily={FONT};fontColor=#222222;spacing=4;", lx, ly, BW, BH)
text("<b>Today</b>", wx(7) - 30, AXIS - 40, 60, 22, size=14, color=AMBER)
save("fig_progress", height=AXIS + 50 + BH + 12)

# Slide 2 (research progress) table stays in presentation1.md as the full record.

# ============ Slides 5 and 6: service comparisons ============
# Prices: Azure Retail Prices API, Canada Central, USD, Oct 16 2026, 730 h/month (Linux). Items the API does not
# return (App Gateway WAF v2, NAT Gateway, Functions Flex on-demand, GPT-4o mini) use Azure's published pricing pages.
# Specs: Microsoft Learn pages listed in presentation1.md (bibliography).
GREY_TXT = "#666666"


def logo(path, x, y, size=40):
    if path.startswith("brand:"):
        _, slug, fill = path.split(":")
        with open(os.path.join(HERE, "icons", slug + ".svg"), encoding="utf-8") as f:
            svg = base64.b64encode(f.read().replace("<svg ", f'<svg fill="{fill}" ', 1).encode()).decode()
        add("", f"image;aspect=fixed;html=1;image=data:image/svg+xml,{svg};", x, y, size, size)
    else:
        icon(path, "", x, y, size=size, lw=1, lh=1)


def comparison(name, rows):
    h, gap = 112, 14
    for r, (need, opts, why) in enumerate(rows):
        y = 16 + r * (h + gap)
        text(f"<b>{need}</b>", 16, y, 185, h, size=19, align="left")
        for n, (path, title, price, spec, chosen) in enumerate(opts):
            x = 205 + n * 262
            color = GREEN if chosen else GREY
            add("", f"rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor={'#FFFFFF' if chosen else '#F3F2F1'};"
                    f"strokeColor={color};strokeWidth={3 if chosen else 1};", x, y, 248, h)
            logo(path, x + 10, y + 10, 34)
            text(f"<b>{title}</b>", x + 50, y + 6, 192, 42, size=15, align="left")
            text(f"<b>{price}</b><span style=\"font-size:13px;font-weight:normal\">/month</span>", x + 10, y + 46, 150, 30,
                 size=21, align="left", color=GREEN if chosen else "#222222")
            if chosen:
                pill("Our choice", x + 150, y + 48, 88, GREEN, h=24)
            text(spec, x + 10, y + 76, 232, 32, size=13, align="left", color=GREY_TXT)
    save(name, width=1000, height=16 + len(rows) * (h + gap) + 4)


comparison("fig_recommendation", [
    ("Run the website",
     [("app_services/App_Services", "App Service B1", "$13", "1 core, 1.75 GB; manual scale", 0),
      ("other/Worker_Container_App", "Container Apps", "$25", "0.5 vCPU, 1 GiB; autoscale 0 to 30", 1),
      ("compute/Kubernetes_Services", "AKS, 2 nodes", "$156", "2 × 2 vCPU, 8 GiB; we run Kubernetes", 0)],
     "Same environment as the data jobs"),
    ("Store the data",
     [("databases/Azure_Database_PostgreSQL_Server", "PostgreSQL B1ms", "$18", "1 vCore, 2 GiB, burstable", 0),
      ("databases/Azure_Database_PostgreSQL_Server", "PostgreSQL B2s", "$58", "2 vCores, 4 GiB, burstable", 1),
      ("databases/SQL_Database", "Azure SQL, 2 vCores", "$267", "2 vCores, about 10 GB; app rewrite", 0)],
     "Same engine, no rewrite"),
    ("Run AI models",
     [("compute/Virtual_Machine", "GPU VM NC4as T4", "$426", "4 vCPU, 28 GiB, 1 T4; billed when idle", 0),
      ("ai_machine_learning/Cognitive_Services", "Foundry, GPT-4o mini", "~$10", "pay per token; no GPU quota", 1)],
     "About 40× cheaper at our volume"),
    ("Protect the edge",
     [("other/Worker_Container_App", "Container Apps ingress", "$0", "HTTPS only; no WAF, no CDN", 0),
      ("networking/Front_Doors", "Front Door Standard", "$42", "WAF + CDN at the global edge", 1),
      ("networking/Application_Gateways", "App Gateway WAF v2", "~$330", "regional WAF, no CDN", 0)],
     "WAF and CDN for an eighth of the price"),
])

comparison("fig_services", [
    ("Run the website",
     [("app_services/App_Services", "App Service B1", "$13", "1 core, 1.75 GB; manual scale", 0),
      ("other/Worker_Container_App", "Container Apps", "$25", "0.5 vCPU, 1 GiB; autoscale 0 to 30", 1),
      ("compute/Kubernetes_Services", "AKS, 2 nodes", "$156", "2 × 2 vCPU, 8 GiB; we run Kubernetes", 0)],
     "Same environment as the data jobs"),
    ("Run scheduled jobs",
     [("other/Worker_Container_App", "Container Apps Jobs", "$13", "cron; any container, even headful Chromium", 1),
      ("compute/Function_Apps", "Functions, Flex", "~$20", "no custom container, so no browser", 0),
      ("compute/Virtual_Machine", "VM B2s + cron", "$34", "2 vCPU, 4 GiB; always on; we patch it", 0)],
     "Pay only while a job runs"),
    ("Store the data",
     [("databases/Azure_Database_PostgreSQL_Server", "PostgreSQL B1ms", "$18", "1 vCore, 2 GiB, burstable", 0),
      ("databases/Azure_Database_PostgreSQL_Server", "PostgreSQL B2s", "$58", "2 vCores, 4 GiB, burstable", 1),
      ("databases/SQL_Database", "Azure SQL, 2 vCores", "$267", "2 vCores, about 10 GB; app rewrite", 0)],
     "Same engine, no rewrite; B1ms as fallback"),
    ("Keep data files",
     [("storage/Storage_Accounts", "Blob, Hot only", "$6", "130 GB, all on the hot tier", 0),
      ("storage/Storage_Accounts", "Blob, Hot + Cool", "$5", "lifecycle moves old raw files to Cool", 1),
      ("storage/Storage_Accounts", "Azure Files", "$7", "SMB share; 1.5× the Blob hot price", 0)],
     "Cheapest; Files only for the browser profile"),
    ("Run AI models",
     [("compute/Virtual_Machine", "GPU VM NC4as T4", "$426", "4 vCPU, 28 GiB, 1 T4; billed when idle", 0),
      ("ai_machine_learning/Cognitive_Services", "Foundry, GPT-4o mini", "~$10", "pay per token; no GPU quota", 1)],
     "About 40× cheaper at our volume"),
])

comparison("fig_services_ops", [
    ("Host the domain",
     [("brand:cloudflare:#F38020", "Cloudflare DNS", "$0", "fast, but outside Azure", 0),
      ("networking/DNS_Zones", "Azure DNS", "$1", "same RBAC; validates the Front Door domain", 1)],
     "Everything in one cloud"),
    ("Protect the edge",
     [("other/Worker_Container_App", "Container Apps ingress", "$0", "HTTPS only; no WAF, no CDN", 0),
      ("networking/Front_Doors", "Front Door Standard", "$42", "WAF + CDN at the global edge", 1),
      ("networking/Application_Gateways", "App Gateway WAF v2", "~$330", "regional WAF, no CDN", 0)],
     "WAF and CDN for an eighth of the price"),
    ("Fixed outbound IP",
     [("networking/Virtual_Networks", "Default outbound", "$0", "IP can change at any time", 0),
      ("networking/NAT", "NAT Gateway", "$34", "one static IP, outbound only", 1),
      ("networking/Firewalls", "Azure Firewall Basic", "$288", "static IP plus traffic filtering", 0)],
     "Static IP without paying for a firewall"),
    ("Keep secrets",
     [("other/Worker_Container_App", "Container Apps secrets", "$0", "per app; no audit log, no rotation", 0),
      ("security/Key_Vaults", "Key Vault", "<$1", "one place; audit log; rotation", 1)],
     "Audited and shared by every service"),
    ("Watch and alert",
     [("brand:healthchecks:#33333f", "Self-hosted Healthchecks", "~$8", "job pings only; we run it", 0),
      ("management_governance/Monitor", "Azure Monitor + App Insights", "$14", "logs, metrics, traces, alerts", 1)],
     "Logs and alerts with nothing to run"),
    ("Store images",
     [("brand:docker:#2496ED", "Docker Hub, free", "$0", "public; pull rate limits", 0),
      ("containers/Container_Registries", "Container Registry Basic", "$5", "private; same region; managed identity", 1)],
     "Private images close to the apps"),
])

# Slide 6 (monthly cost) is an ECharts chart: charts/build_charts.ts writes fig_costs.png

# ============ Slide 8: AI across job search (trend) ============
def lane(title, color, y, steps, dashed=False):
    style = (f"rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=none;strokeColor={color};strokeWidth=2;"
             f"{'dashed=1;dashPattern=6 4;' if dashed else ''}verticalAlign=top;align=left;spacingLeft=14;spacingTop=6;"
             f"fontStyle=1;fontSize=18;fontFamily={FONT};fontColor={color};")
    add(title, style, 20, y, 1240, 200 if steps[0][1] else 120)
    w = 1200 / len(steps)
    for n, (label, svc) in enumerate(steps):
        x = 40 + n * w
        chevron(f"<b><span style=\"font-size:15px\">{label}</span></b>", x, y + 40, w + 8, 60, color, first=n == 0)
        if svc:
            path, name = svc
            if path.startswith("brand:"):
                pass
            icon(path, "", x + w / 2 - 20, y + 110, size=40, lw=1, lh=1)
            text(name, x + 4, y + 152, w - 8, 40, size=14, color="#444444")


lane("For job seekers", BLUE, 20, [
    ("Search in<br>one sentence", ("app_services/Search_Services", "Foundry + AI Search")),
    ("Match<br>my résumé", ("ai_machine_learning/Form_Recognizers", "Document Intelligence + AI Search")),
    ("Improve<br>my résumé", ("ai_machine_learning/Cognitive_Services", "Foundry")),
    ("Write a<br>cover letter", ("ai_machine_learning/Cognitive_Services", "Foundry")),
    ("Apply for me", ("ai_machine_learning/Cognitive_Services", "Foundry Agent Service")),
    ("Practise the<br>interview", ("ai_machine_learning/Speech_Services", "Speech + Foundry")),
])
lane("For the platform", AMBER, 240, [
    ("Find new sources", ("ai_machine_learning/Cognitive_Services", "Foundry Agent Service")),
    ("Read pages and PDFs", ("ai_machine_learning/Form_Recognizers", "Document Intelligence")),
    ("Check quality", ("other/Worker_Container_App", "Container Apps Jobs")),
    ("Index for search", ("app_services/Search_Services", "AI Search")),
])
lane("Next: career pathway, judged by job outcomes", GREY, 460, [
    ("Program", None), ("School", None), ("Skills", None), ("Job", None), ("Permanent residence", None),
], dashed=True)
save("fig_ai_trends", height=600)

# ============ Slide 5: components in every phase ============
phases = [("Collect", [("other/Worker_Container_App", "Container Apps Jobs"), ("networking/NAT", "NAT Gateway")]),
          ("Store", [("storage/Storage_Accounts", "Blob Storage"),
                     ("databases/Azure_Database_PostgreSQL_Server", "PostgreSQL")]),
          ("Process", [("other/Worker_Container_App", "Jobs + quality check"),
                       ("ai_machine_learning/Cognitive_Services", "Azure AI services")]),
          ("Serve", [("networking/Front_Doors", "Front Door + WAF"), ("other/Worker_Container_App", "Container Apps")]),
          ("Monitor", [("management_governance/Monitor", "Azure Monitor"), ("devops/Application_Insights", "App Insights")])]
for n, (name, items) in enumerate(phases):
    x = 30 + n * 245
    chevron(f"<b>{name}</b>", x, 30, 255, 70, BLUE, first=n == 0)
    for k, (path, label) in enumerate(items):
        icon(path, f"<b>{label}</b>", x + 95, 140 + k * 160, lw=220)
box("All phases", 30, 480, 1220, 100, fill="#F5F9FF", size=16, dashed=True)
icon("networking/DNS_Zones", "<b>Azure DNS</b>", 70, 512, size=44, lw=130, pos="right")
icon("security/Key_Vaults", "<b>Key Vault</b>", 300, 512, size=44, lw=130, pos="right")
icon("identity/Managed_Identities", "<b>Managed identity</b>", 530, 512, size=44, lw=160, pos="right")
icon("containers/Container_Registries", "<b>Container Registry</b>", 790, 512, size=44, lw=170, pos="right")
brand_path = os.path.join(HERE, "icons", "githubactions.svg")
with open(brand_path, encoding="utf-8") as f:
    gh = base64.b64encode(f.read().replace("<svg ", '<svg fill="#2088FF" ', 1).encode()).decode()
add("", f"image;aspect=fixed;html=1;image=data:image/svg+xml,{gh};", 1050, 514, 40, 40)
text("<b>GitHub Actions</b>", 1098, 514, 140, 40, size=14, align="left")
save("fig_phases", height=600)

# Slide 6 (key challenges) is a Markdown table in presentation1.md for now.

# Slide 7 (lessons learned) is a Markdown table in presentation1.md for now.

# ============ cat reaction GIFs (memes/, from Tenor); draw.io exports the first frame ============
def cat(name, x, y, w, h):
    with open(os.path.join(HERE, "memes", name + ".gif"), "rb") as f:
        gif = base64.b64encode(f.read()).decode()
    add("", f"image;html=1;imageAspect=1;aspect=fixed;image=data:image/gif,{gif};", x, y, w, h)


def bubble(textv, x, y, w, h, color):
    add(textv, f"shape=callout;whiteSpace=wrap;html=1;perimeter=calloutPerimeter;position2=0.15;base=16;size=14;"
               f"rounded=1;fillColor=#FFFFFF;strokeColor={color};strokeWidth=2;fontSize=15;fontStyle=2;"
               f"fontFamily={FONT};fontColor=#222222;", x, y, w, h)


# ============ Slide 6: key challenges (picked: C1, D1, C2, S1): title, cat + quote, key fact, details, response ============
W4, GAP = 300, 13
picks = [("Fragmented sources", BLUE, "c1_huh", "Where are the jobs?", "8+ job sites", "One pipeline per source type"),
         ("Incomplete data", AMBER, "d1_shocked", "Only 26,049 complete?!", "57% incomplete", "Only complete postings go live"),
         ("Blocked collection", RED, "c2_crying", "Access denied. Again.", "Blocked", "Slow, polite crawling"),
         ("Security and privacy", GREEN, "s1_polite", "Lock them up.", "Personal data", "Mask personal data in the app")]
X = [20 + n * (W4 + GAP) for n in range(4)]
for x, (title, color, gif, quote, fact, response) in zip(X, picks):
    panel(title, x, 20, W4, 620, color)
    bubble(f'"{quote}"', x + 25, 70, 250, 50, color)
    cat(gif, x + 80, 138, 140, 140)
    text(f"<b>{fact}</b>", x + 10, 290, 280, 48, size=28, color=color)
    pill(response, x + 15, 580, 270, color)
DET = 350  # details start here
# C1: the sites
for k, name in enumerate(["Job Bank", "GC Jobs", "Jobillico", "Jobboom", "CareerBeacon", "Company sites"]):
    card(f"<b>{name}</b>", X[0] + 20 + (k % 2) * 135, DET + (k // 2) * 50, 125, 40)
text("own format each, English or French", X[0] + 10, DET + 150, 280, 40, size=15, color="#444444")
# D1: missing fields as mini bars (61,006 postings, Oct 16)
for k, (label, v) in enumerate([("Apply email", 32721), ("Description", 11742), ("Employment term", 6495), ("Hours", 1036)]):
    y = DET + k * 40
    text(label, X[1] + 10, y, 120, 30, size=14, align="right", color="#444444")
    add("", f"rounded=1;arcSize=20;fillColor={AMBER};strokeColor=none;", X[1] + 138, y + 8, max(4, v / 32721 * 90), 16)
    text(f"{v:,}", X[1] + 138 + max(4, v / 32721 * 90) + 6, y, 70, 30, size=14, align="left")
text("missing, of 61,006 postings", X[1] + 10, DET + 165, 280, 30, size=15, color="#444444")
# C2: three reasons
for k, line in enumerate(["Cloud IPs blocked more often", "Some sites need a human check", "Site terms limit robots"]):
    y = DET + k * 55
    text("✕", X[2] + 15, y, 30, 40, size=22, bold=True, color=RED)
    text(line, X[2] + 50, y, 240, 40, size=16, align="left")
# S1: three protections
for k, (path, label) in enumerate([("networking/Front_Doors", "WAF at the edge"),
                                    ("databases/Azure_Database_PostgreSQL_Server", "Private database"),
                                    ("security/Key_Vaults", "Secrets in Key Vault")]):
    icon(path, f"<b>{label}</b>", X[3] + 40, DET + k * 62, size=42, lw=190, pos="right")
save("fig_challenges", height=660)

# ============ Slide 7: lessons learned (picked: E6, E10, E7): three rows with a cat each ============
text("<b>What we learned</b>", 24, 24, 400, 56, size=28, align="left")


def mini_bar(x, y, w, color, label):
    add("", f"rounded=1;arcSize=20;fillColor={color};strokeColor=none;", x, y, max(w, 6), 26)
    text(label, x + max(w, 6) + 10, y - 4, 260, 34, size=18, align="left")


rows = [("e6_laughing", "Real prices change decisions", "GPU server $426? Foundry $10!", GREEN),
        ("e10_smiling", "Data quality shapes the design", "Keep it all in Blob, show only the complete ones.", AMBER),
        ("e7_dancing", "Move when the business needs it", "Stay at $70 until the money comes in.", BLUE)]
ROWH = 170
for n, (gif, title, caption, color) in enumerate(rows):
    y = 100 + n * (ROWH + 18)
    add("", f"rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={color};strokeWidth=2;",
        20, y, 1240, ROWH)
    add(str(n + 1), f"ellipse;whiteSpace=wrap;html=1;fillColor={color};strokeColor=none;fontSize=26;fontStyle=1;"
                    f"fontFamily={FONT};fontColor=#FFFFFF;", 40, y + ROWH / 2 - 24, 48, 48)
    cat(gif, 105, y + 15, 140, 140)
    text(f"<b>{title}</b>", 260, y + 20, 380, 70, size=23, align="left")
    text(f'<i>"{caption}"</i>', 260, y + 90, 360, 60, size=16, align="left", color="#555555")
    x0, yy = 640, y + 25
    if n == 0:
        text("GPU VM", x0, yy + 18, 100, 34, size=17, align="left", color="#444444")
        mini_bar(x0 + 100, yy + 22, 320, RED, "<b>$426</b>/month")
        text("Foundry", x0, yy + 70, 100, 34, size=17, align="left", color="#444444")
        mini_bar(x0 + 100, yy + 74, 8, GREEN, "<b>~$10</b>/month")
    elif n == 1:
        text("All postings", x0, yy + 18, 130, 34, size=17, align="left", color="#444444")
        mini_bar(x0 + 130, yy + 22, 300, "#2a78d6", "<b>61,006</b>")
        text("Complete", x0, yy + 70, 130, 34, size=17, align="left", color="#444444")
        mini_bar(x0 + 130, yy + 74, 128, GREEN, "<b>26,049</b> go live")
    else:
        text("Stay today", x0, yy + 18, 130, 34, size=17, align="left", color="#444444")
        mini_bar(x0 + 130, yy + 22, 100, GREEN, "<b>~$70</b>/month")
        text("Azure", x0, yy + 70, 130, 34, size=17, align="left", color="#444444")
        mini_bar(x0 + 130, yy + 74, 300, BLUE, "<b>~$215</b>/month")
save("fig_lessons", height=100 + 3 * (ROWH + 18) + 10)

# ============ Slide 7 extra: emoji-style "Expectation vs Reality" meme with cat emoji (our own drawing) ============
MEME = ("text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;fontFamily=Impact;fontSize={s};"
        "fontColor=#FFFFFF;textShadow=1;")
for n, (head, face, line1, price, color) in enumerate([
        ("EXPECTATION", "😼", "\"Let's buy our own GPU server for AI\"", "Cheap, right?", GREY),
        ("REALITY", "🙀", "\"It bills even when nobody uses it\"", "$426 / month", RED),
        ("LESSON", "😸", "\"Just pay per token on Foundry\"", "~$10 / month", GREEN)]):
    x = 20 + n * 420
    add("", "rounded=1;arcSize=4;fillColor=#3B3A39;strokeColor=none;", x, 20, 405, 520)
    add(head, MEME.format(s=40), x, 30, 405, 64)
    add(face, "text;html=1;align=center;verticalAlign=middle;fontSize=130;fontFamily=Segoe UI Emoji;", x, 100, 405, 200)
    add(line1, MEME.format(s=26), x + 15, 310, 375, 110)
    add(price, f"rounded=1;arcSize=30;whiteSpace=wrap;html=1;fillColor={color};strokeColor=none;fontSize=26;"
               f"fontStyle=1;fontFamily={FONT};fontColor=#FFFFFF;", x + 62, 445, 280, 60)
save("fig_meme", height=560)
