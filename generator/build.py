# -*- coding: utf-8 -*-
"""bahadari.de generator v3.  Run: python3 build.py   (OUT=path to change output folder)
All internal links are relative, so the site works on GitHub Pages with a custom domain."""
import os, re, html, datetime
from content import CONFIG, ROUTES, UI, SERVICES, SOLUTIONS, FEATURED, CERT_GROUPS
import diagrams as DG

OUT = os.environ.get("OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "site"))
C = CONFIG; e = html.escape
SOL = {s["id"]: s for s in SOLUTIONS}

def path_of(key, lang):
    i = 0 if lang == "de" else 1
    if key.startswith("s:"):
        return ROUTES["solutions"][i] + SOL[key[2:]]["slug"][i] + "/"
    return ROUTES[key][i]

def href(frm, to):
    t = "../" * frm.count("/") + to
    return t or "./"

def asset(frm, a): return "../" * frm.count("/") + a

ICO = {k: f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{v}</svg>' for k, v in DG.IC.items()}
MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

# ------------------------------------------------------------------ layout
def layout(key, lang, title, desc, body):
    u = UI[lang]; me = path_of(key, lang); other = u["other"]
    in_sv = key in SERVICES or key == "services"; in_sol = key.startswith("s:") or key == "solutions"
    nav = []
    for k, label in u["nav"]:
        cur = k == key or (k == "services" and in_sv) or (k == "solutions" and in_sol)
        nav.append(f'<li><a href="{href(me, path_of(k, lang))}"{" aria-current=\"page\"" if cur else ""}>{e(label)}</a></li>')
    nav.append(f'<li class="menu-cta"><a class="btn btn-primary" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a></li>')
    f_sv = "".join(f'<li><a href="{href(me, path_of(k, lang))}">{e(SERVICES[k][lang]["title"])}</a></li>' for k in SERVICES)
    f_co = "".join(f'<li><a href="{href(me, path_of(k, lang))}">{e(l)}</a></li>' for k, l in u["nav"][1:5])
    legal = [("imprint", "Impressum" if lang == "de" else "Legal notice"), ("privacy", "Datenschutz" if lang == "de" else "Privacy policy")]
    legal_l = "".join(f'<a href="{href(me, path_of(k, lang))}">{e(l)}</a>' for k, l in legal)
    de_url, en_url = C["base_url"] + path_of(key, "de"), C["base_url"] + path_of(key, "en")
    full = f"{C['name']} | {u['tagline']}" if key == "home" else f"{title} | {C['name']}"
    ld = ""
    if key == "home":
        ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfessionalService",'
              f'"name":"{C["name"]}","url":"{C["base_url"]}","email":"{C["email"]}","areaServed":"DE",'
              '"address":{"@type":"PostalAddress","addressLocality":"Bremen","addressCountry":"DE"},'
              f'"founder":{{"@type":"Person","name":"{C["name"]}","jobTitle":"IT Systems Administrator & Digital Automation Specialist"}}}}</script>')
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{C["base_url"] + me}">
<link rel="alternate" hreflang="de" href="{de_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{de_url}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{C["base_url"] + me}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{asset(me, "favicon.svg")}" type="image/svg+xml">
<link rel="preload" href="{asset(me, "assets/fonts/schibsted-grotesk-latin-400-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset(me, "assets/css/style.css")}">
{ld}
</head>
<body>
<a class="skip" href="#main">{e(u["skip"])}</a>
<div class="topbar"><div class="wrap topbar-in">
  <span class="tb-loc">{ICO["building"]}Bremen, {"Deutschland" if lang == "de" else "Germany"}</span>
  <a href="mailto:{C["email"]}">{ICO["mail"]}{e(C["email"])}</a>
  <a href="{C["base_url"]}">{ICO["globe"]}{e(C["website"])}</a>
</div></div>
<header class="site-header"><nav class="wrap nav" aria-label="{"Hauptnavigation" if lang == "de" else "Main navigation"}">
  <a class="brand" href="{href(me, path_of("home", lang))}"><img src="{asset(me, "assets/img/logo.svg")}" alt="" width="36" height="36"><span><strong>{e(C["name"])}</strong><em>{e(u["tagline"])}</em></span></a>
  <ul class="menu" id="menu">{"".join(nav)}</ul>
  <div class="nav-tools">
    <a class="lang" href="{href(me, path_of(key, other))}" hreflang="{other}" lang="{other}" aria-label="{e(u["switch_label"])}">{u["switch"]}</a>
    <a class="btn btn-primary btn-sm hide-m" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a>
    <button class="menu-toggle" aria-controls="menu" aria-expanded="false" aria-label="{e(u["menu"])}">{MENU}</button>
  </div>
</nav></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
  <div class="footer-grid">
    <div><a class="brand" href="{href(me, path_of("home", lang))}"><img src="{asset(me, "assets/img/logo.svg")}" alt="" width="36" height="36"><span><strong>{e(C["name"])}</strong><em>{e(u["tagline"])}</em></span></a>
      <p>{e(u["footer_about"])}</p></div>
    <div><h4>{e(u["f_services"])}</h4><ul>{f_sv}</ul></div>
    <div><h4>{e(u["f_company"])}</h4><ul>{f_co}</ul></div>
    <div><h4>{e(u["f_contact"])}</h4><ul>
      <li><a href="mailto:{C["email"]}">{e(C["email"])}</a></li>
      <li><a href="{C["base_url"]}">{e(C["website"])}</a></li>
      <li><a href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a></li>
      <li>Bremen, {"Deutschland" if lang == "de" else "Germany"}</li></ul></div>
  </div>
  <div class="footer-bottom"><span>© <span id="year">{datetime.date.today().year}</span> {e(C["name"])}. {e(u["rights"])}</span><span class="legal-links">{legal_l}</span></div>
</div></footer>
<script src="{asset(me, "assets/js/main.js")}" defer></script>
</body>
</html>
'''

def write(key, lang, title, desc, body):
    d = os.path.join(OUT, path_of(key, lang)); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(layout(key, lang, title, desc, body))

def page_head(key, lang, h1, lead, crumbs=None, eyebrow=None):
    me = path_of(key, lang); u = UI[lang]
    trail = [("home", u["home"])] + (crumbs or [])
    cr = '<span aria-hidden="true">/</span>'.join(f'<a href="{href(me, path_of(k, lang))}">{e(l)}</a>' for k, l in trail)
    eb = f'<p class="eyebrow">{e(eyebrow)}</p>' if eyebrow else ""
    return f'<section class="page-head"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav>{eb}<h1>{e(h1)}</h1><p class="lead">{e(lead)}</p></div></section>'

def figure(dg, caption=None, legend=None, lang="de", compact=False):
    d, leg = dg
    legend = legend if legend is not None else leg
    lg = ""
    if legend:
        lg = '<ol class="legend">' + "".join(f"<li>{e(x)}</li>" for x in legend) + "</ol>"
    cap = f"<p>{e(caption)}</p>" if caption else ""
    foot = f"<figcaption>{cap}{lg}</figcaption>" if (cap or lg) else ""
    return f'<figure class="figure{" compact" if compact else ""}"><div class="figure-bar"><span>{e(d.title)}</span></div><div class="figure-body">{d.svg()}</div>{foot}</figure>'

def cta(lang):
    u = UI[lang]
    return f'''<section class="cta"><div class="wrap cta-in">
<div><h2>{e(u["cta_h"])}</h2><p>{e(u["cta_p"])}</p></div>
<div class="btn-row"><a class="btn btn-primary" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a><a class="btn btn-ghost" href="mailto:{C["email"]}">{e(u["mail"])}</a></div>
</div></section>'''

def sol_card(me, sid, lang):
    s = SOL[sid]; t = s[lang]
    return f'''<a class="card sol-card" href="{href(me, path_of("s:" + sid, lang))}">
<p class="cat">{e(t["cat"])}</p><h3>{e(t["title"])}</h3><p>{e(t["summary"])}</p>
<span class="more">{e(UI[lang]["read"])}</span></a>'''

def svc_card(me, k, lang):
    s = SERVICES[k]; t = s[lang]
    items = "".join(f"<li>{e(i)}</li>" for i in t["items"][:3])
    return f'''<a class="card svc-card" href="{href(me, path_of(k, lang))}">
<div class="icon">{ICO[s["icon"]]}</div><h3>{e(t["title"])}</h3><p>{e(t["short"])}</p>
<ul class="mini">{items}</ul><span class="more">{e(UI[lang]["more"])}</span></a>'''

# ------------------------------------------------------------------ pages
def home(lang):
    key = "home"; me = path_of(key, lang); u = UI[lang]
    if lang == "de":
        h1 = "Zuverlässige IT und automatisierte Abläufe für kleine und mittlere Unternehmen."
        lead = "Ich betreue Netzwerk, Server und Microsoft 365, sichere Ihre Systeme ab und automatisiere wiederkehrende Arbeit – strukturiert, dokumentiert und verständlich erklärt."
        pts = ["Systemadministration, Netzwerk und Firewall", "Microsoft 365, Entra ID und Azure", "Power Automate, Power Apps und SharePoint"]
        facts = [("6+ Jahre", "Erfahrung in IT-Betrieb und IT-Sicherheit"), ("12", "Zertifizierungen, u. a. ISO 27001 und AZ-500"), ("DE · EN · FA", "Arbeitssprachen"), ("Remote", "und vor Ort im Raum Bremen")]
        sv_h, sv_p = "Leistungen", "Vier Bereiche, die aufeinander aufbauen: ein stabiles Netzwerk, ein sicherer Microsoft-365-Tenant, automatisierte Abläufe und eine Dokumentation, die trägt."
        so_h, so_p = "Lösungen aus der Praxis", "Ausgewählte Lösungen, die ich umgesetzt habe – beschrieben als Ausgangslage, Vorgehen und Nutzen, jeweils mit Diagramm in Standardnotation."
        ap_h, ap_p = "Strukturiertes Vorgehen", "Vom ersten Gespräch bis zum Betrieb in fünf klaren Phasen. Sie entscheiden nach jeder Phase, ob es weitergeht."
        why_h = "Warum mit mir arbeiten"
        why = [("shield", "Sicherheit zuerst", "Erfahrung aus einer sicherheitskritischen Umgebung im Finanzsektor und Auditor-Wissen nach ISO/IEC 27001."),
               ("doc", "Saubere Dokumentation", "Jede Lösung wird mit Diagrammen und Anleitungen übergeben – Ihr Team kann sie selbst pflegen."),
               ("check", "Ehrliche Einschätzung", "Ich sage Ihnen auch, wenn sich etwas nicht lohnt, und baue auf vorhandenen Lizenzen auf.")]
    else:
        h1 = "Reliable IT and automated processes for small and mid-sized businesses."
        lead = "I look after network, servers and Microsoft 365, secure your systems and automate recurring work – structured, documented and clearly explained."
        pts = ["System administration, network and firewall", "Microsoft 365, Entra ID and Azure", "Power Automate, Power Apps and SharePoint"]
        facts = [("6+ years", "in IT operations and IT security"), ("12", "certifications incl. ISO 27001 and AZ-500"), ("DE · EN · FA", "working languages"), ("Remote", "and on site around Bremen")]
        sv_h, sv_p = "Services", "Four areas that build on each other: a stable network, a secure Microsoft 365 tenant, automated processes and documentation that holds up."
        so_h, so_p = "Solutions from practice", "Selected solutions I have delivered – described as situation, approach and benefit, each with a diagram in standard notation."
        ap_h, ap_p = "A structured approach", "From the first call to operations in five clear phases. You decide after every phase whether to continue."
        why_h = "Why work with me"
        why = [("shield", "Security first", "Experience from a security-critical environment in the financial sector and ISO/IEC 27001 auditor know-how."),
               ("doc", "Clean documentation", "Every solution is handed over with diagrams and guides – your team can maintain it."),
               ("check", "Honest assessment", "I’ll tell you when something isn’t worth it, and build on the licences you already have.")]
    p = "".join(f"<li>{e(x)}</li>" for x in pts)
    f = "".join(f'<div class="fact"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in facts)
    sv = "".join(svc_card(me, k, lang) for k in SERVICES)
    so = "".join(sol_card(me, s, lang) for s in FEATURED)
    wy = "".join(f'<div class="why"><div class="icon">{ICO[i]}</div><h3>{e(t)}</h3><p>{e(x)}</p></div>' for i, t, x in why)
    body = f'''<section class="hero"><div class="wrap hero-grid">
  <div><p class="eyebrow">Hashmat Bahadari</p><h1>{e(h1)}</h1><p class="lead">{e(lead)}</p>
  <ul class="checks">{p}</ul>
  <div class="btn-row"><a class="btn btn-primary" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a>
  <a class="btn btn-ghost" href="{href(me, path_of("services", lang))}">{e(sv_h)}</a></div></div>
  {figure(DG.overview(lang), lang=lang, compact=True)}
</div><div class="wrap"><div class="facts">{f}</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head"><h2>{e(sv_h)}</h2><p>{e(sv_p)}</p></div><div class="grid-2">{sv}</div></div></section>
<section class="section alt"><div class="wrap"><div class="sec-head"><h2>{e(so_h)}</h2><p>{e(so_p)}</p></div><div class="grid-3">{so}</div>
<div class="btn-row"><a class="btn btn-ghost" href="{href(me, path_of("solutions", lang))}">{e(u["all_solutions"])}</a></div></div></section>
<section class="section"><div class="wrap"><div class="sec-head"><h2>{e(ap_h)}</h2><p>{e(ap_p)}</p></div>{figure(DG.approach(lang), lang=lang)}</div></section>
<section class="section alt"><div class="wrap"><h2>{e(why_h)}</h2><div class="grid-3 whys">{wy}</div></div></section>
{cta(lang)}'''
    write(key, lang, h1, lead, body)

def services_page(lang):
    key = "services"; me = path_of(key, lang)
    if lang == "de":
        h1, lead = "Leistungen", "IT-Betrieb, Microsoft Cloud, Automatisierung und Dokumentation aus einer Hand – für Unternehmen ohne eigene IT-Abteilung oder mit einer, die Entlastung braucht."
        cap = "Vier Leistungsbereiche auf einem gemeinsamen Fundament aus Sicherheit, Dokumentation und Betreuung."
        faq_h = "Häufige Fragen"
        faq = [("Arbeiten Sie remote oder vor Ort?", "Beides. Microsoft 365 und Automatisierung erledige ich meist remote; Netzwerk, Hardware und Schulungen auch vor Ort im Raum Bremen."),
               ("Wie wird abgerechnet?", "Nach Aufwand oder als Festpreis für klar umrissene Vorhaben. Den Rahmen halten wir nach dem Erstgespräch schriftlich fest."),
               ("Brauchen wir neue Lizenzen?", "Oft nicht. Ich baue zuerst auf dem auf, was vorhanden ist, und empfehle Erweiterungen nur, wenn sie wirklich nötig sind."),
               ("Wie gehen Sie mit unseren Daten um?", "Mit minimalen Rechten, dokumentierten Zugriffen und auf Wunsch einer schriftlichen Vertraulichkeitsvereinbarung."),
               ("Können Sie bestehende Lösungen übernehmen?", "Ja. Ich analysiere vorhandene Systeme, Flows und Einstellungen, dokumentiere sie und entwickle sie weiter.")]
    else:
        h1, lead = "Services", "IT operations, Microsoft cloud, automation and documentation from one person – for businesses without an IT department, or with one that needs support."
        cap = "Four service areas on a shared foundation of security, documentation and support."
        faq_h = "Frequently asked questions"
        faq = [("Do you work remotely or on site?", "Both. Microsoft 365 and automation mostly remotely; network, hardware and training also on site around Bremen."),
               ("How is work billed?", "By time spent or as a fixed price for clearly scoped projects. We agree the framework in writing after the first call."),
               ("Do we need new licences?", "Often not. I build on what you have and only recommend upgrades when they are really needed."),
               ("How do you handle our data?", "With least privilege, documented access and, if you wish, a written confidentiality agreement."),
               ("Can you take over existing solutions?", "Yes. I analyse existing systems, flows and settings, document them and develop them further.")]
    cards = "".join(svc_card(me, k, lang) for k in SERVICES)
    fq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap">{figure(DG.service_model(lang), cap, lang=lang)}</div></section>
<section class="section alt"><div class="wrap grid-2">{cards}</div></section>
<section class="section"><div class="wrap narrow"><h2>{e(faq_h)}</h2>{fq}</div></section>
{cta(lang)}'''
    write(key, lang, h1, lead, body)

def service_detail(k, lang):
    s = SERVICES[k]; t = s[lang]; me = path_of(k, lang); u = UI[lang]
    items = "".join(f"<li>{e(i)}</li>" for i in t["items"])
    outs = "".join(f"<li>{e(i)}</li>" for i in t["outcomes"])
    tools = "".join(f"<li>{e(x)}</li>" for x in s["tools"])
    certs = "".join(f"<li>{e(x)}</li>" for x in s["certs"])
    rel = "".join(sol_card(me, x, lang) for x in s["solutions"][:3])
    dg = getattr(DG, s["diagram"])(lang)
    body = page_head(k, lang, t["h1"], t["short"], [("services", u["nav"][0][1])], t["title"]) + f'''
<section class="section"><div class="wrap split">
  <div class="prose"><p class="lead ink">{e(t["intro"])}</p><h2>{e(u["what"])}</h2><ul class="checks">{items}</ul></div>
  <aside class="aside"><h3>{e(u["outcome"])}</h3><ul class="checks sm">{outs}</ul>
  <h3>{e(u["tools"])}</h3><ul class="tags">{tools}</ul><h3>{e(u["certs_rel"])}</h3><ul class="tags">{certs}</ul>
  <a class="btn btn-primary btn-block" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a></aside>
</div></section>
<section class="section alt"><div class="wrap">{figure(dg, t["caption"], lang=lang)}</div></section>
<section class="section"><div class="wrap"><h2>{e(u["related"])}</h2><div class="grid-3 mt">{rel}</div></div></section>
{cta(lang)}'''
    write(k, lang, t["title"], t["short"], body)

def solutions_page(lang):
    key = "solutions"; me = path_of(key, lang)
    if lang == "de":
        h1 = "Lösungen"
        lead = "Lösungen, die ich in der Praxis umgesetzt habe – neutral beschrieben, ohne Kundendaten, jeweils mit Diagramm in Standardnotation."
        cap = "Welche Technologien in welcher Lösung zum Einsatz kommen."
    else:
        h1 = "Solutions"
        lead = "Solutions I have delivered in practice – described neutrally, without client data, each with a diagram in standard notation."
        cap = "Which technologies are used in which solution."
    rows = [(s[lang]["title"], s["flags"]) for s in SOLUTIONS]
    cards = "".join(sol_card(me, s["id"], lang) for s in SOLUTIONS)
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap">{figure(DG.matrix(lang, rows), cap, lang=lang)}</div></section>
<section class="section alt"><div class="wrap grid-3">{cards}</div></section>
{cta(lang)}'''
    write(key, lang, h1, lead, body)

def solution_detail(i, lang):
    s = SOLUTIONS[i]; t = s[lang]; key = "s:" + s["id"]; me = path_of(key, lang); u = UI[lang]
    steps = "".join(f"<li><strong>{e(a)}</strong>{e(b)}</li>" for a, b in t["steps"])
    ben = "".join(f"<li>{e(x)}</li>" for x in t["benefit"])
    tags = "".join(f"<li>{e(x)}</li>" for x in s["stack"])
    prev, nxt = SOLUTIONS[i - 1], SOLUTIONS[(i + 1) % len(SOLUTIONS)]
    dg = getattr(DG, s["diagram"])(lang)
    body = page_head(key, lang, t["title"], t["summary"], [("solutions", u["nav"][1][1])], t["cat"]) + f'''
<section class="section pb0"><div class="wrap">{figure(dg, lang=lang)}</div></section>
<section class="section"><div class="wrap split">
<article class="prose">
  <h2>{e(u["situation"])}</h2><p>{e(t["situation"])}</p>
  <h2>{e(u["solution"])}</h2><ol class="steps">{steps}</ol>
  <div class="benefit"><h2>{e(u["benefit"])}</h2><ul class="checks">{ben}</ul></div>
  <h2>{e(u["tech"])}</h2><p>{e(t["tech"])}</p>
  <nav class="pager"><a href="{href(me, path_of("s:" + prev["id"], lang))}"><span>{e(u["prev"])}</span>{e(prev[lang]["title"])}</a>
  <a class="r" href="{href(me, path_of("s:" + nxt["id"], lang))}"><span>{e(u["next"])}</span>{e(nxt[lang]["title"])}</a></nav>
</article>
<aside class="aside"><h3>{e(u["facts"])}</h3><dl><dt>{e(u["category"])}</dt><dd>{e(t["cat"])}</dd><dt>{e(u["stack"])}</dt><dd><ul class="tags">{tags}</ul></dd></dl>
<a class="btn btn-primary btn-block" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a></aside>
</div></section>
{cta(lang)}'''
    write(key, lang, t["title"], t["summary"], body)

def approach_page(lang):
    key = "approach"
    if lang == "de":
        h1, lead = "Vorgehen", "Klare Phasen, sichtbare Ergebnisse und Entscheidungen bei Ihnen. So bleibt jedes Vorhaben überschaubar."
        ph = [("Analyse", "Gemeinsame Aufnahme des Ist-Zustands: Systeme, Abläufe, Schwachstellen und Ziele. Ergebnis: eine kurze schriftliche Bestandsaufnahme."),
              ("Konzept", "Lösungsskizze mit Diagramm, Aufwandsschätzung und Alternativen. Ergebnis: ein Angebot, über das Sie entscheiden."),
              ("Pilot", "Umsetzung im kleinen Rahmen mit echten Daten und wenigen Nutzern. Ergebnis: eine getestete Lösung und Feedback."),
              ("Rollout", "Einführung für alle Beteiligten mit kurzer Einweisung. Ergebnis: Lösung im produktiven Einsatz."),
              ("Betrieb", "Dokumentation, Übergabe und auf Wunsch laufende Betreuung. Ergebnis: eine Lösung, die Ihr Team versteht.")]
        pr_h = "Grundsätze"
        pr = ["Sicherheit und Datenschutz sind von Anfang an Teil der Lösung.", "Ich baue auf vorhandenen Lizenzen und Systemen auf.", "Jede Lösung wird mit Diagrammen und Anleitungen dokumentiert.", "Prozessmodelle in BPMN, Architekturen in Standardnotation."]
        cap = "Fünf Phasen mit klaren Ergebnissen. Nach jeder Phase entscheiden Sie über den nächsten Schritt."
    else:
        h1, lead = "Approach", "Clear phases, visible results and decisions that stay with you. That keeps every project manageable."
        ph = [("Analysis", "Joint review of the current state: systems, processes, weak points and goals. Result: a short written assessment."),
              ("Design", "Solution outline with diagram, effort estimate and alternatives. Result: a proposal for you to decide on."),
              ("Pilot", "Delivery on a small scale with real data and a few users. Result: a tested solution and feedback."),
              ("Rollout", "Introduction for everyone involved with a short training. Result: the solution in production."),
              ("Operate", "Documentation, handover and ongoing support if you wish. Result: a solution your team understands.")]
        pr_h = "Principles"
        pr = ["Security and data protection are part of the solution from day one.", "I build on existing licences and systems.", "Every solution is documented with diagrams and guides.", "Process models in BPMN, architectures in standard notation."]
        cap = "Five phases with clear results. After each phase you decide on the next step."
    st = "".join(f"<li><strong>{e(a)}</strong>{e(b)}</li>" for a, b in ph)
    p = "".join(f"<li>{e(x)}</li>" for x in pr)
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap">{figure(DG.approach(lang), cap, lang=lang)}</div></section>
<section class="section alt"><div class="wrap grid-2 gap-l"><div><ol class="steps">{st}</ol></div><div class="panel"><h2>{e(pr_h)}</h2><ul class="checks">{p}</ul></div></div></section>
{cta(lang)}'''
    write(key, lang, h1, lead, body)

def about_page(lang):
    key = "about"; me = path_of(key, lang)
    if lang == "de":
        h1, lead = "Über mich", "Ich bin Hashmat Bahadari, IT-Systemadministrator und Spezialist für digitale Automatisierung in Bremen."
        paras = ["Meine Laufbahn begann in der IT-Sicherheit einer nationalen Zentralbank. In dieser großen, auf viele Standorte verteilten Umgebung habe ich gelernt, sorgfältig zu dokumentieren, jede Änderung zu begründen und Risiken früh zu erkennen.",
                 "Heute verbinde ich Systemadministration mit Digitalisierung: Ich betreue Netzwerke, Server und Microsoft 365, baue Intranets und automatisiere Abläufe mit der Power Platform – für Unternehmen, die keine eigene IT-Abteilung haben oder ihre bestehende entlasten wollen.",
                 "Mein Anspruch: Lösungen, die sicher sind, im Alltag funktionieren und auch ohne mich verstanden werden. Deshalb gehört zu jedem Projekt eine Dokumentation mit Diagrammen und Anleitungen."]
        facts = [("Ausbildung", "B.Sc. Informatik (ZAB-anerkannt)"), ("Erfahrung", "6+ Jahre IT-Betrieb und IT-Sicherheit"), ("Schwerpunkte", "Netzwerk, Microsoft 365, Azure, Power Platform"), ("Sprachen", "Deutsch, Englisch, Persisch"), ("Standort", "Bremen, remote und vor Ort"), ("Web", C["website"])]
        fh = "Auf einen Blick"; cap = "Kompetenzen und Schwerpunkte."
    else:
        h1, lead = "About", "I’m Hashmat Bahadari, an IT systems administrator and digital automation specialist in Bremen, Germany."
        paras = ["My career began in IT security at a national central bank. In that large, multi-site environment I learned to document carefully, justify every change and spot risks early.",
                 "Today I combine system administration with digitalisation: I look after networks, servers and Microsoft 365, build intranets and automate processes with the Power Platform – for businesses without their own IT department, or that want to take load off the one they have.",
                 "My standard: solutions that are secure, work day to day and can be understood without me. That’s why every project includes documentation with diagrams and guides."]
        facts = [("Education", "B.Sc. Computer Science (ZAB-recognised)"), ("Experience", "6+ years in IT operations and security"), ("Focus", "Network, Microsoft 365, Azure, Power Platform"), ("Languages", "German, English, Persian"), ("Location", "Bremen, remote and on site"), ("Web", C["website"])]
        fh = "At a glance"; cap = "Competences and focus areas."
    ph = "".join(f"<p>{e(x)}</p>" for x in paras)
    fl = "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in facts)
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap about">
  <div><div class="portrait" aria-hidden="true"><span>HB</span><!-- replace with <img src="../assets/img/portrait.jpg" alt="Hashmat Bahadari"> --></div>
  <aside class="aside st"><h3>{e(fh)}</h3><dl>{fl}</dl></aside></div>
  <div class="prose">{ph}<div class="btn-row"><a class="btn btn-primary" href="{C["booking"]}" target="_blank" rel="noopener">{e(UI[lang]["book"])}</a><a class="btn btn-ghost" href="{href(me, path_of("certs", lang))}">{e(UI[lang]["nav"][4][1])}</a></div></div>
</div></section>
<section class="section alt"><div class="wrap">{figure(DG.competence(lang), cap, lang=lang)}</div></section>
{cta(lang)}'''
    write(key, lang, h1, lead, body)

def certs_page(lang):
    key = "certs"
    if lang == "de":
        h1, lead, cap, note = "Zertifizierungen", "Zertifikate ersetzen keine Erfahrung, zeigen aber ein solides Fundament in Informationssicherheit, Microsoft Azure und Netzwerken.", "Wie die Zertifizierungsbereiche in die Leistungen einfließen.", "Nachweise lege ich auf Anfrage gern vor."
    else:
        h1, lead, cap, note = "Certifications", "Certificates don’t replace experience, but they show a solid foundation in information security, Microsoft Azure and networking.", "How certification areas feed into the services.", "Proof of certification is available on request."
    g = ""
    for grp in CERT_GROUPS:
        it = "".join(f'<div class="card cert"><div class="badge">{e(b)}</div><div><p class="cat">{e(iss)}</p><h3>{e(n)}</h3><p>{e(de if lang == "de" else en)}</p></div></div>' for b, n, iss, de, en in grp["items"])
        g += f'<h2 class="grp">{e(grp[lang])}</h2><div class="grid-2">{it}</div>'
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap">{figure(DG.cert_map(lang), cap, lang=lang)}</div></section>
<section class="section alt"><div class="wrap">{g}<p class="small mt">{e(note)}</p></div></section>
{cta(lang)}'''
    write(key, lang, h1, lead, body)

def contact_page(lang):
    key = "contact"; u = UI[lang]
    if lang == "de":
        h1, lead = "Kontakt", "Buchen Sie direkt einen Termin oder schreiben Sie mir. Ich antworte in der Regel innerhalb eines Werktags."
        bh, bp = "Erstgespräch buchen", "30 Minuten, kostenlos, per Microsoft Teams. Sie schildern die Lage, ich stelle Fragen und gebe eine erste Einschätzung."
        lab = ("E-Mail", "Website", "Standort", "Bremen, remote in ganz Deutschland")
        fh = "Anfrage schreiben"
        f = dict(name="Name", company="Unternehmen (optional)", email="E-Mail-Adresse", topic="Thema", msg="Ihr Anliegen", send="Anfrage per E-Mail senden",
                 topics=["Systemadministration / Netzwerk", "Microsoft 365 / Azure", "Automatisierung", "Intranet / Dokumentation", "Sonstiges"],
                 hint="Beim Absenden öffnet sich Ihr E-Mail-Programm mit der vorbereiteten Nachricht. Auf dieser Website werden keine Daten gespeichert.")
        cap = "So läuft eine Anfrage ab."
    else:
        h1, lead = "Contact", "Book a slot directly or send me a message. I usually reply within one business day."
        bh, bp = "Book an intro call", "30 minutes, free of charge, via Microsoft Teams. You describe the situation, I ask questions and give a first assessment."
        lab = ("Email", "Website", "Location", "Bremen, remote across Germany")
        fh = "Send an enquiry"
        f = dict(name="Name", company="Company (optional)", email="Email address", topic="Topic", msg="Your request", send="Send enquiry by email",
                 topics=["System administration / network", "Microsoft 365 / Azure", "Automation", "Intranet / documentation", "Other"],
                 hint="Submitting opens your email app with the message prepared. No data is stored on this website.")
        cap = "How an enquiry works."
    opts = "".join(f"<option>{e(t)}</option>" for t in f["topics"])
    body = page_head(key, lang, h1, lead) + f'''
<section class="section"><div class="wrap grid-2 gap-l">
<div>
  <div class="card book"><div class="icon">{ICO["clock"]}</div><h2>{e(bh)}</h2><p>{e(bp)}</p><a class="btn btn-primary" href="{C["booking"]}" target="_blank" rel="noopener">{e(u["book"])}</a></div>
  <ul class="contact-list">
    <li><div class="icon">{ICO["mail"]}</div><div><span>{e(lab[0])}</span><a href="mailto:{C["email"]}">{e(C["email"])}</a></div></li>
    <li><div class="icon">{ICO["globe"]}</div><div><span>{e(lab[1])}</span><a href="{C["base_url"]}">{e(C["website"])}</a></div></li>
    <li><div class="icon">{ICO["building"]}</div><div><span>{e(lab[2])}</span><b>{e(lab[3])}</b></div></li>
  </ul>
</div>
<form class="card form" id="enquiry" data-to="{C["email"]}" data-subject="{e("Anfrage über bahadari.de" if lang == "de" else "Enquiry via bahadari.de")}">
  <h2>{e(fh)}</h2>
  <label>{e(f["name"])}<input name="name" required autocomplete="name"></label>
  <label>{e(f["company"])}<input name="company" autocomplete="organization"></label>
  <label>{e(f["email"])}<input name="email" type="email" required autocomplete="email"></label>
  <label>{e(f["topic"])}<select name="topic">{opts}</select></label>
  <label>{e(f["msg"])}<textarea name="message" rows="5" required></textarea></label>
  <button class="btn btn-primary" type="submit">{e(f["send"])}</button><p class="small">{e(f["hint"])}</p>
</form>
</div></section>
<section class="section alt"><div class="wrap">{figure(DG.contact_flow(lang), cap, lang=lang)}</div></section>'''
    write(key, lang, h1, lead, body)

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "legal.py"), encoding="utf-8").read())

def not_found():
    body = '''<section class="page-head"><div class="wrap"><h1>Seite nicht gefunden</h1>
<p class="lead">Die Adresse existiert nicht oder wurde verschoben. Page not found.</p>
<div class="btn-row"><a class="btn btn-primary" href="/">Zur Startseite</a><a class="btn btn-ghost" href="/en/">English</a></div></div></section>'''
    out = layout("home", "de", "404", "Seite nicht gefunden", body)
    out = re.sub(r'(href|src)="(?!https?:|mailto:|/|#)(?:\./)?([^"]*)"', lambda m: f'{m.group(1)}="/{m.group(2)}"', out)
    out = re.sub(r"<title>.*?</title>", f"<title>404 | {C['name']}</title>", out)
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(out)

def extras():
    keys = [k for k in ROUTES] + ["s:" + s["id"] for s in SOLUTIONS]
    today = datetime.date.today().isoformat(); urls = []
    for k in keys:
        for l in ("de", "en"):
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{C["base_url"] + path_of(k, x)}"/>' for x in ("de", "en"))
            urls.append(f'<url><loc>{C["base_url"] + path_of(k, l)}</loc><lastmod>{today}</lastmod>{alts}</url>')
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {C['base_url']}sitemap.xml\n")
    open(os.path.join(OUT, "CNAME"), "w").write(C["domain"] + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    return len(keys) * 2

if __name__ == "__main__":
    for lang in ("de", "en"):
        home(lang); services_page(lang); solutions_page(lang); approach_page(lang)
        about_page(lang); certs_page(lang); contact_page(lang); imprint_page(lang); privacy_page(lang)
        for k in SERVICES: service_detail(k, lang)
        for i in range(len(SOLUTIONS)): solution_detail(i, lang)
    not_found()
    print(f"Built {extras()} pages + 404 into {OUT}")
