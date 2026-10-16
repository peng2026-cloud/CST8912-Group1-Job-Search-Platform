"""Build the Presentation 1 diagrams: fig_current (slide 3) and fig_architecture (slide 4).

Run:  python build_figures.py   (needs draw.io desktop for the PNG export)
"""
import base64
import os

from drawio_lib import FONT, HERE, LABEL, add, box, card, edge, icon, save, text

GROUP = ("rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#999999;dashed=1;"
         "dashPattern=6 4;strokeWidth=1.5;verticalAlign=top;align=center;spacingTop=6;fontStyle=1;"
         f"fontSize=16;fontFamily={FONT};fontColor=#0078D4;")
PROBLEM = ("rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=#FDE7E9;strokeColor=#C00000;strokeWidth=2;"
           f"fontSize=14;fontFamily={FONT};fontColor=#C00000;fontStyle=1;")
DB = ("shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;size=12;fillColor=#FFFFFF;strokeColor=#666666;"
      f"fontSize=14;fontFamily={FONT};fontColor=#222222;")


def sources(x, y):
    box("Data sources", x, 60, 150, 640, dashed=True)
    return card("<b>Job Bank</b><br><font color='#777777'>job boards<br>government data</font>", x + 10, y, 130, 72)


def stencil(shape, label, x, y, w=60, h=70, lw=200, fill="#2875E2", right=False):
    """Non-Azure icon from draw.io's built-in Networks library, label below."""
    i = add("", f"shape=mxgraph.networks.{shape};html=1;fillColor={fill};strokeColor=#ffffff;gradientColor=none;"
                "sketch=0;outlineConnect=0;", x, y, w, h)
    LABEL_X[i] = x + w / 2
    if right:
        LABEL[i] = text(label, x + w + 8, y, lw, h, align="left")
    else:
        LABEL[i] = text(label, x + w / 2 - lw / 2, y + h + 4, lw, 50)
    return i


LABEL_X = {}


def brand(slug, color, label, x, y, size=56, lw=160, right=False):
    """Product logo from icons/<slug>.svg (simple-icons), filled with its brand colour, label below."""
    with open(os.path.join(HERE, "icons", slug + ".svg"), encoding="utf-8") as f:
        svg = f.read().replace("<svg ", f'<svg fill="{color}" ', 1)
    data = base64.b64encode(svg.encode()).decode()
    i = add("", f"image;aspect=fixed;html=1;points=[];image=data:image/svg+xml,{data};", x, y, size, size)
    LABEL_X[i] = x + size / 2
    if right:
        LABEL[i] = text(label, x + size + 8, y, lw, size, align="left")
    else:
        LABEL[i] = text(label, x + size / 2 - lw / 2, y + size + 4, lw, 50)
    return i


def step(n, x, y, side=0):
    """Green numbered circle beside a flow line: 0 above, 1 right of a vertical line, 2 below, 3 left."""
    x, y = {0: (x, y - 22), 1: (x + 22, y), 2: (x, y + 22), 3: (x - 22, y)}[side]
    add(str(n), f"ellipse;whiteSpace=wrap;html=1;fillColor=#107C10;strokeColor=#FFFFFF;strokeWidth=2;"
                f"fontSize=15;fontStyle=1;fontFamily={FONT};fontColor=#FFFFFF;", x - 14, y - 14, 28, 28)


def legend(x=1118, y=560):
    """Key for line styles and step numbers, bottom of the Data sources column."""
    def pt(px, py):
        return add("", "text;html=1;", px, py, 1, 1)
    edge(pt(x, y), pt(x + 40, y))
    text("main flow", x + 46, y - 12, 90, 24, size=13, align="left")
    edge(pt(x, y + 32), pt(x + 40, y + 32), dashed=True)
    text("support", x + 46, y + 20, 90, 24, size=13, align="left")
    step("1", x + 20, y + 86)
    text("step order", x + 46, y + 52, 90, 24, size=13, align="left")


# ============ Slide 3: current state (hybrid PaaS + on-premises) ============
box("Job seekers", 20, 60, 135, 640, dashed=True)
users = icon("identity/Users", "", 55, 400, lw=125, lh=30)

box("Domain", 165, 215, 125, 485, dashed=True)
cf = brand("cloudflare", "#F38020", "<b>Cloudflare DNS</b><br><font color='#777777'>custom domain</font>", 199, 404, lw=120)

box("SaaS", 165, 60, 930, 140, dashed=True)
google = brand("google", "#4285F4", "<b>Google</b><br><font color='#777777'>SEO, sign-in</font>", 282, 82, size=36, lw=84)
umami = brand("umami", "#000000", "<b>Umami</b><br><font color='#777777'>analytics</font>", 348, 82, size=36, lw=64)
stripe = brand("stripe", "#635BFF", "<b>Stripe</b><br><font color='#777777'>payments</font>", 414, 82, size=36, lw=64)
resend = brand("resend", "#000000", "<b>Resend</b><br><font color='#777777'>email</font>", 480, 82, size=36, lw=64)
llm = brand("anthropic", "#191919", "<b>LLM API</b><br><font color='#777777'>chat, letters</font>", 546, 82, size=36, lw=92)
mail = brand("gmail", "#EA4335", "<b>Gmail</b><br><font color='#777777'>alert email</font>", 822, 82, size=36, lw=84)
hc = brand("healthchecks", "#33333f", "<b>Healthchecks</b><br><font color='#777777'>job monitoring</font>", 917, 82, size=36, lw=110)

box("Render (PaaS): public IP, auto-deploy", 300, 215, 265, 485, dashed=True, where="bottom", size=13)
web = brand("nextdotjs", "#000000", "<b>Website</b><br><font color='#777777'>Next.js + Payload</font>", 404, 404, lw=180)
pg = brand("postgresql", "#4169E1", "<b>PostgreSQL</b>", 404, 595, lw=88, right=True)

box("On-premises servers: no inbound public IP", 580, 215, 515, 485, dashed=True, size=13)
gpu = brand("ollama", "#000000", "<b>GPU server</b><br><font color='#777777'>Ollama AI models</font>", 700, 404, lw=160)
etl = brand("docker", "#2496ED", "<b>~60 Docker jobs</b><br><font color='#777777'>ETL + browser crawler</font>", 907, 404, lw=200)
data = stencil("storage", "<b>Local data files</b><br><font color='#777777'>only mart is synced</font>", 913, 598, w=44, h=50, lw=150)

src = sources(1110, 396)

edge(users, cf, exit=(1, 0.5), entry=(0, 0.5))
edge(cf, web, exit=(1, 0.5), entry=(0, 0.5))
for target, ex, turn in [(google, 0.1, 190), (umami, 0.3, 178), (stripe, 0.5, 0), (resend, 0.7, 178), (llm, 0.9, 190)]:
    x0, x1 = 404 + 56 * ex, LABEL_X[target]
    pts = [(x0, turn), (x1, turn)] if turn else None
    edge(web, LABEL[target], exit=(ex, 0), entry=(0.5, 1), dashed=True, points=pts)
edge(etl, LABEL[hc], exit=(0.5, 0), entry=(0.5, 1), dashed=True)
edge(hc, mail, exit=(0, 0.5), entry=(1, 0.5), dashed=True)
edge(LABEL[web], pg, exit=(0.5, 1), entry=(0.5, 0))
edge(src, etl, exit=(0, 0.5), entry=(1, 0.5))
edge(etl, gpu, exit=(0, 0.5), entry=(1, 0.5))
edge(LABEL[etl], data, exit=(0.5, 1), entry=(0.5, 0))
edge(data, LABEL[pg], exit=(0, 0.5), entry=(1, 0.5))

for n, (x, y, v) in enumerate([(140, 432, 0), (432, 557, 1), (1040, 432, 0), (935, 545, 1), (830, 432, 0),
                                (640, 623, 0)], 1):
    step(n, x, y, v)

legend()
save("fig_current")

# ============ Slide 4: proposed Azure architecture ============
box("People", 20, 60, 110, 470, dashed=True)
dev = brand("githubactions", "#2088FF", "<b>GitHub Actions</b>", 47, 130, lw=110)
users = icon("identity/Users", "<b>Job seekers</b>", 43, 400, lw=110, lh=30)

box("Domain", 140, 60, 90, 470, dashed=True, size=13)
cf = icon("networking/DNS_Zones", "<b>Azure DNS</b><br><font color='#777777'>domain</font>", 153, 400, lw=100, lh=54)

box("SaaS", 20, 545, 210, 155, dashed=True, size=13)
brand("google", "#4285F4", "<b>Google</b> <font color='#777777'>SEO, sign-in</font>", 32, 574, size=26, lw=160, right=True)
brand("umami", "#000000", "<b>Umami</b> <font color='#777777'>analytics</font>", 32, 604, size=26, lw=160, right=True)
brand("stripe", "#635BFF", "<b>Stripe</b> <font color='#777777'>payments</font>", 32, 634, size=26, lw=160, right=True)
brand("resend", "#000000", "<b>Resend</b> <font color='#777777'>email</font>", 32, 664, size=26, lw=160, right=True)
saas = add("", "text;html=1;", 230, 600, 1, 1)

box("Azure global edge", 240, 60, 100, 640, size=13, dashed=True)
fd = icon("networking/Front_Doors", "<b>Front Door</b><br><font color='#777777'>WAF + CDN</font>", 258, 400, lw=100, lh=54)

box("Microsoft Azure (Canada Central)", 350, 60, 750, 640, where="bottom", dashed=True)
for label, x, w in [("Serve", 355, 170), ("Store", 535, 270), ("Collect & process", 815, 280)]:
    add(label, GROUP, x, 68, w, 490)

acr = icon("containers/Container_Registries", "<b>Container Registry</b>", 408, 130, lw=165)
app = icon("other/Worker_Container_App", "<b>Container Apps</b><br><font color='#777777'>website</font>", 408, 400, lw=165)

blob = icon("storage/Storage_Accounts", "<b>Blob Storage + Files</b><br><font color='#777777'>raw → processed → mart</font>", 638, 130, lw=210)
pg = icon("databases/Azure_Database_PostgreSQL_Server",
          "<b>Azure Database for<br>PostgreSQL</b>", 638, 400, lw=200, lh=54)

ai = add("Azure AI services", "rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#F5F9FF;strokeColor=#999999;dashed=1;"
         "verticalAlign=top;align=center;spacingTop=2;fontStyle=1;fontSize=13;fontFamily={FONT};fontColor=#222222;",
         828, 122, 255, 222)
icon("ai_machine_learning/Cognitive_Services", "<b>Foundry</b><br><font color='#777777'>models, agents</font>", 868, 146, size=40, lw=110, lh=40)
icon("app_services/Search_Services", "<b>AI Search</b><br><font color='#777777'>job matching</font>", 988, 146, size=40, lw=110, lh=40)
icon("ai_machine_learning/Form_Recognizers", "<b>Document Intel.</b><br><font color='#777777'>résumés</font>", 868, 240, size=40, lw=110, lh=40)
icon("ai_machine_learning/Speech_Services", "<b>Speech</b><br><font color='#777777'>mock interviews</font>", 988, 240, size=40, lw=110, lh=40)
jobs = icon("other/Worker_Container_App", "<b>Container Apps Jobs</b><br><font color='#777777'>~60 scheduled</font>", 923, 400, lw=200)

src = sources(1110, 396)

edge(dev, acr, exit=(1, 0.5), entry=(0, 0.5), dashed=True, at=0.5)
edge(LABEL[acr], app, exit=(0.5, 1), entry=(0.5, 0), dashed=True)
edge(users, cf, exit=(1, 0.5), entry=(0, 0.5))
edge(cf, fd, exit=(1, 0.5), entry=(0, 0.5))
edge(fd, app, exit=(1, 0.5), entry=(0, 0.5))
edge(LABEL[app], saas, exit=(0.5, 1), entry=(1, 0.5), dashed=True,
     points=[(440, 545), (290, 545), (290, 600)], at=0.2)
edge(app, pg, exit=(1, 0.5), entry=(0, 0.5), at=0.2)
edge(LABEL[blob], pg, exit=(0.5, 1), entry=(0.5, 0))
edge(jobs, blob, exit=(0, 0.25), entry=(1, 0.5), points=[(810, 416), (810, 162)], at=0.7)
edge(jobs, ai, exit=(0.5, 0), entry=(0.5, 1))
edge(app, ai, exit=(1, 0.2), entry=(0.5, 0), dashed=True, points=[(518, 413), (518, 106), (955, 106)])
edge(src, jobs, exit=(0, 0.5), entry=(1, 0.5))

box("Security & operations", 365, 570, 720, 95, fill="#F5F9FF", size=14, dashed=True)
icon("security/Key_Vaults", "<b>Key Vault</b>", 378, 603, size=42, lw=90, pos="right")
icon("identity/Managed_Identities", "<b>Managed identity</b>", 522, 603, size=42, lw=90, pos="right")
icon("networking/NAT", "<b>NAT Gateway</b><br><font color='#777777'>static IP out</font>", 666, 603, size=42, lw=90, pos="right")
icon("management_governance/Monitor", "<b>Monitor alerts</b>", 810, 603, size=42, lw=85, pos="right")
icon("devops/Application_Insights", "<b>App Insights</b>", 954, 603, size=42, lw=80, pos="right")

for n, (x, y, v) in enumerate([(132, 432, 0), (490, 432, 2), (1050, 432, 0), (810, 300, 3), (955, 370, 1),
                                (670, 330, 1)], 1):
    step(n, x, y, v)

legend()
save("fig_architecture")
