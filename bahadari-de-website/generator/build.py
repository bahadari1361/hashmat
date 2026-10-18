# -*- coding: utf-8 -*-
"""Generates the static bilingual site. Run:  python3 build.py
All internal links are RELATIVE, so the site works on GitHub Pages
with a custom domain, on username.github.io/repo/, and locally."""
import os, html, datetime
from content import CONFIG, ROUTES, UI, SERVICES, PROJECTS, FEATURED, CERT_GROUPS

OUT = os.environ.get("OUT", os.path.join(os.path.dirname(__file__), "..", "site"))
C = CONFIG
e = html.escape
PROJ = {p["id"]: p for p in PROJECTS}

EN_TERMS = {"SharePoint-Listen": "SharePoint lists", "Netzwerksicherheit": "Network security",
            "HTML-E-Mail": "HTML email", "ERP-Desktop-Client": "ERP desktop client",
            "REST-APIs (z. B. Trello)": "REST APIs (e.g. Trello)", "Netzwerk & VPN": "Networking & VPN",
            "Backup-Lösungen": "Backup solutions", "Excel & Power Query": "Excel & Power Query"}
def term(t, lang): return EN_TERMS.get(t, t) if lang == "en" else t

# ------------------------------------------------------------ paths
def path_of(key, lang):
    if key.startswith("p:"):
        p = PROJ[key[2:]]
        base = ROUTES["projects"][0 if lang == "de" else 1]
        return base + p["slug"][0 if lang == "de" else 1] + "/"
    return ROUTES[key][0 if lang == "de" else 1]

def depth(path): return path.count("/")

def href(frm, to):
    pre = "../" * depth(frm)
    target = pre + to
    return target if target else "./"

def asset(frm, a): return "../" * depth(frm) + a

# ------------------------------------------------------------ icons
ICONS = {
 "flow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="6" height="6" rx="1.5"/><rect x="15" y="15" width="6" height="6" rx="1.5"/><path d="M9 6h4a3 3 0 0 1 3 3v6"/><path d="M13.5 12.5 16 15l2.5-2.5"/></svg>',
 "cloud": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 18h10.5a4 4 0 0 0 .6-7.96A6 6 0 0 0 6.3 9.2 4.4 4.4 0 0 0 7 18Z"/><path d="m10 13.5 1.6 1.6 3-3"/></svg>',
 "server": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01M11 7.5h6M11 16.5h6"/></svg>',
 "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5Z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 21H20"/><path d="M9 8h7M9 11.5h5"/></svg>',
 "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/></svg>',
 "github": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.52 2.34 1.08 2.91.83.09-.65.35-1.08.63-1.33-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.91-1.3 2.75-1.02 2.75-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85v2.75c0 .27.18.58.69.48A10 10 0 0 0 12 2Z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.2 7-11.5a7 7 0 0 0-14 0C5 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 "lang": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
}
MENU_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

# ------------------------------------------------------------ layout
def layout(key, lang, title, desc, body):
    u = UI[lang]
    me = path_of(key, lang)
    other = u["other"]
    alt = path_of(key, other)
    is_services = key in SERVICES or key == "services"
    is_projects = key.startswith("p:") or key == "projects"

    nav_items = []
    for k, label in u["nav"]:
        cur = (k == key) or (k == "services" and is_services) or (k == "projects" and is_projects)
        nav_items.append(f'<li><a href="{href(me, path_of(k, lang))}"{" aria-current=\"page\"" if cur else ""}>{e(label)}</a></li>')
    nav_items.append(f'<li class="menu-cta"><a class="btn btn-primary btn-sm" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a></li>')

    svc_links = "".join(f'<li><a href="{href(me, path_of(k, lang))}">{e(SERVICES[k][lang]["title"])}</a></li>' for k in SERVICES)
    site_links = "".join(f'<li><a href="{href(me, path_of(k, lang))}">{e(l)}</a></li>' for k, l in [("home", u["home"])] + u["nav"][1:4])
    legal = [("imprint", "Impressum" if lang == "de" else "Legal notice"), ("privacy", "Datenschutz" if lang == "de" else "Privacy policy")]
    legal_links = " &nbsp; ".join(f'<a href="{href(me, path_of(k, lang))}">{e(l)}</a>' for k, l in legal)

    canonical = C["base_url"] + me
    alt_url = C["base_url"] + alt
    de_url = C["base_url"] + path_of(key, "de")
    en_url = C["base_url"] + path_of(key, "en")
    full_title = f"{title} | {C['name']}" if key != "home" else f"{C['name']} | {u['tagline']}"

    ld = ""
    if key == "home":
        ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfessionalService",'
              f'"name":"{C["name"]} – {u["tagline"]}","url":"{C["base_url"]}","email":"{C["email"]}",'
              '"areaServed":"DE","address":{"@type":"PostalAddress","addressLocality":"Bremen","addressCountry":"DE"},'
              f'"founder":{{"@type":"Person","name":"{C["name"]}","jobTitle":"IT Systems Administrator & Digital Automation Specialist","sameAs":["{C["github"]}"]}}}}</script>')

    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="de" href="{de_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{de_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{"de_DE" if lang == "de" else "en_GB"}">
<meta name="theme-color" content="#0A2540">
<link rel="icon" href="{asset(me, "favicon.svg")}" type="image/svg+xml">
<link rel="preload" href="{asset(me, "assets/fonts/schibsted-grotesk-latin-400-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{asset(me, "assets/fonts/schibsted-grotesk-latin-700-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset(me, "assets/css/style.css")}">
{ld}
</head>
<body>
<a class="skip" href="#main">{e(u["skip"])}</a>
<header class="site-header">
  <nav class="wrap nav" aria-label="{"Hauptnavigation" if lang == "de" else "Main navigation"}">
    <a class="brand" href="{href(me, path_of("home", lang))}">
      <img src="{asset(me, "assets/img/logo.svg")}" alt="" width="38" height="38">
      <span><strong>{e(C["name"])}</strong><em>{e(u["tagline"])}</em></span>
    </a>
    <ul class="menu" id="menu">{"".join(nav_items)}</ul>
    <div class="nav-tools">
      <a class="lang" href="{href(me, alt)}" hreflang="{other}" lang="{other}" aria-label="{e(u["switch_label"])}">{u["switch"]}</a>
      <a class="btn btn-primary btn-sm" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a>
      <button class="menu-toggle" aria-controls="menu" aria-expanded="false" aria-label="{e(u["menu"])}">{MENU_ICON}</button>
    </div>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{href(me, path_of("home", lang))}"><img src="{asset(me, "assets/img/logo.svg")}" alt="" width="38" height="38"><span><strong>{e(C["name"])}</strong><em>{e(u["tagline"])}</em></span></a>
        <p class="small" style="color:#A9C1D9">{e(u["footer_about"])}</p>
      </div>
      <div><h4>{e(u["footer_services"])}</h4><ul>{svc_links}</ul></div>
      <div><h4>{e(u["footer_site"])}</h4><ul>{site_links}</ul></div>
      <div><h4>{e(u["footer_contact"])}</h4><ul>
        <li><a href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a></li>
        <li><a href="mailto:{C["email"]}">{e(u["cta_mail"])}</a></li>
        <li><a href="{C["github"]}" target="_blank" rel="noopener">GitHub</a></li>
        <li><a href="{href(me, path_of("contact", lang))}">{e(u["nav"][4][1])}</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">{datetime.date.today().year}</span> {e(C["name"])}. {e(u["rights"])}</span>
      <span>{legal_links}</span>
    </div>
  </div>
</footer>
<script src="{asset(me, "assets/js/main.js")}" defer></script>
</body>
</html>
'''

def write(key, lang, title, desc, body):
    p = path_of(key, lang)
    d = os.path.join(OUT, p)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(layout(key, lang, title, desc, body))

def page_head(key, lang, h1, lead, crumbs=None):
    me = path_of(key, lang)
    u = UI[lang]
    trail = [("home", u["home"])] + (crumbs or [])
    cr = " / ".join(f'<a href="{href(me, path_of(k, lang))}">{e(l)}</a>' for k, l in trail)
    return f'''<section class="page-head"><div class="wrap">
<p class="crumbs">{cr}</p>
<h1>{e(h1)}</h1>
<p class="lead">{e(lead)}</p>
</div></section>'''

def cta(key, lang):
    u = UI[lang]
    return f'''<section class="section-tight"><div class="wrap"><div class="cta-band">
<div><h2>{e(u["cta_h"])}</h2><p>{e(u["cta_p"])}</p></div>
<div class="btn-row"><a class="btn btn-light" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a>
<a class="btn btn-ghost" style="color:#fff;border-color:rgba(255,255,255,.55)" href="mailto:{C["email"]}">{e(u["cta_mail"])}</a></div>
</div></div></section>'''

def kicker(p, lang): return p[lang]["kicker"].replace(" · ", ", ")

def project_card(me, pid, lang):
    p = PROJ[pid]; t = p[lang]
    tags = "".join(f"<li>{e(term(s, lang))}</li>" for s in p["stack"][:4])
    return f'''<a class="card project-card" href="{href(me, path_of("p:" + pid, lang))}">
<p class="kicker">{e(kicker(p, lang))}</p>
<h3>{e(t["title"])}</h3>
<p>{e(t["summary"])}</p>
<ul class="tags">{tags}</ul>
<span class="more">{e(UI[lang]["read_case"])}</span>
</a>'''

def service_card(me, k, lang):
    s = SERVICES[k]
    return f'''<a class="card" href="{href(me, path_of(k, lang))}">
<div class="icon">{ICONS[s["icon"]]}</div>
<h3>{e(s[lang]["title"])}</h3>
<p>{e(s[lang]["short"])}</p>
<span class="more">{e(UI[lang]["learn_more"])}</span>
</a>'''

# ------------------------------------------------------------ hero diagram
def hero_svg(lang):
    cap = ("Ein typischer Ablauf: Daten aus Excel, Outlook und Forms laufen über Power Automate nach Trello, Teams und SharePoint – abgesichert über Entra ID."
           if lang == "de" else
           "A typical flow: data from Excel, Outlook and Forms runs through Power Automate into Trello, Teams and SharePoint – secured by Entra ID.")
    def node(x, y, w, label, cls=""):
        return f'<g class="node {cls}"><rect x="{x}" y="{y}" width="{w}" height="40" rx="10"/><text x="{x + w/2}" y="{y + 25}" text-anchor="middle">{label}</text></g>'
    paths = [
        ("p1", "M130 80 C165 80 160 200 190 204", "d1"),
        ("p2", "M130 210 H190", "d2"),
        ("p3", "M130 340 C165 340 160 220 190 216", "d3"),
        ("p4", "M330 202 C360 202 355 80 390 80", "d4"),
        ("p5", "M330 210 H390", "d5"),
        ("p6", "M330 218 C360 218 355 340 390 340", "d6"),
    ]
    lines = "".join(f'<path id="{i}" class="flow-line {c}" d="{d}"/>' for i, d, c in paths)
    dots = "".join(
        f'<circle class="flow-dot" r="3.5"><animateMotion dur="{3 + n*0.4}s" begin="{n*0.3}s" repeatCount="indefinite"><mpath href="#{i}"/></animateMotion></circle>'
        for n, (i, _, _) in enumerate(paths))
    return f'''<figure class="hero-map" aria-label="{e(cap)}">
<svg viewBox="0 0 520 420" role="img" aria-hidden="true">
{lines}
<path class="flow-line d7" d="M260 102 V182" style="stroke-dasharray:4 4;stroke-dashoffset:0;animation:none;opacity:.7"/>
{node(20, 60, 110, "Excel")}{node(20, 190, 110, "Outlook")}{node(20, 320, 110, "Forms")}
<g class="node hub"><rect x="190" y="182" width="140" height="56" rx="14"/><text x="260" y="215" text-anchor="middle">Power Automate</text></g>
{node(390, 60, 110, "Trello")}{node(390, 190, 110, "Teams")}{node(390, 320, 110, "SharePoint")}
{node(205, 62, 110, "Entra ID", "guard")}
{dots}
</svg>
<figcaption>{e(cap)}</figcaption>
</figure>'''

# ------------------------------------------------------------ pages
def home(lang):
    key = "home"; me = path_of(key, lang); u = UI[lang]
    if lang == "de":
        h1 = "IT, die läuft. Abläufe, die sich selbst erledigen."
        lead = "Ich betreue Systeme, Microsoft 365 und Azure für kleine und mittlere Unternehmen – und automatisiere die Prozesse, die heute noch per Hand, per Excel oder per Zuruf laufen."
        hero_name = "Hashmat Bahadari, Bremen"
        btn2 = "Projekte ansehen"
        facts = [("6+ Jahre", "Berufserfahrung in der IT"), ("2.500+", "betreute Nutzer an 34 Standorten"),
                 ("≈ 1.600", "Kunden in automatisierten Wartungsmails"), ("12", "Zertifizierungen in Sicherheit und Cloud")]
        svc_h, svc_p = "Was ich für Sie übernehme", "Vier Bereiche, die in der Praxis ineinandergreifen: Ein sicherer Tenant ist die Grundlage für jede Automatisierung, und ein Intranet ist nur so gut wie die Abläufe dahinter."
        prj_h, prj_p = "Ausgewählte Projekte", "Echte Projekte aus dem Mittelstand, mit Ausgangslage, Vorgehen und Ergebnis. Kundennamen sind anonymisiert."
        how_h = "So arbeite ich"
        how_p = "Kein großes Konzeptpapier vorab, sondern kleine Schritte, die schnell zeigen, ob etwas funktioniert."
        steps = [("Verstehen", "Ich schaue mir den Ablauf an, wie er heute wirklich läuft – nicht wie er im Handbuch steht."),
                 ("Pilotieren", "Eine erste Version mit einem kleinen Team und echten Daten. Was nicht trägt, fliegt raus."),
                 ("Ausrollen", "Erst wenn der Pilot überzeugt, geht die Lösung an alle – mit kurzer Einweisung."),
                 ("Übergeben", "Sie bekommen eine Dokumentation, mit der Ihr Team die Lösung selbst pflegen kann.")]
        sec_h = "Sicherheit ist kein Zusatzpaket"
        sec_p = "Meine Wurzeln liegen in der IT-Sicherheit. Bevor ich etwas automatisiere, prüfe ich, wer worauf Zugriff hat. Das ist bei zehn Arbeitsplätzen genauso wichtig wie bei zweieinhalbtausend."
        sec_link = "Zertifizierungen ansehen"
    else:
        h1 = "IT that runs. Processes that take care of themselves."
        lead = "I look after systems, Microsoft 365 and Azure for small and mid-sized businesses – and automate the processes that still run by hand, by spreadsheet or by word of mouth."
        hero_name = "Hashmat Bahadari, Bremen"
        btn2 = "View projects"
        facts = [("6+ years", "of professional IT experience"), ("2,500+", "users supported across 34 sites"),
                 ("≈ 1,600", "customers in automated maintenance emails"), ("12", "certifications in security and cloud")]
        svc_h, svc_p = "What I take care of", "Four areas that work hand in hand: a secure tenant is the base for any automation, and an intranet is only as good as the processes behind it."
        prj_h, prj_p = "Selected projects", "Real projects from mid-sized businesses, with starting point, approach and outcome. Client names are anonymised."
        how_h = "How I work"
        how_p = "No thick concept paper up front, but small steps that quickly show whether something works."
        steps = [("Understand", "I look at the process as it really runs today – not as it’s written in the manual."),
                 ("Pilot", "A first version with a small team and real data. Whatever doesn’t hold up gets dropped."),
                 ("Roll out", "Only once the pilot convinces does the solution go to everyone – with a short introduction."),
                 ("Hand over", "You get documentation that lets your team maintain the solution themselves.")]
        sec_h = "Security is not an add-on"
        sec_p = "My roots are in IT security. Before I automate anything, I check who has access to what. That matters for ten workstations just as much as for two and a half thousand."
        sec_link = "View certifications"

    facts_html = "".join(f'<div class="fact"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in facts)
    svc = "".join(service_card(me, k, lang) for k in SERVICES)
    prj = "".join(project_card(me, pid, lang) for pid in FEATURED)
    st = "".join(f"<li><strong>{e(a)}</strong>{e(b)}</li>" for a, b in steps)
    certs = ["ISO/IEC 27001 Senior Lead Auditor", "AZ-500", "SC-900", "AZ-900", "CEH", "CompTIA Security+", "CompTIA Network+", "Fortinet NSE 2"]
    cert_tags = "".join(f"<li>{e(c)}</li>" for c in certs)

    body = f'''<section class="hero"><div class="wrap">
<div class="hero-grid">
  <div>
    <p class="hero-name">{e(hero_name)}</p>
    <h1>{e(h1)}</h1>
    <p class="lead">{e(lead)}</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a>
      <a class="btn btn-ghost" href="{href(me, path_of("projects", lang))}">{e(btn2)}</a>
    </div>
  </div>
  {hero_svg(lang)}
</div>
<div class="facts" style="margin-top:clamp(2.5rem,5vw,4rem)">{facts_html}</div>
</div></section>

<section class="section section-white"><div class="wrap">
<div class="section-head"><h2>{e(svc_h)}</h2><p>{e(svc_p)}</p></div>
<div class="grid-2">{svc}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><h2>{e(prj_h)}</h2><p>{e(prj_p)}</p></div>
<div class="grid-3">{prj}</div>
<div class="btn-row"><a class="btn btn-ghost" href="{href(me, path_of("projects", lang))}">{e(u["all_projects"])}</a></div>
</div></section>

<section class="section section-white"><div class="wrap">
<div class="grid-2" style="gap:clamp(2rem,5vw,5rem);align-items:start">
  <div><h2>{e(how_h)}</h2><p class="lead">{e(how_p)}</p><ol class="steps">{st}</ol></div>
  <div><h2>{e(sec_h)}</h2><p>{e(sec_p)}</p><ul class="tags" style="margin-top:1.25rem">{cert_tags}</ul>
  <p><a href="{href(me, path_of("certs", lang))}">{e(sec_link)}</a></p></div>
</div>
</div></section>
{cta(key, lang)}'''
    desc = lead
    write(key, lang, h1, desc, body)

def services_page(lang):
    key = "services"; me = path_of(key, lang); u = UI[lang]
    if lang == "de":
        h1 = "Leistungen"
        lead = "IT-Betrieb, Microsoft Cloud und Automatisierung aus einer Hand – für Unternehmen, die keine eigene IT-Abteilung haben oder ihre bestehende entlasten wollen."
        who_h = "Für wen ich arbeite"
        who = [("Kleine und mittlere Unternehmen", "Betriebe mit 5 bis 250 Mitarbeitenden, die Microsoft 365 nutzen oder einführen wollen."),
               ("Handwerk und Haustechnik", "Ich kenne die Abläufe von Anfrage, Angebot, Montage und Wartung aus eigener Projektarbeit."),
               ("Privatpersonen und Selbstständige", "Einrichtung, Absicherung und Hilfe, wenn etwas nicht mehr funktioniert.")]
        how_h = "Wie eine Zusammenarbeit aussieht"
        how = [("Erstgespräch", "30 Minuten, kostenlos, per Teams oder Telefon. Sie schildern die Lage, ich stelle Fragen."),
               ("Einschätzung", "Sie erhalten eine kurze schriftliche Einschätzung mit Vorschlag und Aufwand."),
               ("Umsetzung", "In abgestimmten Schritten, remote oder vor Ort im Raum Bremen."),
               ("Betreuung", "Auf Wunsch übernehme ich danach den laufenden Betrieb oder stehe bei Bedarf bereit.")]
    else:
        h1 = "Services"
        lead = "IT operations, Microsoft cloud and automation from one person – for businesses without their own IT department, or that want to take load off the one they have."
        who_h = "Who I work with"
        who = [("Small and mid-sized businesses", "Companies with 5 to 250 employees using or introducing Microsoft 365."),
               ("Trades and building services", "I know the path from enquiry to quote, installation and maintenance from hands-on project work."),
               ("Individuals and freelancers", "Setup, security, and help when something stops working.")]
        how_h = "What working together looks like"
        how = [("Intro call", "30 minutes, free, via Teams or phone. You describe the situation, I ask questions."),
               ("Assessment", "You receive a short written assessment with a proposal and effort estimate."),
               ("Delivery", "In agreed steps, remotely or on site around Bremen."),
               ("Support", "If you like, I take over ongoing operations afterwards or stay available as needed.")]
    cards = "".join(service_card(me, k, lang) for k in SERVICES)
    who_html = "".join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in who)
    how_html = "".join(f"<li><strong>{e(a)}</strong>{e(b)}</li>" for a, b in how)
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap"><div class="grid-2">{cards}</div></div></section>
<section class="section section-white"><div class="wrap">
<h2>{e(who_h)}</h2><div class="grid-3" style="margin-top:1.5rem">{who_html}</div>
</div></section>
<section class="section"><div class="wrap" style="max-width:860px">
<h2>{e(how_h)}</h2><ol class="steps">{how_html}</ol>
</div></section>
{cta(key, lang)}'''
    write(key, lang, h1, lead, body)

def service_detail(k, lang):
    s = SERVICES[k]; t = s[lang]; me = path_of(k, lang); u = UI[lang]
    items = "".join(f"<li>{e(i)}</li>" for i in t["items"])
    outs = "".join(f"<li>{e(i)}</li>" for i in t["outcomes"])
    rel = "".join(project_card(me, pid, lang) for pid in s["projects"][:3])
    tools = "".join(f"<li>{e(term(x, lang))}</li>" for x in s["tools"])
    certs = "".join(f"<li>{e(x)}</li>" for x in s["certs"])
    body = page_head(k, lang, t["h1"], t["short"], [("services", u["nav"][0][1])]) + f'''
<section class="section"><div class="wrap split">
<div class="prose">
  <p class="lead" style="color:var(--ink)">{e(t["intro"])}</p>
  <h2>{e(u["what"])}</h2><ul class="checks">{items}</ul>
  <h2>{e(u["outcome"])}</h2><ul>{outs}</ul>
</div>
<aside class="aside-box">
  <h3>{e(u["tools"])}</h3><ul class="tags">{tools}</ul>
  <h3 style="margin-top:1.25rem">{e(u["certs_rel"])}</h3><ul class="tags">{certs}</ul>
  <a class="btn btn-primary btn-sm" style="margin-top:.75rem" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a>
</aside>
</div></section>
<section class="section section-white"><div class="wrap">
<h2>{e(u["related"])}</h2>
<div class="grid-3" style="margin-top:1.5rem">{rel}</div>
</div></section>
{cta(k, lang)}'''
    write(k, lang, t["title"], t["short"], body)

def projects_page(lang):
    key = "projects"; me = path_of(key, lang)
    if lang == "de":
        h1 = "Projekte"
        lead = "Eine Auswahl an Projekten aus Automatisierung, Microsoft 365 und IT-Sicherheit. Jede Fallstudie zeigt Ausgangslage, Vorgehen und Ergebnis – ehrlich, auch wo ein Projekt noch im Pilot läuft."
        note = "Kunden und Arbeitgeber sind anonymisiert. Interne Daten, Zugangsdaten und vertrauliche Vorgänge werden grundsätzlich nicht veröffentlicht."
    else:
        h1 = "Projects"
        lead = "A selection of projects in automation, Microsoft 365 and IT security. Each case study shows the starting point, approach and outcome – honestly, including where a project is still in pilot."
        note = "Clients and employers are anonymised. Internal data, credentials and confidential matters are never published."
    cards = "".join(project_card(me, p["id"], lang) for p in PROJECTS)
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap">
<div class="grid-2">{cards}</div>
<p class="small" style="margin-top:2rem">{e(note)}</p>
</div></section>
{cta(key, lang)}'''
    write(key, lang, h1, lead, body)

def project_detail(idx, lang):
    p = PROJECTS[idx]; t = p[lang]; key = "p:" + p["id"]; me = path_of(key, lang); u = UI[lang]
    steps = "".join(f"<li><strong>{e(a)}</strong>{e(b)}</li>" for a, b in t["steps"])
    res = "".join(f"<li>{e(r)}</li>" for r in t["result"])
    tags = "".join(f"<li>{e(term(s, lang))}</li>" for s in p["stack"])
    prev = PROJECTS[idx - 1]; nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    body = page_head(key, lang, t["title"], t["summary"], [("projects", u["nav"][1][1])]) + f'''
<section class="section"><div class="wrap split">
<article class="prose">
  <h2>{e(u["context_h"])}</h2><p>{e(t["context"])}</p>
  <h2>{e(u["approach_h"])}</h2><ol class="steps">{steps}</ol>
  <div class="result"><h2>{e(u["result_h"])}</h2><ul>{res}</ul></div>
  <h2>{e(u["lessons_h"])}</h2><p>{e(t["details"])}</p>
  <nav class="pager" aria-label="{"Projektnavigation" if lang == "de" else "Project navigation"}">
    <a href="{href(me, path_of("p:" + prev["id"], lang))}"><span>{e(u["prev"])}</span>{e(prev[lang]["title"])}</a>
    <a href="{href(me, path_of("p:" + nxt["id"], lang))}" style="text-align:right"><span>{e(u["next"])}</span>{e(nxt[lang]["title"])}</a>
  </nav>
</article>
<aside class="aside-box">
  <h3>{e(u["facts_title"])}</h3>
  <dl>
    <dt>{e(u["type"])}</dt><dd>{e(t["type"])}</dd>
    <dt>{e(u["role"])}</dt><dd>{e(t["role"])}</dd>
    <dt>{e(u["stack"])}</dt><dd><ul class="tags" style="margin-top:.4rem">{tags}</ul></dd>
  </dl>
  <a class="btn btn-primary btn-sm" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a>
</aside>
</div></section>
{cta(key, lang)}'''
    write(key, lang, t["title"], t["summary"], body)

def about_page(lang):
    key = "about"; me = path_of(key, lang)
    if lang == "de":
        h1 = "Über mich"
        lead = "Ich bin Hashmat Bahadari, IT-Systemadministrator und Spezialist für digitale Automatisierung aus Bremen."
        paras = [
            "Ich komme aus der IT-Sicherheit. Mehrere Jahre habe ich in einer nationalen Zentralbank gearbeitet, mit über 2.500 Nutzern an 34 Standorten. Dort habe ich gelernt, sauber zu dokumentieren, Änderungen zu begründen und Risiken früh zu erkennen.",
            "Heute arbeite ich mit dem Mittelstand, vor allem mit Handwerks- und Haustechnikbetrieben. Dort sehe ich jeden Tag, wie viel Zeit in Excel-Listen, weitergeleiteten E-Mails und Zetteln steckt. Genau da setze ich an: Ich richte Microsoft 365 sicher ein und baue Abläufe, die Menschen entlasten statt sie zu kontrollieren.",
            "Mir ist wichtig, dass meine Lösungen auch ohne mich funktionieren. Deshalb starte ich klein, teste mit echten Daten und übergebe am Ende eine Dokumentation, die Ihr Team versteht.",
        ]
        facts_h = "Auf einen Blick"
        facts = [("Ausbildung", "B.Sc. Informatik (von der ZAB anerkannt)"), ("Erfahrung", "Über 6 Jahre in IT-Administration und IT-Sicherheit"),
                 ("Schwerpunkte", "Microsoft 365, Azure, Power Platform, IT-Sicherheit"), ("Standort", "Bremen – remote und vor Ort")]
        lang_h = "Sprachen"; langs = ["Deutsch", "Englisch", "Persisch"]
        val_h = "Worauf Sie sich verlassen können"
        vals = ["Ehrliche Einschätzungen, auch wenn die Antwort „das lohnt sich nicht“ lautet",
                "Vertraulichkeit: Ihre Daten und Vorgänge bleiben bei Ihnen",
                "Lösungen auf Basis dessen, was Sie schon lizenziert haben",
                "Erklärungen ohne Fachchinesisch"]
    else:
        h1 = "About"
        lead = "I’m Hashmat Bahadari, an IT systems administrator and digital automation specialist based in Bremen, Germany."
        paras = [
            "My background is in IT security. I spent several years at a national central bank, supporting more than 2,500 users across 34 sites. That’s where I learned to document properly, justify every change and spot risks early.",
            "Today I work with mid-sized businesses, especially in the trades and building services. Every day I see how much time goes into spreadsheets, forwarded emails and notes on paper. That’s where I come in: I set up Microsoft 365 securely and build processes that take load off people rather than policing them.",
            "I want my solutions to work without me. So I start small, test with real data and hand over documentation your team can actually follow.",
        ]
        facts_h = "At a glance"
        facts = [("Education", "B.Sc. in Computer Science (recognised by Germany’s ZAB)"), ("Experience", "6+ years in IT administration and security"),
                 ("Focus", "Microsoft 365, Azure, Power Platform, IT security"), ("Location", "Bremen – remote and on site")]
        lang_h = "Languages"; langs = ["German", "English", "Persian"]
        val_h = "What you can count on"
        vals = ["Honest assessments, even when the answer is “that’s not worth it”",
                "Confidentiality: your data and business stay yours",
                "Solutions built on what you already license",
                "Explanations without jargon"]
    p_html = "".join(f"<p>{e(x)}</p>" for x in paras)
    f_html = "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in facts)
    l_html = "".join(f"<li>{e(x)}</li>" for x in langs)
    v_html = "".join(f"<li>{e(x)}</li>" for x in vals)
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap about-grid">
<div>
  <div class="portrait" aria-hidden="true">HB<!-- Replace with: <img src="../assets/img/portrait.jpg" alt="Hashmat Bahadari"> --></div>
  <div class="aside-box" style="position:static;margin-top:1.25rem"><h3>{e(facts_h)}</h3><dl>{f_html}</dl></div>
</div>
<div class="prose">
  {p_html}
  <h2>{e(val_h)}</h2><ul class="checks">{v_html}</ul>
  <h2>{e(lang_h)}</h2><ul class="langs">{l_html}</ul>
  <div class="btn-row">
    <a class="btn btn-primary" href="{C["booking"]}" target="_blank" rel="noopener">{e(UI[lang]["book"])}</a>
    <a class="btn btn-ghost" href="{href(me, path_of("certs", lang))}">{e(UI[lang]["nav"][3][1])}</a>
  </div>
</div>
</div></section>
{cta(key, lang)}'''
    write(key, lang, h1, lead, body)

def certs_page(lang):
    key = "certs"
    if lang == "de":
        h1 = "Zertifizierungen"
        lead = "Zertifikate ersetzen keine Erfahrung, aber sie zeigen, dass das Fundament stimmt. Meine Schwerpunkte liegen bei Informationssicherheit, Microsoft Azure und Netzwerken."
        note = "Nachweise lege ich auf Anfrage gern vor."
    else:
        h1 = "Certifications"
        lead = "Certificates don’t replace experience, but they show the foundation is solid. My focus is information security, Microsoft Azure and networking."
        note = "Proof of certification is available on request."
    groups = ""
    for g in CERT_GROUPS:
        items = ""
        for badge, name, issuer, de, en in g["items"]:
            items += f'''<div class="card cert"><div class="cert-badge">{e(badge)}</div><div>
<p class="issuer">{e(issuer)}</p><h3>{e(name)}</h3><p>{e(de if lang == "de" else en)}</p></div></div>'''
        groups += f'<h2 style="margin-top:2.5rem;font-size:1.5rem">{e(g[lang])}</h2><div class="grid-2">{items}</div>'
    body = page_head(key, lang, h1, lead) + f'''
<section class="section" style="padding-top:1rem"><div class="wrap">{groups}
<p class="small" style="margin-top:2rem">{e(note)}</p></div></section>
{cta(key, lang)}'''
    write(key, lang, h1, lead, body)

def contact_page(lang):
    key = "contact"; u = UI[lang]
    if lang == "de":
        h1 = "Kontakt"
        lead = "Am schnellsten geht es über einen Termin im Kalender. Für kurze Fragen erreichen Sie mich per E-Mail."
        book_h = "Erstgespräch buchen"
        book_p = "Wählen Sie einen freien Termin in meinem Kalender. Das Gespräch dauert 30 Minuten, findet per Microsoft Teams statt und ist kostenlos."
        prep_h = "Hilfreich für das Gespräch"
        prep = ["Kurz beschreiben, was heute nicht rund läuft", "Welche Microsoft-365-Lizenzen vorhanden sind (falls bekannt)", "Wie viele Personen betroffen sind"]
        labels = ("Termin", "E-Mail", "GitHub", "Standort", "Bremen, remote in ganz Deutschland")
        resp = "Ich antworte in der Regel innerhalb von einem Werktag."
    else:
        h1 = "Contact"
        lead = "The quickest way is to book a slot in my calendar. For short questions, email works well."
        book_h = "Book an intro call"
        book_p = "Pick a free slot in my calendar. The call takes 30 minutes, runs on Microsoft Teams and is free of charge."
        prep_h = "Helpful to have ready"
        prep = ["A short description of what isn’t working well today", "Which Microsoft 365 licences you have (if known)", "How many people are affected"]
        labels = ("Appointment", "Email", "GitHub", "Location", "Bremen, remote across Germany")
        resp = "I usually reply within one business day."
    pr = "".join(f"<li>{e(x)}</li>" for x in prep)
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap grid-2" style="gap:clamp(1.5rem,4vw,3rem);align-items:start">
<div class="card" style="padding:clamp(1.75rem,3vw,2.5rem)">
  <div class="icon">{ICONS["calendar"]}</div>
  <h2 style="font-size:1.6rem">{e(book_h)}</h2>
  <p>{e(book_p)}</p>
  <a class="btn btn-primary" href="{C["booking"]}" target="_blank" rel="noopener" style="align-self:flex-start;margin:.5rem 0 1.5rem">{e(u["book"])}</a>
  <h3 style="font-size:1rem">{e(prep_h)}</h3>
  <ul class="checks">{pr}</ul>
</div>
<div>
  <ul class="contact-list">
    <li><div class="icon">{ICONS["calendar"]}</div><div><span>{e(labels[0])}</span><a href="{C["booking"]}" target="_blank" rel="noopener">Microsoft Bookings</a></div></li>
    <li><div class="icon">{ICONS["mail"]}</div><div><span>{e(labels[1])}</span><a href="mailto:{C["email"]}">{e(C["email"])}</a></div></li>
    <li><div class="icon">{ICONS["github"]}</div><div><span>{e(labels[2])}</span><a href="{C["github"]}" target="_blank" rel="noopener">github.com/{e(C["github_handle"])}</a></div></li>
    <li><div class="icon">{ICONS["pin"]}</div><div><span>{e(labels[3])}</span><b>{e(labels[4])}</b></div></li>
  </ul>
  <p class="small" style="margin-top:1.5rem">{e(resp)}</p>
</div>
</div></section>'''
    write(key, lang, h1, lead, body)

def imprint_page(lang):
    key = "imprint"
    phone = f"<br>Telefon: {e(C['phone'])}" if C["phone"] else ""
    vat_de = f"<h2>Umsatzsteuer-ID</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: {e(C['vat_id'])}</p>" if C["vat_id"] else ""
    addr = f'{e(C["legal_name"])}<br>{e(C["street"])}<br>{e(C["city"])}<br>Deutschland'
    if lang == "de":
        h1, lead = "Impressum", "Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)"
        txt = f'''<h2>Anbieter</h2><p>{addr}</p>
<h2>Kontakt</h2><p>E-Mail: <a href="mailto:{C["email"]}">{e(C["email"])}</a>{phone}</p>
{vat_de}
<h2>Verantwortlich für den Inhalt</h2><p>Verantwortlich nach § 18 Abs. 2 MStV:<br>{addr}</p>
<h2>Haftung für Inhalte</h2><p>Die Inhalte dieser Seiten wurden mit Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte kann ich jedoch keine Gewähr übernehmen. Als Diensteanbieter bin ich für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich.</p>
<h2>Haftung für Links</h2><p>Diese Website enthält Links zu externen Websites Dritter, auf deren Inhalte ich keinen Einfluss habe. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter verantwortlich. Bei Bekanntwerden von Rechtsverletzungen entferne ich derartige Links umgehend.</p>
<h2>Urheberrecht</h2><p>Die Inhalte und Grafiken dieser Website unterliegen dem deutschen Urheberrecht. Vervielfältigung und Verwendung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung. Produktnamen wie Microsoft 365, Azure oder Trello sind Marken ihrer jeweiligen Inhaber.</p>
<h2>Verbraucherstreitbeilegung</h2><p>Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>'''
    else:
        h1, lead = "Legal notice", "Information pursuant to Section 5 of the German Digital Services Act (DDG). The German version is legally binding."
        txt = f'''<h2>Provider</h2><p>{addr.replace("Deutschland", "Germany")}</p>
<h2>Contact</h2><p>Email: <a href="mailto:{C["email"]}">{e(C["email"])}</a>{phone.replace("Telefon", "Phone")}</p>
{"<h2>VAT ID</h2><p>" + e(C["vat_id"]) + "</p>" if C["vat_id"] else ""}
<h2>Responsible for content</h2><p>Responsible under Section 18(2) of the German Interstate Media Treaty (MStV):<br>{addr.replace("Deutschland", "Germany")}</p>
<h2>Liability for content</h2><p>The content of these pages was created with care. However, I cannot guarantee that it is accurate, complete or up to date.</p>
<h2>Liability for links</h2><p>This website links to external third-party websites whose content I do not control. The respective provider is always responsible for the content of linked pages. Links will be removed promptly if any infringement becomes known.</p>
<h2>Copyright</h2><p>The content and graphics on this website are subject to German copyright law. Product names such as Microsoft 365, Azure or Trello are trademarks of their respective owners.</p>
<h2>Consumer dispute resolution</h2><p>I am neither willing nor obliged to take part in dispute resolution proceedings before a consumer arbitration board.</p>'''
    body = page_head(key, lang, h1, lead) + f'<section class="section"><div class="wrap legal">{txt}</div></section>'
    write(key, lang, h1, lead, body)

def privacy_page(lang):
    key = "privacy"
    addr = f'{e(C["legal_name"])}, {e(C["street"])}, {e(C["city"])}, E-Mail: <a href="mailto:{C["email"]}">{e(C["email"])}</a>'
    if lang == "de":
        h1, lead = "Datenschutzerklärung", "Informationen zur Verarbeitung personenbezogener Daten nach Art. 13 DSGVO"
        txt = f'''<h2>1. Verantwortlicher</h2><p>{addr}</p>
<h2>2. Das Wichtigste in Kürze</h2><p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Tracking-Werkzeuge und bindet keine Inhalte von Drittanbietern ein. Schriftarten werden lokal vom eigenen Server geladen, nicht von Google.</p>
<h2>3. Hosting über GitHub Pages</h2><p>Die Website wird über GitHub Pages bereitgestellt, einen Dienst der GitHub, Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, USA. Beim Aufruf verarbeitet GitHub technisch notwendige Daten wie Ihre IP-Adresse, Datum und Uhrzeit des Zugriffs, die aufgerufene Seite und Browserinformationen, um die Seite auszuliefern und die Sicherheit zu gewährleisten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer sicheren und stabilen Bereitstellung). Eine Übermittlung in die USA findet statt; GitHub stützt sich dabei auf das EU-US Data Privacy Framework bzw. Standardvertragsklauseln. Weitere Informationen: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">Datenschutzerklärung von GitHub</a>.</p>
<h2>4. Kontakt per E-Mail</h2><p>Wenn Sie mir eine E-Mail schreiben, verarbeite ich Ihre Angaben zur Bearbeitung der Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen) bzw. lit. f DSGVO. Die Daten werden gelöscht, sobald sie nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten bestehen.</p>
<h2>5. Terminbuchung über Microsoft Bookings</h2><p>Für die Terminbuchung verlinke ich auf Microsoft Bookings, einen Dienst der Microsoft Ireland Operations Limited, One Microsoft Place, South County Business Park, Leopardstown, Dublin 18, Irland. Erst wenn Sie den Link anklicken, werden Daten an Microsoft übertragen. Die von Ihnen eingegebenen Daten (Name, E-Mail-Adresse, ggf. Telefonnummer und Anliegen) nutze ich zur Durchführung des Termins. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO. Weitere Informationen: <a href="https://privacy.microsoft.com/de-de/privacystatement" target="_blank" rel="noopener">Datenschutzerklärung von Microsoft</a>.</p>
<h2>6. Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21). Wenden Sie sich dazu einfach per E-Mail an mich.</p>
<h2>7. Beschwerderecht</h2><p>Sie können sich bei einer Datenschutz-Aufsichtsbehörde beschweren. Zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit der Freien Hansestadt Bremen.</p>
<p class="small">Stand: {datetime.date.today().strftime("%m/%Y")}</p>'''
    else:
        h1, lead = "Privacy policy", "How personal data is processed under Art. 13 GDPR. The German version is legally binding."
        txt = f'''<h2>1. Controller</h2><p>{addr}</p>
<h2>2. In short</h2><p>This website sets no cookies, uses no analytics or tracking tools and embeds no third-party content. Fonts are served locally from this site, not from Google.</p>
<h2>3. Hosting on GitHub Pages</h2><p>This website is served via GitHub Pages, a service of GitHub, Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, USA. When you visit, GitHub processes technically necessary data such as your IP address, date and time of access, the requested page and browser information to deliver the site and keep it secure. The legal basis is Art. 6(1)(f) GDPR (legitimate interest in secure and stable delivery). Data is transferred to the USA; GitHub relies on the EU-US Data Privacy Framework and standard contractual clauses. More: <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">GitHub privacy statement</a>.</p>
<h2>4. Contact by email</h2><p>If you email me, I process your details to handle your request. The legal basis is Art. 6(1)(b) GDPR (pre-contractual steps) or Art. 6(1)(f) GDPR. Data is deleted once it’s no longer needed and no statutory retention obligations apply.</p>
<h2>5. Booking via Microsoft Bookings</h2><p>For appointments I link to Microsoft Bookings, a service of Microsoft Ireland Operations Limited, One Microsoft Place, South County Business Park, Leopardstown, Dublin 18, Ireland. Data is only sent to Microsoft once you click the link. I use the details you enter (name, email, phone if given, and your topic) to hold the appointment. The legal basis is Art. 6(1)(b) GDPR. More: <a href="https://privacy.microsoft.com/en-gb/privacystatement" target="_blank" rel="noopener">Microsoft privacy statement</a>.</p>
<h2>6. Your rights</h2><p>You have the right of access (Art. 15 GDPR), rectification (Art. 16), erasure (Art. 17), restriction of processing (Art. 18), data portability (Art. 20) and to object (Art. 21). Just email me.</p>
<h2>7. Right to lodge a complaint</h2><p>You can lodge a complaint with a data protection authority. The competent authority is the State Commissioner for Data Protection and Freedom of Information of the Free Hanseatic City of Bremen.</p>
<p class="small">Last updated: {datetime.date.today().strftime("%m/%Y")}</p>'''
    body = page_head(key, lang, h1, lead) + f'<section class="section"><div class="wrap legal">{txt}</div></section>'
    write(key, lang, h1, lead, body)

def not_found():
    # 404 lives at root; GitHub serves it for any depth, so use absolute paths here only.
    body = '''<section class="page-head"><div class="wrap">
<h1>Seite nicht gefunden</h1>
<p class="lead">Die Adresse existiert nicht oder wurde verschoben. Page not found – the address doesn’t exist or has moved.</p>
<div class="btn-row"><a class="btn btn-primary" href="/">Zur Startseite</a><a class="btn btn-ghost" href="/en/">English home</a></div>
</div></section>'''
    out = layout("home", "de", "404", "Seite nicht gefunden", body)
    # make every relative asset/link absolute for the 404 page
    out = out.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/') \
             .replace('href="favicon.svg"', 'href="/favicon.svg"').replace('src="assets/js', 'src="/assets/js')
    import re
    out = re.sub(r'href="(?!https?:|mailto:|/|#)([^"]*)"', lambda m: f'href="/{m.group(1) if m.group(1) != "./" else ""}"', out)
    out = out.replace(f"<title>{C['name']} | {UI['de']['tagline']}</title>", f"<title>404 | {C['name']}</title>")
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f: f.write(out)

def extras():
    keys = list(ROUTES) + ["p:" + p["id"] for p in PROJECTS]
    today = datetime.date.today().isoformat()
    urls = []
    for k in keys:
        for lang in ("de", "en"):
            loc = C["base_url"] + path_of(k, lang)
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{C["base_url"] + path_of(k, l)}"/>' for l in ("de", "en"))
            urls.append(f"<url><loc>{loc}</loc><lastmod>{today}</lastmod>{alts}</url>")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {C['base_url']}sitemap.xml\n")
    with open(os.path.join(OUT, "CNAME"), "w") as f: f.write(C["domain"] + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    return len(keys) * 2

if __name__ == "__main__":
    for lang in ("de", "en"):
        home(lang); services_page(lang); projects_page(lang); about_page(lang)
        certs_page(lang); contact_page(lang); imprint_page(lang); privacy_page(lang)
        for k in SERVICES: service_detail(k, lang)
        for i in range(len(PROJECTS)): project_detail(i, lang)
    not_found()
    n = extras()
    print(f"Built {n} pages + 404 into {os.path.abspath(OUT)}")
