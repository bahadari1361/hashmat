# -*- coding: utf-8 -*-
"""SVG diagram engine + every diagram on the site (bilingual)."""
import html
e = html.escape

TILE = {  # connector-style tiles (generic colours, no logos)
    "sp": ("SP", "#038387"), "ol": ("OL", "#0F6CBD"), "tm": ("T", "#5B5FC7"), "xl": ("X", "#107C41"),
    "tr": ("TR", "#0079BF"), "ctl": ("{ }", "#5C6B7A"), "fm": ("F", "#077568"), "pa": ("PA", "#0066FF"),
    "http": ("API", "#6B3FA0"), "sch": ("@clock", "#0A6E8A"), "id": ("ID", "#0A2540"), "fw": ("FW", "#0A2540"),
    "pq": ("PQ", "#1F6E43"), "app": ("App", "#742774"), "srv": ("SRV", "#2E4A66"), "net": ("SW", "#2E4A66"),
    "usr": ("@user", "#1479C9"), "cld": ("@cloud", "#1479C9"), "erp": ("ERP", "#5C6B7A"), "def": ("D", "#1F3B8A"),
    "ex": ("EX", "#0F6CBD"), "bk": ("BK", "#2E4A66"), "wifi": ("AP", "#2E4A66"), "doc": ("@doc", "#1479C9"),
}

ICON = {
    "user": '<circle cx="12" cy="8.5" r="3.6"/><path d="M5 19.5c1.2-3.6 4-5.2 7-5.2s5.8 1.6 7 5.2"/>',
    "cloud": '<path d="M7.5 18h9.2a3.8 3.8 0 0 0 .5-7.56A5.6 5.6 0 0 0 6.6 9.3 4.2 4.2 0 0 0 7.5 18Z"/>',
    "doc": '<path d="M7 3.5h7l4 4V20.5H7z"/><path d="M14 3.5v4h4M9.5 12h6M9.5 15.5h6"/>',
    "clock": '<circle cx="12" cy="12" r="7.5"/><path d="M12 8v4.3l2.8 1.8"/>',
}

def tw(text, size=13):  # rough text width
    return len(text) * size * 0.55

class D:
    n = 0
    def __init__(self, w, h, title=""):
        D.n += 1
        self.uid = f"dg{D.n}"
        self.w, self.h, self.title = w, h, title
        self.nodes, self.bg, self.fg, self.lines = {}, [], [], []

    # ---- primitives
    def group(self, gid, x, y, w, h, label, kind=""):
        self.nodes[gid] = (x, y, w, h)
        self.bg.append(f'<g class="dg-group {kind}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>'
                       f'<text class="dg-glabel" x="{x+14}" y="{y+20}">{e(label)}</text></g>')

    def node(self, nid, x, y, w, h, title, sub=None, kind="", tile=None, center=False):
        self.nodes[nid] = (x, y, w, h)
        rx = h / 2 if kind == "pill" else 10
        out = [f'<g class="dg-node {kind}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>']
        tx = x + 14
        if tile:
            code, col = TILE[tile]
            ts = 30 if h >= 44 else 24
            out.append(f'<rect class="dg-tile" x="{x+10}" y="{y+(h-ts)/2}" width="{ts}" height="{ts}" rx="7" fill="{col}"/>')
            if code.startswith("@"):
                sc = ts / 24 * 0.78; ox = x + 10 + ts * 0.11; oy = y + (h - ts) / 2 + ts * 0.11
                out.append(f'<g class="dg-ico" transform="translate({ox} {oy}) scale({sc})">{ICON[code[1:]]}</g>')
            else:
                out.append(f'<text class="dg-tiletxt" x="{x+10+ts/2}" y="{y+h/2+4}" text-anchor="middle">{e(code)}</text>')
            tx = x + 10 + ts + 10
        tl = title.split("\n")
        sl = sub.split("\n") if sub else []
        lh_t, lh_s = 15, 13.5
        total = len(tl) * lh_t + len(sl) * lh_s
        cy = y + (h - total) / 2 + 11
        anchor = ' text-anchor="middle"' if center else ""
        ax = x + w / 2 if center else tx
        avail = (w - 20) if center else (x + w - tx - 10)
        fs = 13
        longest = max(len(t) for t in tl)
        if longest * 13 * 0.6 > avail:
            fs = max(10.5, avail / (longest * 0.6))
        fst = f' style="font-size:{fs:.1f}px"' if fs < 13 else ""
        for i, t in enumerate(tl):
            out.append(f'<text class="dg-t" x="{ax}" y="{cy + i*lh_t}"{anchor}{fst}>{e(t)}</text>')
        cy += len(tl) * lh_t
        for i, s in enumerate(sl):
            out.append(f'<text class="dg-s" x="{ax}" y="{cy + i*lh_s}"{anchor}>{e(s)}</text>')
        out.append("</g>")
        self.fg.append("".join(out))

    def raw(self, svg, front=True):
        (self.fg if front else self.bg).append(svg)

    def _anchor(self, nid, side):
        x, y, w, h = self.nodes[nid]
        return {"l": (x, y + h/2), "r": (x + w, y + h/2), "t": (x + w/2, y), "b": (x + w/2, y + h)}[side]

    def edge(self, a, b, label=None, dashed=False, sa=None, sb=None, curve=False, arrow=True, ox=0, oy=0):
        ax, ay, aw, ah = self.nodes[a]; bx, by, bw, bh = self.nodes[b]
        dx = (bx + bw/2) - (ax + aw/2); dy = (by + bh/2) - (ay + ah/2)
        if sa is None:
            if abs(dx) > abs(dy) or (ay < by + bh and by < ay + ah):
                sa, sb = ("r", "l") if dx > 0 else ("l", "r")
            else:
                sa, sb = ("b", "t") if dy > 0 else ("t", "b")
        sx, sy = self._anchor(a, sa); ex, ey = self._anchor(b, sb)
        sx += ox; ex += ox if sa in "tb" and sb in "tb" else 0
        sy += oy; ey += oy if sa in "lr" and sb in "lr" else 0
        if curve:
            if sa in "lr":
                c = (ex - sx) * 0.5
                d = f"M{sx} {sy} C{sx+c} {sy} {ex-c} {ey} {ex} {ey}"
            else:
                c = (ey - sy) * 0.5
                d = f"M{sx} {sy} C{sx} {sy+c} {ex} {ey-c} {ex} {ey}"
            mx, my = (sx + ex) / 2, (sy + ey) / 2
        elif sa in "lr" and sb in "lr":
            mx = (sx + ex) / 2; my = (sy + ey) / 2
            d = f"M{sx} {sy} H{mx} V{ey} H{ex}"
        elif sa in "tb" and sb in "tb":
            my = (sy + ey) / 2; mx = (sx + ex) / 2
            d = f"M{sx} {sy} V{my} H{ex} V{ey}"
        elif sa in "lr":
            d = f"M{sx} {sy} H{ex} V{ey}"; mx, my = ex, sy
        else:
            d = f"M{sx} {sy} V{ey} H{ex}"; mx, my = sx, ey
        cls = "dg-edge" + (" dashed" if dashed else "")
        mk = f' marker-end="url(#{self.uid}a)"' if arrow else ""
        self.lines.append(f'<path class="{cls}" d="{d}"{mk}/>')
        if label:
            lw = tw(label, 11) + 14
            self.fg.append(f'<g class="dg-elabel"><rect x="{mx-lw/2}" y="{my-10}" width="{lw}" height="20" rx="10"/>'
                           f'<text x="{mx}" y="{my+4}" text-anchor="middle">{e(label)}</text></g>')

    def poly(self, pts, dashed=False, arrow=True):
        d = "M" + " L".join(f"{x} {y}" for x, y in pts)
        mk = f' marker-end="url(#{self.uid}a)"' if arrow else ""
        self.lines.append(f'<path class="dg-edge{" dashed" if dashed else ""}" d="{d}"{mk}/>')

    def svg(self, cls="dg"):
        defs = (f'<defs><marker id="{self.uid}a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0 0 L10 5 L0 10 z" class="dg-arrow"/></marker>'
                f'<pattern id="{self.uid}p" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" class="dg-dot"/></pattern></defs>')
        return (f'<svg class="{cls}" viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{e(self.title)}">'
                f'{defs}<rect width="{self.w}" height="{self.h}" fill="url(#{self.uid}p)"/>'
                + "".join(self.bg) + "".join(self.lines) + "".join(self.fg) + "</svg>")


# ------------------------------------------------------------------ Power Automate canvas
def pa_flow(lang, name, steps, status=None, width=600):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(width, 100, name)
    CW, CH, GAP = 340, 56, 34
    y0 = 78

    def card(x, y, w, s):
        tile, title, sub = s[1], s[2], s[3] if len(s) > 3 else None
        d.node(f"n{len(d.nodes)}", x, y, w, CH, title, sub, kind="pa", tile=tile)
        return (x, y, w, CH)

    def arrow(x, y1, y2):
        d.poly([(x, y1), (x, y2 - 2)])

    def lay(steps, x, w, y):
        prev = None
        for s in steps:
            cw = min(CW, w)
            cx = x + (w - cw) / 2
            if prev:
                arrow(x + w/2, prev, y)
            if s[0] == "a":
                card(cx, y, cw, s); prev = y + CH; y += CH + GAP
            elif s[0] == "loop":
                card(cx, y, cw, ("a", "ctl", s[1], s[2]))
                top = y - 10
                y2 = y + CH + GAP
                arrow(x + w/2, y + CH, y2)
                yend = lay(s[3], x + 18, w - 36, y2)
                d.raw(f'<rect class="dg-scope" x="{x}" y="{top}" width="{w}" height="{yend - top - GAP + 14}" rx="12"/>', front=False)
                prev = yend - GAP + 14; y = yend + 14
            elif s[0] == "cond":
                card(cx, y, cw, ("a", "ctl", s[1], s[2]))
                cy = y + CH; y += CH + 26
                half = (w - 16) / 2
                cols = [(x, s[3], L("Wenn ja", "If yes"), "yes"), (x + half + 16, s[4], L("Wenn nein", "If no"), "no")]
                ends = []
                for bx, items, lab, k in cols:
                    mx = bx + half / 2
                    d.poly([(x + w/2, cy), (x + w/2, cy + 12), (mx, cy + 12), (mx, y + 2)], arrow=False)
                    d.raw(f'<g class="dg-branch {k}"><rect x="{bx}" y="{y}" width="{half}" height="26" rx="8"/>'
                          f'<text x="{bx+12}" y="{y+17}">{e(lab)}</text></g>')
                    ends.append(lay(items, bx, half, y + 26 + 18))
                y = max(ends); prev = None
        return y

    end = lay(steps, (width - 520) / 2 if width > 540 else 10, min(520, width - 20), y0)
    d.h = end + 6
    # header bar
    st = status or L("Ein", "On")
    d.raw(f'<g class="dg-pahead"><rect x="0" y="0" width="{width}" height="48"/>'
          f'<rect class="dg-tile" x="16" y="11" width="26" height="26" rx="7" fill="#0066FF"/><text class="dg-tiletxt" x="29" y="28" text-anchor="middle">PA</text>'
          f'<text class="dg-t" x="52" y="22">{e(name)}</text><text class="dg-s" x="52" y="38">Power Automate Cloud-Flow</text>'
          f'<g class="dg-status"><rect x="{width-150}" y="13" width="134" height="22" rx="11"/><circle cx="{width-136}" cy="24" r="4"/>'
          f'<text x="{width-126}" y="28">{e(L("Letzter Lauf: OK", "Last run: OK"))}</text></g></g>')
    return d


# ------------------------------------------------------------------ diagrams
def flow_reminder(lang):
    L = (lambda de, en: de if lang == "de" else en)
    return pa_flow(lang, L("Wartungserinnerung, Stufe 1", "Maintenance reminder, step 1"), [
        ("a", "sch", L("Wiederholung", "Recurrence"), L("Täglich um 06:00 Uhr", "Daily at 06:00")),
        ("a", "sp", L("Elemente abrufen", "Get items"), L("Liste Anlagen, Filter Status = Fällig", "List devices, filter status = due")),
        ("loop", L("Auf alle anwenden", "Apply to each"), L("Für jede fällige Anlage", "For each due device"), [
            ("cond", L("Bedingung", "Condition"), L("E-Mail-Adresse vorhanden?", "Email address present?"),
             [("a", "ol", L("E-Mail senden (V2)", "Send an email (V2)"), L("HTML-Vorlage, Anrede", "HTML template, salutation")),
              ("a", "sp", L("Element aktualisieren", "Update item"), L("Status = Stufe 1", "Status = step 1"))],
             [("a", "tm", L("Nachricht posten", "Post message"), L("Büro: Adresse fehlt", "Office: address missing"))]),
        ]),
    ])

def flow_guard(lang):
    L = (lambda de, en: de if lang == "de" else en)
    return pa_flow(lang, L("Phasenwechsel prüfen", "Check phase change"), [
        ("a", "tr", L("Wenn eine Karte verschoben wird", "When a card is moved"), L("Board Wärmepumpe", "Heat-pump board")),
        ("a", "http", "HTTP GET", L("Checklisten der Vorphase abrufen", "Get checklists of previous phase")),
        ("a", "ctl", L("Verfassen", "Compose"), L("Offene Punkte zählen", "Count open items")),
        ("cond", L("Bedingung", "Condition"), L("Alle Punkte erledigt?", "All items complete?"),
         [("a", "http", "HTTP POST", L("Checkliste neue Phase", "Checklist for new phase")),
          ("a", "tr", L("Karte aktualisieren", "Update card"), L("Titel: nächste Aufgabe", "Title: next task"))],
         [("a", "tr", L("Karte verschieben", "Move card"), L("Zurück in Vorphase", "Back to previous phase")),
          ("a", "tr", L("Kommentar hinzufügen", "Add comment"), L("Liste der offenen Punkte", "List of open items"))]),
    ])

def flow_email(lang):
    L = (lambda de, en: de if lang == "de" else en)
    return pa_flow(lang, L("Kunden-E-Mail zuordnen", "File customer email"), [
        ("a", "ol", L("Wenn eine neue E-Mail eintrifft", "When a new email arrives"), L("Postfach Kundenanfragen", "Customer requests mailbox")),
        ("a", "ctl", L("Verfassen", "Compose"), L("Projektnummer aus Betreff lesen", "Read project number from subject")),
        ("cond", L("Bedingung", "Condition"), L("Projektnummer gefunden?", "Project number found?"),
         [("a", "tr", L("Kommentar hinzufügen", "Add comment"), L("E-Mail an Projektkarte", "Email to project card")),
          ("a", "sp", L("Element erstellen", "Create item"), L("Verlauf für Power App", "History for Power App"))],
         [("a", "sp", L("Element erstellen", "Create item"), L("Status: zu klären", "Status: to clarify")),
          ("a", "tm", L("Nachricht posten", "Post message"), L("Hinweis an das Büro", "Notify the office"))]),
    ])

def stack(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 372, L("Leistungsarchitektur", "Service architecture"))
    layers = [
        (L("Intranet & Wissensbasis", "Intranet & knowledge base"), L("Was Mitarbeitende täglich sehen", "What staff see every day"), [L("Rollenportale", "Role portals"), L("Anträge", "Requests"), L("Anleitungen", "Procedures"), L("Kontakte", "Contacts")]),
        (L("Automatisierung", "Automation"), L("Abläufe, die von selbst laufen", "Processes that run themselves"), ["Power Automate", "Power Apps", "REST-API", "RPA"]),
        ("Microsoft Cloud", L("Identität, E-Mail, Dateien, Teams", "Identity, email, files, Teams"), ["Entra ID", "Exchange", "SharePoint", "Teams"]),
        (L("Systemadministration", "System administration"), L("Das Fundament im Betrieb", "The foundation in operation"), [L("Netzwerk", "Network"), "Server", "Clients", "Backup"]),
    ]
    y = 20
    for i, (t, s, chips) in enumerate(layers):
        kind = "layer" + (" top" if i == 0 else "")
        d.node(f"l{i}", 20, y, 610, 74, t, s, kind=kind)
        cx = 255
        for c in chips:
            w = tw(c, 12) + 22
            d.raw(f'<g class="dg-chip"><rect x="{cx}" y="{y+24}" width="{w}" height="26" rx="13"/><text x="{cx+w/2}" y="{y+41}" text-anchor="middle">{e(c)}</text></g>')
            cx += w + 8
        y += 86
    d.raw(f'<g class="dg-node primary"><rect x="645" y="20" width="95" height="332" rx="12"/>'
          f'<text class="dg-t" transform="translate(698 186) rotate(-90)" text-anchor="middle">{e(L("IT-Sicherheit in jeder Ebene", "IT security in every layer"))}</text></g>')
    return d

def cloud_identity(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 420, L("Identität und Zugriff in Microsoft 365", "Identity and access in Microsoft 365"))
    d.node("u1", 20, 60, 165, 56, L("Büro-Arbeitsplatz", "Office workstation"), L("Verwaltetes Gerät", "Managed device"), tile="usr")
    d.node("u2", 20, 165, 165, 56, L("Außendienst", "Field staff"), L("Smartphone, Tablet", "Phone, tablet"), tile="usr")
    d.node("u3", 20, 270, 165, 56, L("Externe Partner", "External partners"), L("Gastzugang", "Guest access"), tile="usr", kind="guard")
    d.group("entra", 225, 30, 230, 320, "Microsoft Entra ID", "accent")
    for i, (t, s) in enumerate([(L("Mehrstufige Anmeldung", "Multi-factor sign-in"), "MFA"),
                                (L("Bedingter Zugriff", "Conditional Access"), L("Gerät, Ort, Risiko", "Device, location, risk")),
                                (L("Gruppen & Rollen", "Groups & roles"), L("Minimale Rechte", "Least privilege")),
                                (L("Anmeldeprotokolle", "Sign-in logs"), L("Auffälligkeiten prüfen", "Review anomalies"))]):
        d.node(f"e{i}", 240, 60 + i * 70, 200, 54, t, s, tile="id")
    d.group("m365", 495, 30, 245, 320, "Microsoft 365", "")
    for i, (tile, t, s) in enumerate([("ex", "Exchange Online", L("E-Mail, Kalender", "Email, calendar")),
                                      ("sp", "SharePoint & OneDrive", L("Dateien, Intranet", "Files, intranet")),
                                      ("tm", "Microsoft Teams", L("Chat, Projekträume", "Chat, project spaces")),
                                      ("pa", "Power Platform", L("Flows, Apps", "Flows, apps"))]):
        d.node(f"m{i}", 510, 60 + i * 70, 215, 54, t, s, tile=tile)
    for u in ("u1", "u2"):
        d.edge(u, "entra", sb="l", curve=True)
    d.edge("u3", "entra", sb="l", curve=True, dashed=True)
    d.edge("entra", "m365", L("Zugriffstoken", "Access token"))
    d.node("def", 225, 366, 515, 42, L("Microsoft Defender und Protokollierung über alle Dienste", "Microsoft Defender and logging across all services"), kind="soft", tile="def")
    return d

def network(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 430, L("Netzwerk-Referenzdesign", "Reference network design"))
    d.node("inet", 290, 18, 180, 44, "Internet", kind="pill", tile="cld")
    d.node("m365", 560, 14, 180, 52, "Microsoft 365", L("Cloud-Dienste", "Cloud services"), tile="cld")
    d.node("fw", 280, 104, 200, 58, L("Firewall (Fortinet)", "Firewall (Fortinet)"), L("UTM, VPN-Gateway", "UTM, VPN gateway"), kind="primary", tile="fw")
    d.node("vpn", 20, 104, 215, 58, L("Remote & Außendienst", "Remote & field staff"), L("SSL-VPN mit MFA", "SSL VPN with MFA"), tile="usr")
    d.node("core", 280, 200, 200, 52, "Core-Switch", L("VLAN-Routing, ACLs", "VLAN routing, ACLs"), tile="net")
    d.edge("inet", "fw", sa="b", sb="t")
    d.edge("inet", "m365")
    d.edge("vpn", "fw", "VPN", dashed=True)
    d.edge("fw", "core", sa="b", sb="t")
    vl = [("VLAN 10 · " + L("Büro", "Office"), [(L("Arbeitsplätze", "Workstations"), "usr"), (L("Netzwerkdrucker", "Printers"), "doc")]),
          ("VLAN 20 · Server", [(L("Datei- & ERP-Server", "File & ERP server"), "srv"), (L("Backup + Offsite", "Backup + offsite"), "bk")]),
          ("VLAN 30 · WLAN", [(L("Mitarbeiter-WLAN", "Staff Wi-Fi"), "wifi"), ("Access Points", "wifi")]),
          ("VLAN 40 · " + L("Gäste", "Guests"), [(L("Gast-WLAN", "Guest Wi-Fi"), "wifi"), (L("Nur Internet", "Internet only"), "cld")])]
    for i, (lab, items) in enumerate(vl):
        x = 20 + i * 185
        d.group(f"v{i}", x, 296, 170, 124, lab.replace(" · ", ": "), "accent" if i == 1 else "")
        for j, (t, tile) in enumerate(items):
            d.node(f"v{i}{j}", x + 10, 326 + j * 46, 150, 40, t, tile=tile)
        d.edge("core", f"v{i}", sa="b", sb="t")
    return d

def intranet_tree(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 420, L("Informationsarchitektur des Intranets", "Intranet information architecture"))
    d.node("hub", 250, 18, 260, 60, L("Startseite (Hub)", "Home page (hub)"), L("Begrüßung, Kacheln, Termine", "Welcome, tiles, events"), kind="primary", tile="sp")
    portals = [(L("Techniker-Portal", "Technician portal"), L("Außendienst", "Field service"),
                [L("Kundendienst", "Customer service"), L("Melden & Beantragen", "Report & request"), L("Sicherheit & Vorschriften", "Safety & regulations"), L("Erste Hilfe", "First aid")]),
               (L("Büro-Portal", "Office portal"), L("Innendienst", "Back office"),
                [L("Abläufe", "Procedures"), L("Wochenmeeting (App)", "Weekly meeting (app)"), L("Ansprechpartner (App)", "Contacts (app)"), L("Reklamationen", "Complaints")]),
               (L("Geschäftsführung", "Management"), L("Leitung", "Leadership"),
                [L("Besprechungs-Tracker", "Meeting tracker"), L("Organisation", "Organisation"), L("Freigaben", "Approvals")])]
    for i, (t, s, items) in enumerate(portals):
        x = 20 + i * 250
        d.node(f"p{i}", x, 120, 220, 56, t, s, kind="accent", tile="sp")
        d.edge("hub", f"p{i}", sa="b", sb="t")
        for j, it in enumerate(items):
            yy = 206 + j * 50
            d.node(f"p{i}{j}", x + 26, yy, 194, 38, it, kind="soft")
            d.poly([(x + 12, 176), (x + 12, yy + 19), (x + 24, yy + 19)], arrow=False)
    return d

def intranet_request(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 300, L("Digitaler Antrag mit Freigabe", "Digital request with approval"))
    d.node("a", 20, 110, 150, 60, L("Mitarbeiter/in", "Employee"), L("Formular ausfüllen", "Fills in form"), tile="fm")
    d.node("b", 205, 110, 160, 60, "Power Automate", L("Freigabe starten", "Start approval"), tile="pa", kind="primary")
    d.node("c", 400, 110, 150, 60, L("Vorgesetzte/r", "Manager"), L("Genehmigt in Teams", "Approves in Teams"), tile="tm")
    d.node("ok", 590, 40, 150, 60, L("Bestellung", "Order"), L("Büro + Bestätigung", "Office + confirmation"), kind="accent", tile="ol")
    d.node("no", 590, 180, 150, 60, L("Absage", "Rejection"), L("Mit Begründung", "With reason"), tile="ol")
    d.node("log", 205, 222, 160, 52, L("SharePoint-Liste", "SharePoint list"), L("Verlauf jedes Antrags", "History of each request"), tile="sp", kind="soft")
    d.edge("a", "b"); d.edge("b", "c")
    d.edge("c", "ok", L("genehmigt", "approved"), curve=True)
    d.edge("c", "no", L("abgelehnt", "rejected"), curve=True)
    d.edge("b", "log", L("protokolliert", "logged"), dashed=True, sa="b", sb="t")
    return d

def phases(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 360, L("Phasenmodell Wärmepumpen-Projekt", "Heat-pump project phase model"))
    r1 = [L("Anfrage /\nTermin", "Enquiry /\nappointment"), L("Angebot\nerstellen", "Prepare\nquote"), L("Rückfragen &\nNachfassen", "Questions &\nfollow-up"),
          L("BzA, AR,\nTermine", "Permits,\norders, dates"), L("Ausführung\nvorbereiten", "Prepare\ninstallation")]
    r2 = [L("Ausführung", "Installation"), L("Restarbeiten", "Rework"), L("IBN, Abnahme,\nAbschluss", "Commissioning,\nsign-off"), L("Erledigt", "Done")]
    for i, t in enumerate(r1):
        d.node(f"a{i}", 20 + i * 148, 30, 128, 70, t, L("Phase ", "Phase ") + str(i + 1), kind="accent" if i == 0 else "")
    xs = [612, 464, 316, 168]
    for i, t in enumerate(r2):
        kind = "primary" if i == 3 else ("guard" if i == 1 else "")
        d.node(f"b{i}", xs[i], 150, 128, 70, t, (L("optional", "optional") if i == 1 else L("Phase ", "Phase ") + str(i + 6)) if i < 3 else L("Archiv", "Archive"), kind=kind)
    d.edge("a0", "a1", L("auto", "auto"))
    for i in range(1, 4): d.edge(f"a{i}", f"a{i+1}")
    d.edge("a4", "b0", sa="b", sb="t")
    for i in range(3): d.edge(f"b{i}", f"b{i+1}")
    d.node("h1", 20, 150, 128, 32, L("Zurückgestellt", "On hold"), kind="soft")
    d.node("h2", 20, 188, 128, 32, L("Verloren", "Lost"), kind="soft")
    d.node("chk", 20, 262, 720, 78, L("Prüfung bei jedem manuellen Wechsel", "Check on every manual move"),
           L("Checkliste der Vorphase vollständig? Ja: neue Checkliste und Titel aktualisieren.\nNein: Karte zurück, offene Punkte als Kommentar.",
             "Previous checklist complete? Yes: new checklist and updated title.\nNo: card moves back, open items posted as a comment."), kind="soft", tile="pa")
    return d

def reminder_pipe(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 310, L("Datenfluss Wartungserinnerungen", "Maintenance reminder data flow"))
    d.node("x1", 20, 30, 150, 54, L("Kundendatei A", "Customer file A"), "Excel", tile="xl")
    d.node("x2", 20, 120, 150, 54, L("Kundendatei B", "Customer file B"), "Excel", tile="xl")
    d.node("pq", 205, 75, 160, 54, "Power Query", L("Anfügen, 1 Zeile je Anlage", "Append, 1 row per device"), tile="pq")
    d.node("sp", 400, 75, 165, 54, L("SharePoint-Liste", "SharePoint list"), L("≈ 1.600 Kunden, Status", "≈ 1,600 customers, status"), tile="sp", kind="accent")
    d.node("fl", 600, 75, 140, 54, L("Tägliche Flows", "Daily flows"), L("OData-Filter", "OData filter"), tile="pa", kind="primary")
    d.edge("x1", "pq", curve=True); d.edge("x2", "pq", curve=True); d.edge("pq", "sp"); d.edge("sp", "fl")
    for i in range(3):
        d.node(f"m{i}", 400 + i * 116, 210, 108, 54, L("E-Mail ", "Email ") + str(i + 1), L("Stufe ", "Step ") + str(i + 1), tile="ol")
    d.edge("fl", "m0", sa="b", sb="t")
    d.edge("m0", "m1"); d.edge("m1", "m2")
    d.node("st", 20, 210, 345, 54, L("Status je Anlage", "Status per device"), L("Zeigt, welche Stufe erreicht ist", "Shows which step has been reached"), kind="soft", tile="sp")
    return d

def tracker_mock(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 360, L("Besprechungs-Tracker (Beispieldaten)", "Meeting tracker (sample data)"))
    d.raw('<rect class="dg-app" x="20" y="16" width="720" height="328" rx="14"/>'
          '<path class="dg-appbar" d="M20 30 a14 14 0 0 1 14 -14 H726 a14 14 0 0 1 14 14 V62 H20 Z"/>'
          f'<text class="dg-apptitle" x="40" y="45">{e(L("Wochenmeeting", "Weekly meeting"))}</text>'
          f'<rect x="590" y="27" width="130" height="26" rx="7" class="dg-appbtn"/><text x="655" y="44" text-anchor="middle" class="dg-appbtntxt">+ {e(L("Neue Aufgabe", "New action"))}</text>')
    kpis = [(L("Offen", "Open"), "9", "o"), (L("In Arbeit", "In progress"), "6", "w"), (L("Erledigt", "Done"), "24", "d"), (L("Überfällig", "Overdue"), "2", "l")]
    for i, (t, n, k) in enumerate(kpis):
        x = 40 + i * 172
        d.raw(f'<g class="dg-kpi {k}"><rect x="{x}" y="78" width="160" height="62" rx="10"/><text class="n" x="{x+16}" y="112">{n}</text><text class="l" x="{x+16}" y="130">{e(t)}</text></g>')
    hdr = [L("Aufgabe", "Action"), L("Verantwortlich", "Owner"), L("Fällig", "Due"), "Status"]
    cx = [40, 380, 520, 610]
    d.raw("".join(f'<text class="dg-th" x="{x}" y="168">{e(h)}</text>' for x, h in zip(cx, hdr)))
    rows = [(L("Angebotsvorlage aktualisieren", "Update quote template"), L("Büro", "Office"), "KW 44", L("In Arbeit", "In progress"), "w"),
            (L("Werkzeugprüfung planen", "Plan tool inspection"), L("Werkstatt", "Workshop"), "KW 45", L("Offen", "Open"), "o"),
            (L("Schulung Wärmepumpe", "Heat-pump training"), L("Geschäftsführung", "Management"), "KW 43", L("Erledigt", "Done"), "d"),
            (L("Fahrzeugliste pflegen", "Maintain vehicle list"), L("Büro", "Office"), "KW 42", L("Überfällig", "Overdue"), "l")]
    for i, (a, b, c, s, k) in enumerate(rows):
        y = 180 + i * 38
        d.raw(f'<rect class="dg-row" x="32" y="{y}" width="696" height="32" rx="7"/>'
              f'<text class="dg-td" x="40" y="{y+21}">{e(a)}</text><text class="dg-td" x="380" y="{y+21}">{e(b)}</text><text class="dg-td" x="520" y="{y+21}">{c}</text>'
              f'<g class="dg-badge {k}"><rect x="604" y="{y+6}" width="{tw(s,11)+20}" height="20" rx="10"/><text x="{614}" y="{y+20}">{e(s)}</text></g>')
    return d

def erp_decision(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 320, L("Bewertung der ERP-Anbindung", "ERP integration assessment"))
    d.node("erp", 20, 128, 150, 64, L("ERP-Desktop-Client", "ERP desktop client"), L("keine offene API", "no open API"), tile="erp")
    opts = [(L("Datenexport", "Data export"), L("CSV, Berichte", "CSV, reports")), (L("Datenbankzugriff", "Database access"), L("Herstellerfreigabe nötig", "Needs vendor approval")),
            (L("Oberflächen-RPA", "UI automation (RPA)"), "Power Automate Desktop")]
    for i, (t, s) in enumerate(opts):
        d.node(f"o{i}", 215, 40 + i * 92, 190, 60, t, s, tile="pa" if i == 2 else "doc", kind="accent" if i == 2 else "")
        d.edge("erp", f"o{i}", curve=True)
    d.node("tp", 445, 92, 150, 136, L("Testprotokoll", "Test protocol"),
           L("Stabilität bei Updates\nFehlerbehandlung\nLaufzeit\nPflegeaufwand", "Stability on updates\nError handling\nRun time\nMaintenance effort"), kind="soft")
    for i in range(3): d.edge(f"o{i}", "tp", curve=True, sb="l")
    d.node("dec", 625, 125, 115, 70, L("Entscheidung", "Decision"), L("Vorlage GF", "For management"), kind="primary")
    d.edge("tp", "dec")
    return d

def email_wire(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 400, L("Aufbau der Kampagnen-E-Mail", "Campaign email structure"))
    x, w = 200, 360
    d.raw(f'<rect class="dg-app" x="{x}" y="16" width="{w}" height="368" rx="10"/>'
          f'<rect x="{x}" y="16" width="{w}" height="42" rx="10" class="dg-mailhead"/><rect x="{x}" y="40" width="{w}" height="18" class="dg-mailhead"/>'
          f'<rect x="{x+16}" y="28" width="70" height="18" rx="4" class="dg-logo"/>'
          f'<rect x="{x}" y="58" width="{w}" height="66" class="dg-hero"/><text class="dg-herot" x="{x+20}" y="96">{e(L("Wärmepumpen-Tag", "Heat-pump open day"))}</text>'
          f'<text class="dg-td" x="{x+20}" y="150">{e(L("Sehr geehrte/r", "Dear"))}</text>'
          f'<rect x="{x+20+tw(L("Sehr geehrte/r ","Dear "),12.5)}" y="137" width="128" height="20" rx="5" class="dg-token"/>'
          f'<text class="dg-tokent" x="{x+26+tw(L("Sehr geehrte/r ","Dear "),12.5)}" y="151">{e(L("{Anrede} {Name}", "{Title} {Name}"))}</text>')
    for i in range(3):
        yy = 180 + i * 30
        d.raw(f'<rect x="{x+20}" y="{yy}" width="14" height="14" rx="4" class="dg-check"/><rect x="{x+44}" y="{yy+3}" width="{220 - i*30}" height="8" rx="4" class="dg-line"/>')
    d.raw(f'<rect x="{x+20}" y="282" width="150" height="34" rx="8" class="dg-cta"/><text x="{x+95}" y="304" text-anchor="middle" class="dg-ctat">{e(L("Jetzt anmelden", "Register now"))}</text>'
          f'<rect x="{x}" y="336" width="{w}" height="48" class="dg-foot"/><text class="dg-s" x="{x+20}" y="364">{e(L("Impressum  |  Datenschutz", "Legal notice  |  Privacy"))}</text>')
    notes = [(20, 60, L("Tabellenlayout", "Table layout"), L("Sicher in Outlook", "Safe in Outlook"), 78),
             (20, 128, L("Inhalte aus SharePoint", "Content from SharePoint"), L("über Compose-Schritte", "via Compose steps"), 147),
             (580, 128, L("Dynamische Anrede", "Dynamic salutation"), L("Herr / Frau", "Mr / Ms (German)"), 147),
             (580, 280, L("Klare Handlung", "Clear action"), L("Ein Button, ein Ziel", "One button, one goal"), 299),
             (580, 338, L("Pflichtlinks", "Required links"), L("Impressum, Datenschutz", "Legal, privacy"), 360)]
    for i, (nx, ny, t, s, ty) in enumerate(notes):
        d.node(f"c{i}", nx, ny - 20, 160, 46, t, s, kind="soft")
        if nx < x:
            d.poly([(nx + 160, ty - 18), (x - 4, ty - 18)])
        else:
            d.poly([(nx, ty - 18), (x + w + 4, ty - 18)])
    return d

def security_layers(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 360, L("Mehrschichtige Sicherheit", "Defence in depth"))
    layers = [(L("Richtlinien, Audit und Nachweis", "Policies, audit and evidence"), "ISO/IEC 27001"),
              (L("Identität und Zugriff", "Identity and access"), L("Least Privilege, MFA", "Least privilege, MFA")),
              (L("Netzwerk", "Network"), L("Segmentierung, Firewall", "Segmentation, firewall")),
              (L("Endgeräte und Server", "Endpoints and servers"), L("Härtung, Patches", "Hardening, patching")),
              (L("Daten", "Data"), L("Backup, Klassifizierung", "Backup, classification"))]
    for i, (t, s) in enumerate(layers):
        x, y = 20 + i * 44, 16 + i * 52
        w, h = 520 - i * 88, 328 - i * 104 / 1
        h = 328 - i * 62
        d.raw(f'<g class="dg-layer l{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{16 - i*2}"/>'
              f'<text class="dg-t" x="{x+16}" y="{y+24}">{e(t)}</text><text class="dg-s" x="{x+16}" y="{y+40}">{e(s)}</text></g>')
    d.node("k1", 580, 60, 160, 70, "2.500+", L("Nutzerkonten", "user accounts"), kind="primary", center=True)
    d.node("k2", 580, 150, 160, 70, "34", L("Standorte", "sites"), kind="accent", center=True)
    d.node("k3", 580, 240, 160, 70, L("Dokumentiert", "Documented"), L("jede Änderung", "every change"), kind="soft", center=True)
    return d

def radial(lang, title, center, items, dashed_last=False):
    d = D(760, 390, title)
    d.node("c", 280, 162, 200, 66, center[0], center[1], kind="primary", center=True)
    pos = [(20, 24), (20, 162), (20, 300), (560, 24), (560, 162), (560, 300), (280, 310)]
    for i, (t, s, tile) in enumerate(items):
        x, y = pos[i]
        last = dashed_last and i == len(items) - 1
        d.node(f"i{i}", x, y, 180, 62 if y != 310 else 60, t, s, tile=tile, kind="guard" if last else "")
        if y == 310:
            d.edge("c", f"i{i}", sa="b", sb="t", dashed=last)
        else:
            d.edge("c", f"i{i}", curve=True, sa="l" if x < 280 else "r", sb="r" if x < 280 else "l", dashed=last)
    return d

def ecosystem(lang):
    L = (lambda de, en: de if lang == "de" else en)
    return radial(lang, L("Projektlandschaft", "Project landscape"), ("Microsoft 365", L("Ein Tenant, viele Lösungen", "One tenant, many solutions")), [
        (L("Intranet", "Intranet"), L("Rollenportale", "Role portals"), "sp"),
        (L("Besprechungs-Tracker", "Meeting tracker"), "Power Apps", "app"),
        (L("E-Mail-Kampagnen", "Email campaigns"), L("HTML aus Flows", "HTML from flows"), "ol"),
        (L("Projektsteuerung", "Project control"), "Trello + REST-API", "tr"),
        (L("Wartungserinnerungen", "Maintenance reminders"), L("≈ 1.600 Kunden", "≈ 1,600 customers"), "pa"),
        (L("E-Mail-Tracking", "Email tracking"), "Power Apps + Flow", "app"),
        (L("ERP-Anbindung", "ERP integration"), L("RPA, in Prüfung", "RPA, under review"), "erp"),
    ], dashed_last=True)

def competence(lang):
    L = (lambda de, en: de if lang == "de" else en)
    return radial(lang, L("Kompetenzprofil", "Competence profile"), ("Hashmat Bahadari", L("IT & Digitale Automatisierung", "IT & Digital Automation")), [
        (L("IT-Sicherheit", "IT security"), "ISO 27001, IAM, CEH", "id"),
        ("Microsoft 365", "Entra ID, Exchange, Teams", "sp"),
        ("Azure", "AZ-500, AZ-900, SC-900", "cld"),
        ("Power Platform", "Automate, Apps, Forms", "pa"),
        (L("Netzwerk & Server", "Network & servers"), "Fortinet, Windows", "net"),
        (L("Dokumentation", "Documentation"), L("SOPs, Schulungen", "SOPs, training"), "doc"),
        (L("Sprachen", "Languages"), L("Deutsch, Englisch, Persisch", "German, English, Persian"), "usr"),
    ])

def cert_map(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 340, L("Zertifizierungen und Leistungen", "Certifications and services"))
    cs = [(L("Sicherheit & Audit", "Security & audit"), "ISO 27001, CEH, IAM", "id"),
          ("Microsoft & Azure", "AZ-500, SC-900, AZ-900, MCITP", "cld"),
          (L("Netzwerk & Grundlagen", "Networking & foundations"), "Security+, Network+, NSE", "net")]
    for i, (t, s, tile) in enumerate(cs):
        d.node(f"c{i}", 20, 40 + i * 100, 250, 64, t, s, tile=tile, kind="accent")
    sv = [(L("Systemadministration", "System administration"), "net"), ("Microsoft Cloud", "cld"), (L("Automatisierung", "Automation"), "pa"), (L("Intranet & Wissensbasis", "Intranet & knowledge base"), "sp")]
    for i, (t, tile) in enumerate(sv):
        d.node(f"s{i}", 490, 24 + i * 78, 250, 56, t, tile=tile)
    for a, b in [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 0)]:
        d.edge(f"c{a}", f"s{b}", curve=True, sa="r", sb="l")
    return d

def contact_process(lang):
    L = (lambda de, en: de if lang == "de" else en)
    d = D(760, 140, L("Ablauf einer Zusammenarbeit", "How a project runs"))
    st = [(L("Termin buchen", "Book a slot"), "Microsoft Bookings", "sch"), (L("Erstgespräch", "Intro call"), L("30 Min., kostenlos", "30 min, free"), "tm"),
          (L("Einschätzung", "Assessment"), L("schriftlich", "in writing"), "doc"), (L("Umsetzung", "Delivery"), L("Pilot, Rollout", "Pilot, rollout"), "pa"),
          (L("Betreuung", "Support"), L("nach Bedarf", "as needed"), "usr")]
    for i, (t, s, tile) in enumerate(st):
        d.node(f"s{i}", 20 + i * 148, 38, 128, 64, t, s, tile=tile, kind="primary" if i == 0 else "")
        if i: d.edge(f"s{i-1}", f"s{i}")
    return d


PROJECT_DIAGRAMS = {"heat-pump": phases, "intranet": intranet_request, "reminders": reminder_pipe,
                    "meeting-tracker": tracker_mock, "email-tracking": flow_email, "erp-rpa": erp_decision,
                    "campaigns": email_wire, "security": security_layers}
SERVICE_DIAGRAMS = {"automation": flow_guard, "cloud": cloud_identity, "sysadmin": network, "intranet": intranet_tree}
