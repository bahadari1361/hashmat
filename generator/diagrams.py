# -*- coding: utf-8 -*-
"""Diagram engine v3 – clean, standard notation.
Reference-architecture style (zones + line icons), BPMN 2.0 for processes,
classic topology symbols for networks. All diagrams bilingual."""
import html
e = html.escape

IC = {
 "user": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5"/>',
 "users": '<circle cx="9" cy="8.5" r="3"/><path d="M3.5 19c.6-3 2.8-4.6 5.5-4.6s4.9 1.6 5.5 4.6"/><circle cx="16.5" cy="9" r="2.5"/><path d="M15.8 14.5c2.3.1 4.1 1.5 4.7 4"/>',
 "laptop": '<rect x="5" y="5" width="14" height="10" rx="1.5"/><path d="M3 18.5h18"/>',
 "phone": '<rect x="7.5" y="3" width="9" height="18" rx="2"/><path d="M11 18h2"/>',
 "pc": '<rect x="3.5" y="4" width="17" height="11" rx="1.5"/><path d="M9 20h6M12 15v5"/>',
 "server": '<rect x="5" y="3.5" width="14" height="7" rx="1.5"/><rect x="5" y="13.5" width="14" height="7" rx="1.5"/><path d="M8 7h.01M8 17h.01M11 7h5M11 17h5"/>',
 "nas": '<rect x="6" y="3" width="12" height="18" rx="1.5"/><path d="M9 7h6M9 10.5h6M9 14h6M12 17.5h.01"/>',
 "cloud": '<path d="M7.5 18h9.5a4 4 0 0 0 .5-7.96A5.8 5.8 0 0 0 6.4 9.1 4.4 4.4 0 0 0 7.5 18Z"/>',
 "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 2.5 14.4 0 17M12 3.5c-2.5 2.6-2.5 14.4 0 17"/>',
 "firewall": '<rect x="3.5" y="5" width="17" height="14" rx="1"/><path d="M3.5 9.7h17M3.5 14.3h17M9 5v4.7M15 5v4.7M6 9.7v4.6M12 9.7v4.6M18 9.7v4.6M9 14.3V19M15 14.3V19"/>',
 "router": '<circle cx="12" cy="12" r="8.5"/><path d="M7 12h10M14 9l3 3-3 3M10 9l-3 3 3 3"/>',
 "switch": '<rect x="3" y="7" width="18" height="10" rx="1.5"/><path d="M6.5 10.5h3M6.5 13.5h3M12.5 10.5h.01M15 10.5h.01M17.5 10.5h.01M12.5 13.5h.01M15 13.5h.01M17.5 13.5h.01"/>',
 "ap": '<path d="M5.5 10a9 9 0 0 1 13 0M8 12.6a5.5 5.5 0 0 1 8 0M10.5 15.2a2 2 0 0 1 3 0"/><circle cx="12" cy="18.3" r=".9"/>',
 "printer": '<path d="M7 9V4h10v5"/><rect x="4" y="9" width="16" height="7" rx="1.5"/><path d="M7 14h10v6H7z"/>',
 "shield": '<path d="M12 3.5l7 2.6v5.4c0 4.4-3 7.6-7 9-4-1.4-7-4.6-7-9V6.1z"/><path d="M9 12l2 2 4-4"/>',
 "key": '<circle cx="8" cy="12" r="3.5"/><path d="M11.5 12H20M17 12v3M20 12v2"/>',
 "lock": '<rect x="5" y="10.5" width="14" height="9.5" rx="1.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
 "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="1.5"/><path d="M4 7l8 6 8-6"/>',
 "chat": '<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7a2.5 2.5 0 0 1-2.5 2.5H10l-4.5 4v-4A2 2 0 0 1 4 14z"/>',
 "folder": '<path d="M3.5 7A1.5 1.5 0 0 1 5 5.5h4l2 2h8A1.5 1.5 0 0 1 20.5 9v8.5A1.5 1.5 0 0 1 19 19H5a1.5 1.5 0 0 1-1.5-1.5z"/>',
 "doc": '<path d="M7 3.5h7l4 4v13H7z"/><path d="M14 3.5v4h4M9.5 12h6M9.5 15.5h6"/>',
 "list": '<path d="M9 7h11M9 12h11M9 17h11M4.5 7h.01M4.5 12h.01M4.5 17h.01"/>',
 "table": '<rect x="3.5" y="5" width="17" height="14" rx="1.5"/><path d="M3.5 10h17M3.5 14.5h17M9.5 10v9"/>',
 "flow": '<rect x="3.5" y="4" width="6" height="5" rx="1"/><rect x="14.5" y="15" width="6" height="5" rx="1"/><path d="M9.5 6.5H14a3 3 0 0 1 3 3V15"/>',
 "app": '<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><path d="M3.5 8.5h17M7 12h4v4H7zM14 12h3M14 15h3"/>',
 "form": '<rect x="5" y="3.5" width="14" height="17" rx="1.5"/><path d="M8 8h8M8 11.5h8M8 15h4"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 "search": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
 "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>',
 "chart": '<path d="M4 20V4M4 20h16M8 16v-4M12 16V8M16 16v-6"/>',
 "building": '<path d="M5 20.5V5l7-2v17.5M12 8h7v12.5M8 8h1M8 11h1M8 14h1M15 11h1M15 14h1M3.5 20.5h17"/>',
 "desktopapp": '<rect x="3.5" y="4" width="17" height="12" rx="1.5"/><path d="M3.5 7.5h17M9 20h6M12 16v4"/>',
 "robot": '<rect x="5" y="8" width="14" height="10" rx="2"/><path d="M12 8V5.5M9.5 12.5h.01M14.5 12.5h.01M9.5 15.5h5"/><circle cx="12" cy="4.5" r="1"/>',
 "alert": '<path d="M12 4l9 16H3z"/><path d="M12 10v4M12 17h.01"/>',
 "backup": '<path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3"/><path d="M4.5 4.5v3.5H8"/><path d="M12 8.5V12l2.5 1.8"/>',
 "book": '<path d="M4 5.5A2 2 0 0 1 6 3.5h13v15H6a2 2 0 0 0-2 2z"/><path d="M4 20.5a2 2 0 0 0 2 0h13"/>',
 "id": '<rect x="3.5" y="5.5" width="17" height="13" rx="1.5"/><circle cx="9" cy="11" r="2"/><path d="M6 15.5c.6-1.4 1.7-2 3-2s2.4.6 3 2M14 10h4M14 13h3"/>',
 "excel": '<rect x="4" y="3.5" width="16" height="17" rx="1.5"/><path d="M4 8.5h16M4 13.5h16M10 8.5v12"/>',
 "funnel": '<path d="M4 5h16l-6 7.5V19l-4-2v-4.5z"/>',
}

def tw(t, s=12.5): return len(t) * s * 0.56


class D:
    n = 0
    def __init__(self, w, h, title):
        D.n += 1; self.uid = f"g{D.n}"
        self.w, self.h, self.title = w, h, title
        self.nodes = {}; self.extra = {}; self.bg = []; self.ln = []; self.fg = []

    # ------------------------------------------------ helpers
    def _ico(self, name, x, y, size, cls="ic"):
        s = size / 24
        return f'<g class="{cls}" transform="translate({x} {y}) scale({s})">{IC[name]}</g>'

    def _text(self, x, y, lines, cls, anchor="middle", lh=14.5):
        return "".join(f'<text class="{cls}" x="{x}" y="{y + i*lh}" text-anchor="{anchor}">{e(t)}</text>' for i, t in enumerate(lines))

    # ------------------------------------------------ containers
    def zone(self, zid, x, y, w, h, label, kind=""):
        self.nodes[zid] = (x, y, w, h)
        self.bg.append(f'<g class="z {kind}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'
                       f'<text class="zl" x="{x+14}" y="{y+21}">{e(label)}</text></g>')

    def lane(self, x, y, w, h, label):
        self.bg.append(f'<g class="lane"><rect x="{x}" y="{y}" width="{w}" height="{h}"/>'
                       f'<rect class="lh" x="{x}" y="{y}" width="30" height="{h}"/>'
                       f'<text class="ll" transform="translate({x+19} {y+h/2}) rotate(-90)" text-anchor="middle">{e(label)}</text></g>')

    # ------------------------------------------------ nodes
    def icon(self, nid, cx, cy, label, sub=None, ic="gear", kind="", size=50):
        x, y = cx - size/2, cy - size/2
        self.nodes[nid] = (x, y, size, size)
        self.extra[nid] = 8 + 14.5 * len(label.split("\n")) + (13 * len(sub.split("\n")) if sub else 0)
        out = f'<g class="in {kind}"><rect x="{x}" y="{y}" width="{size}" height="{size}" rx="13"/>'
        out += self._ico(ic, cx - 13, cy - 13, 26)
        out += self._text(cx, y + size + 17, label.split("\n"), "t")
        if sub:
            out += self._text(cx, y + size + 17 + 14.5 * len(label.split("\n")), sub.split("\n"), "s", lh=13)
        self.fg.append(out + "</g>")

    def box(self, nid, x, y, w, h, title, sub=None, ic=None, kind="", center=False):
        self.nodes[nid] = (x, y, w, h)
        out = f'<g class="bx {kind}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
        tl = title.split("\n"); sl = sub.split("\n") if sub else []
        tot = len(tl) * 15 + len(sl) * 13
        ty = y + (h - tot) / 2 + 11
        if ic and not center:
            out += f'<rect class="bi" x="{x+12}" y="{y+h/2-16}" width="32" height="32" rx="8"/>' + self._ico(ic, x + 18, y + h/2 - 10, 20)
            tx, anc = x + 54, "start"
        elif center:
            tx, anc = x + w/2, "middle"
        else:
            tx, anc = x + 14, "start"
        avail = w - (54 if (ic and not center) else 14) - 10
        def fit(lines, size):
            m = max((len(x) for x in lines), default=0) * size * 0.56
            return f' style="font-size:{max(9.5, size*avail/m):.1f}px"' if m > avail else ""
        ft, fs = fit(tl, 12.5), fit(sl, 11)
        out += "".join(f'<text class="t" x="{tx}" y="{ty + i*15}" text-anchor="{anc}"{ft}>{e(t)}</text>' for i, t in enumerate(tl))
        out += "".join(f'<text class="s" x="{tx}" y="{ty + len(tl)*15 + i*13}" text-anchor="{anc}"{fs}>{e(t)}</text>' for i, t in enumerate(sl))
        self.fg.append(out + "</g>")

    def task(self, nid, x, y, w, h, title, ic=None, kind=""):
        """BPMN task. ic: 'user' (user task), 'gear' (service task), 'mail' (send task)."""
        self.nodes[nid] = (x, y, w, h)
        out = f'<g class="tk {kind}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/>'
        if ic:
            out += self._ico(ic, x + 7, y + 6, 14, "tic")
        tl = title.split("\n")
        ty = y + h/2 - (len(tl) - 1) * 7.5 + 4.5
        out += self._text(x + w/2, ty, tl, "tt", "middle", 15)
        self.fg.append(out + "</g>")

    def event(self, nid, cx, cy, kind="start", label=None, ic=None, above=False):
        r = 16
        self.nodes[nid] = (cx - r, cy - r, 2*r, 2*r)
        out = f'<g class="ev {kind}"><circle cx="{cx}" cy="{cy}" r="{r}"/>'
        if ic:
            out += self._ico(ic, cx - 9, cy - 9, 18, "eic")
        if label:
            n = len(label.split("\n"))
            ly = cy - r - 8 - 13 * (n - 1) if above else cy + r + 15
            out += self._text(cx, ly, label.split("\n"), "s", lh=13)
        self.fg.append(out + "</g>")

    def gw(self, nid, cx, cy, label=None, above=True, right=False):
        s = 22
        self.nodes[nid] = (cx - s, cy - s, 2*s, 2*s)
        out = (f'<g class="gw"><path d="M{cx} {cy-s} L{cx+s} {cy} L{cx} {cy+s} L{cx-s} {cy} Z"/>'
               f'<path class="gx" d="M{cx-7} {cy-7} L{cx+7} {cy+7} M{cx+7} {cy-7} L{cx-7} {cy+7}"/>')
        if label and right:
            out += self._text(cx + s + 8, cy + 4, [label], "s", "start")
        elif label:
            ly = cy - s - 8 if above else cy + s + 16
            out += self._text(cx, ly, [label], "s")
        self.fg.append(out + "</g>")

    def num(self, x, y, n):
        self.fg.append(f'<g class="nm"><circle cx="{x}" cy="{y}" r="10"/><text x="{x}" y="{y+4}" text-anchor="middle">{n}</text></g>')

    def note(self, x, y, text, anchor="start"):
        self.fg.append(f'<text class="nt" x="{x}" y="{y}" text-anchor="{anchor}">{e(text)}</text>')

    # ------------------------------------------------ connectors
    def _a(self, nid, side):
        x, y, w, h = self.nodes[nid]
        return {"l": (x, y+h/2), "r": (x+w, y+h/2), "t": (x+w/2, y), "b": (x+w/2, y+h+self.extra.get(nid, 0))}[side]

    def curve(self, a, b, sa="r", sb="l"):
        (sx, sy), (ex, ey) = self._a(a, sa), self._a(b, sb)
        c = (ex - sx) * .5
        self.ln.append(f'<path class="ed" d="M{sx} {sy} C{sx+c} {sy} {ex-c} {ey} {ex} {ey}" marker-end="url(#{self.uid}m)"/>')

    def edge(self, a, b, label=None, sa=None, sb=None, dashed=False, arrow=True, both=False, lpos=0.5, kind=""):
        ax, ay, aw, ah = self.nodes[a]; bx, by, bw, bh = self.nodes[b]
        dx = (bx+bw/2) - (ax+aw/2); dy = (by+bh/2) - (ay+ah/2)
        if sa is None:
            if abs(dx) >= abs(dy):
                sa, sb = ("r", "l") if dx > 0 else ("l", "r")
            else:
                sa, sb = ("b", "t") if dy > 0 else ("t", "b")
        sx, sy = self._a(a, sa); ex, ey = self._a(b, sb)
        if sa in "lr" and sb in "lr":
            if abs(sy - ey) < 1:
                pts = [(sx, sy), (ex, ey)]
            else:
                mx = sx + (ex - sx) * lpos
                pts = [(sx, sy), (mx, sy), (mx, ey), (ex, ey)]
        elif sa in "tb" and sb in "tb":
            if abs(sx - ex) < 1:
                pts = [(sx, sy), (ex, ey)]
            else:
                my = sy + (ey - sy) * lpos
                pts = [(sx, sy), (sx, my), (ex, my), (ex, ey)]
        elif sa in "lr":
            pts = [(sx, sy), (ex, sy), (ex, ey)]
        else:
            pts = [(sx, sy), (sx, ey), (ex, ey)]
        self.path(pts, label, dashed, arrow, both, kind)

    def path(self, pts, label=None, dashed=False, arrow=True, both=False, kind=""):
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        cls = "ed" + (" ds" if dashed else "") + (f" {kind}" if kind else "")
        mk = (f' marker-end="url(#{self.uid}m)"' if arrow else "") + (f' marker-start="url(#{self.uid}m)"' if both else "")
        self.ln.append(f'<path class="{cls}" d="{d}"{mk}/>')
        if label:
            # label on the longest segment
            best = max(range(len(pts) - 1), key=lambda i: abs(pts[i+1][0]-pts[i][0]) + abs(pts[i+1][1]-pts[i][1]))
            (x1, y1), (x2, y2) = pts[best], pts[best+1]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            lw = tw(label, 11) + 12
            self.fg.append(f'<g class="el"><rect x="{mx-lw/2}" y="{my-9.5}" width="{lw}" height="19" rx="4"/>'
                           f'<text x="{mx}" y="{my+4}" text-anchor="middle">{e(label)}</text></g>')

    def svg(self):
        defs = (f'<defs><marker id="{self.uid}m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">'
                f'<path d="M0 0 L10 5 L0 10 z" class="ah"/></marker></defs>')
        return (f'<svg class="dg" viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{e(self.title)}">'
                + defs + "".join(self.bg) + "".join(self.ln) + "".join(self.fg) + "</svg>")


def T(lang):
    return lambda de, en: de if lang == "de" else en


# =================================================================== OVERVIEW / HOME
def overview(lang):
    L = T(lang)
    d = D(640, 470, L("Referenzarchitektur: moderner Arbeitsplatz", "Reference architecture: modern workplace"))
    d.zone("zu", 16, 16, 150, 438, L("Nutzer & Geräte", "Users & devices"))
    d.icon("u1", 91, 92, L("Büro", "Office"), L("verwaltet", "managed"), "laptop")
    d.icon("u2", 91, 222, L("Mobil", "Mobile"), "iOS, Android", "phone")
    d.icon("u3", 91, 352, L("Remote", "Remote"), "VPN", "user")
    d.zone("zi", 196, 150, 128, 170, "Entra ID", "acc")
    d.icon("id", 260, 218, L("Identität", "Identity"), L("MFA, Richtlinien", "MFA, policies"), "key", "pri")
    d.zone("zm", 354, 16, 270, 230, "Microsoft 365")
    d.icon("ex", 410, 92, "Exchange", L("E-Mail", "Email"), "mail")
    d.icon("sp", 489, 92, "SharePoint", L("Dateien", "Files"), "folder")
    d.icon("tm", 568, 92, "Teams", L("Zusammenarbeit", "Collaboration"), "chat")
    d.note(489, 214, L("Daten zentral, Zugriff nach Rolle", "Central data, role-based access"), "middle")
    d.zone("za", 354, 270, 270, 184, L("Automatisierung", "Automation"))
    d.icon("pa", 430, 346, "Power Automate", L("Abläufe", "Workflows"), "flow")
    d.icon("pp", 548, 346, "Power Apps", L("Oberflächen", "Interfaces"), "app")
    for u in ("u1", "u2", "u3"):
        d.edge(u, "zi", sa="r", sb="l", lpos=.5)
    d.edge("zi", "zm", sa="r", sb="l")
    d.edge("zi", "za", sa="r", sb="l")
    d.edge("zm", "za", sa="b", sb="t", both=True)
    d.num(181, 235, 1); d.num(339, 200, 2); d.num(504, 258, 3)
    return d, [L("Jede Anmeldung läuft über Entra ID mit MFA und Richtlinien für bedingten Zugriff.", "Every sign-in goes through Entra ID with MFA and Conditional Access policies."),
               L("Nach erfolgreicher Prüfung erhalten Nutzer Zugriff auf die Dienste, die ihre Rolle vorsieht.", "Once verified, users get access to the services their role allows."),
               L("Power Automate und Power Apps arbeiten direkt mit den Daten in Microsoft 365.", "Power Automate and Power Apps work directly with data in Microsoft 365.")]

# =================================================================== SERVICES MODEL
def service_model(lang):
    L = T(lang)
    d = D(800, 330, L("Leistungsmodell", "Service model"))
    cols = [("server", L("Systemadministration", "System administration"), [L("Netzwerk & WLAN", "Network & Wi-Fi"), "Firewall & VPN", L("Server & Clients", "Servers & clients"), "Backup"]),
            ("cloud", "Microsoft Cloud", ["Microsoft 365", "Entra ID", L("Sicherheit", "Security"), "Azure"]),
            ("flow", L("Automatisierung", "Automation"), ["Power Automate", "Power Apps", L("Schnittstellen", "Integrations"), L("Datenqualität", "Data quality")]),
            ("book", L("Intranet & Dokumentation", "Intranet & documentation"), ["SharePoint", L("Wissensbasis", "Knowledge base"), L("Arbeitsanweisungen", "Procedures"), L("Schulung", "Training")])]
    for i, (ic, t, items) in enumerate(cols):
        x = 20 + i * 192
        d.zone(f"c{i}", x, 20, 176, 220, "", "")
        d.fg.append(f'<g class="in pri"><rect x="{x+16}" y="36" width="44" height="44" rx="12"/></g>' + d._ico(ic, x + 26, 46, 24, "ic icw"))
        d.fg.append(d._text(x + 16, 106, [t], "t", "start"))
        for j, it in enumerate(items):
            yy = 136 + j * 24
            d.fg.append(f'<circle class="dot" cx="{x+20}" cy="{yy-4}" r="2.6"/>' + d._text(x + 30, yy, [it], "s", "start"))
    d.box("base", 20, 256, 752, 54, L("IT-Sicherheit, Dokumentation und Betreuung als Fundament jeder Leistung", "IT security, documentation and support underpin every service"), ic="shield", kind="pri")
    return d, []

# =================================================================== AUTOMATION (BPMN)
def bpmn_generic(lang):
    L = T(lang)
    d = D(800, 330, L("Prozessmodell (BPMN): automatisierte Bearbeitung einer Anfrage", "Process model (BPMN): automated handling of a request"))
    d.lane(16, 16, 768, 96, L("Fachbereich", "Business"))
    d.lane(16, 112, 768, 108, "Power Automate")
    d.lane(16, 220, 768, 96, "Microsoft 365")
    d.event("s", 80, 64, "start", L("Anfrage\neingegangen", "Request\nreceived"), "form")
    d.task("t1", 130, 140, 130, 52, L("Daten prüfen", "Validate data"), "gear")
    d.gw("g", 320, 166, L("vollständig?", "complete?"))
    d.task("t2", 390, 242, 140, 52, L("Eintrag in Liste\nanlegen", "Create list\nitem"), "gear")
    d.task("t3", 570, 242, 130, 52, L("Team in Teams\ninformieren", "Notify team\nin Teams"), "mail")
    d.event("e1", 744, 268, "end")
    d.task("t4", 390, 140, 140, 52, L("Rückfrage an\nAntragsteller", "Request missing\ninformation"), "mail")
    d.event("e2", 744, 64, "end", L("Rückfrage\ngesendet", "Query\nsent"))
    d.edge("s", "t1", sa="r", sb="t")
    d.edge("t1", "g")
    d.edge("g", "t2", L("ja", "yes"), sa="b", sb="l")
    d.edge("t2", "t3"); d.edge("t3", "e1")
    d.edge("g", "t4", L("nein", "no"))
    d.path([(530, 166), (690, 166), (690, 64), (728, 64)])
    return d, []

# =================================================================== CLOUD IDENTITY
def cloud_arch(lang):
    L = T(lang)
    d = D(800, 430, L("Identität und Zugriff in Microsoft 365", "Identity and access in Microsoft 365"))
    d.zone("zu", 16, 16, 150, 300, L("Zugriff von", "Access from"))
    d.icon("u1", 91, 82, L("Verwaltete Geräte", "Managed devices"), None, "laptop")
    d.icon("u2", 91, 172, L("Mobilgeräte", "Mobile devices"), None, "phone")
    d.icon("u3", 91, 262, L("Gäste", "Guests"), None, "user", "dash")
    d.zone("ze", 206, 16, 250, 300, "Microsoft Entra ID", "acc")
    rows = [("key", L("Mehrstufige Anmeldung", "Multi-factor authentication")), ("lock", L("Bedingter Zugriff", "Conditional Access")),
            ("users", L("Gruppen und Rollen", "Groups and roles")), ("search", L("Anmelde- und Auditprotokolle", "Sign-in and audit logs"))]
    for i, (ic, t) in enumerate(rows):
        d.box(f"e{i}", 222, 46 + i * 66, 218, 52, t, ic=ic)
    d.zone("zm", 496, 16, 288, 300, L("Dienste", "Services"))
    sv = [("mail", "Exchange Online"), ("folder", "SharePoint, OneDrive"), ("chat", "Microsoft Teams"), ("flow", "Power Platform")]
    for i, (ic, t) in enumerate(sv):
        d.box(f"m{i}", 512, 46 + i * 66, 256, 52, t, ic=ic)
    d.zone("zs", 206, 336, 578, 78, L("Sicherheit und Compliance", "Security and compliance"), "acc")
    d.box("s1", 222, 360, 170, 40, "Microsoft Defender", ic=None, center=True)
    d.box("s2", 406, 360, 170, 40, "Microsoft Purview", center=True)
    d.box("s3", 590, 360, 178, 40, L("Sichere Standardwerte", "Secure defaults"), center=True)
    d.edge("u1", "ze", sa="r", sb="l"); d.edge("u2", "ze", sa="r", sb="l"); d.edge("u3", "ze", sa="r", sb="l", dashed=True)
    d.edge("ze", "zm", L("Token", "Token"))
    d.num(186, 130, 1); d.num(476, 148, 2); d.num(476, 326, 3)
    return d, [L("Nutzer melden sich von verwalteten Geräten, Mobilgeräten oder als Gast an.", "Users sign in from managed devices, mobile devices or as guests."),
               L("Entra ID prüft Identität, Gerät und Risiko und stellt ein Zugriffstoken aus.", "Entra ID checks identity, device and risk, then issues an access token."),
               L("Defender und Purview überwachen Dienste und Daten übergreifend.", "Defender and Purview monitor services and data across the tenant.")]

# =================================================================== NETWORK TOPOLOGY
def network(lang):
    L = T(lang)
    d = D(800, 600, L("Netzwerktopologie: Standort mit Büro, Server und WLAN", "Network topology: site with office, servers and Wi-Fi"))
    d.icon("inet", 400, 44, "Internet", None, "globe")
    d.icon("m365", 640, 44, "Microsoft 365", None, "cloud")
    d.icon("rtr", 400, 150, L("Router / Modem", "Router / modem"), L("Provider", "ISP"), "router")
    d.icon("fw", 400, 262, L("Firewall (NGFW)", "Firewall (NGFW)"), L("IPS, Webfilter, VPN", "IPS, web filter, VPN"), "firewall", "pri")
    d.icon("vpn", 150, 262, L("Remote-Nutzer", "Remote users"), L("SSL-VPN + MFA", "SSL VPN + MFA"), "laptop")
    d.icon("bk", 650, 262, L("Offsite-Backup", "Off-site backup"), L("Kopie außer Haus", "copy off site"), "backup")
    d.icon("core", 400, 372, "Core-Switch", L("VLAN-Routing, PoE", "VLAN routing, PoE"), "switch")
    d.edge("inet", "rtr"); d.edge("inet", "m365", dashed=True, arrow=False)
    d.edge("rtr", "fw"); d.edge("fw", "core")
    d.edge("vpn", "fw", L("Tunnel", "Tunnel"), dashed=True, both=True)
    vl = [("VLAN 10", L("Arbeitsplätze", "Workstations"), [("pc", L("Clients", "Clients")), ("printer", L("Drucker", "Printers"))]),
          ("VLAN 20", "Server", [("server", "Server"), ("nas", "NAS")]),
          ("VLAN 30", L("WLAN intern", "Wi-Fi internal"), [("ap", "AP 1"), ("ap", "AP 2")]),
          ("VLAN 40", L("WLAN Gäste", "Wi-Fi guests"), [("ap", L("Gast-AP", "Guest AP")), ("globe", L("nur Internet", "Internet only"))])]
    for i, (v, lab, items) in enumerate(vl):
        x = 16 + i * 194
        d.zone(f"v{i}", x, 456, 184, 128, f"{v}: {lab}", "acc" if i == 1 else ("dash" if i == 3 else ""))
        for j, (ic, t) in enumerate(items):
            d.icon(f"v{i}{j}", x + 50 + j * 84, 518, t, None, ic, size=40)
        d.edge("core", f"v{i}", sa="b", sb="t", lpos=.5)
    d.edge("fw", "bk", L("verschlüsselt", "encrypted"), dashed=True)
    d.num(432, 236, 1); d.num(275, 242, 2); d.num(432, 346, 3); d.num(525, 242, 4)
    return d, [L("Die Firewall trennt Internet und internes Netz und filtert den Datenverkehr (IPS, Webfilter).", "The firewall separates internet and internal network and filters traffic (IPS, web filter)."),
               L("Remote-Zugriff nur über verschlüsseltes VPN mit zweitem Faktor.", "Remote access only via encrypted VPN with a second factor."),
               L("VLANs trennen Arbeitsplätze, Server, internes WLAN und Gäste. Gäste erreichen nur das Internet.", "VLANs separate workstations, servers, internal Wi-Fi and guests. Guests reach the internet only."),
               L("Sicherungen werden zusätzlich verschlüsselt außer Haus gespeichert (3-2-1-Regel).", "Backups are additionally stored encrypted off site (3-2-1 rule).")]

def fw_zones(lang):
    L = T(lang)
    d = D(800, 590, L("Firewall-Zonen und Regelwerk", "Firewall zones and rule base"))
    d.fg.append(f'<g class="bx pri"><rect x="350" y="20" width="100" height="300" rx="12"/></g>' + d._ico("firewall", 382, 40, 36, "ic icw"))
    d.fg.append(f'<text class="t" fill="#fff" style="fill:#fff" transform="translate(400 200) rotate(-90)" text-anchor="middle">{e(L("Firewall (NGFW)", "Firewall (NGFW)"))}</text>')
    d.fg.append(f'<text class="s" style="fill:#AFC4D9" transform="translate(422 200) rotate(-90)" text-anchor="middle">{e(L("Standard: alles verweigern", "Default: deny all"))}</text>')
    d.nodes["fwL"] = (350, 20, 0, 300); d.nodes["fwR"] = (450, 20, 0, 300)
    left = [("lan", 40, "LAN (VLAN 10)", L("Arbeitsplätze, Drucker", "Workstations, printers"), "pc", ""),
            ("srv", 140, "SERVER (VLAN 20)", L("Datei-, Anwendungsserver, NAS", "File, app servers, NAS"), "server", "acc"),
            ("vpn", 240, "VPN", L("Remote-Nutzer mit MFA", "Remote users with MFA"), "lock", "")]
    right = [("wan", 40, "WAN", L("Internet, Microsoft 365", "Internet, Microsoft 365"), "globe", ""),
             ("wl", 140, L("WLAN intern (VLAN 30)", "Wi-Fi internal (VLAN 30)"), "WPA3-Enterprise, 802.1X", "ap", ""),
             ("gst", 240, L("GAST (VLAN 40)", "GUEST (VLAN 40)"), L("isoliert, Bandbreite begrenzt", "isolated, bandwidth-limited"), "ap", "soft")]
    for nid, y, t, sub, ic, k in left:
        d.box(nid, 16, y, 270, 60, t, sub, ic=ic, kind=k)
        d.path([(286, y + 30), (350, y + 30)], both=True, dashed=(nid == "vpn"))
    for nid, y, t, sub, ic, k in right:
        d.box(nid, 514, y, 270, 60, t, sub, ic=ic, kind=k)
        d.path([(450, y + 30), (514, y + 30)], both=True)
    # rule table
    hdr = [L("Quelle", "Source"), L("Ziel", "Destination"), L("Erlaubt", "Allowed"), L("Aktion", "Action")]
    rows = [("LAN", "SERVER", L("Datei, Druck, Anwendungen", "File, print, applications"), "allow"),
            ("LAN", "WAN", L("Web (HTTPS), gefiltert", "Web (HTTPS), filtered"), "allow"),
            (L("WLAN intern", "Wi-Fi internal"), "SERVER, WAN", L("wie LAN", "same as LAN"), "allow"),
            ("VPN", "SERVER", L("nur benötigte Dienste", "required services only"), "allow"),
            (L("GAST", "GUEST"), "WAN", L("nur Web", "web only"), "allow"),
            (L("GAST", "GUEST"), "LAN, SERVER", L("kein Zugriff", "no access"), "deny"),
            (L("alle", "any"), L("alle", "any"), L("alles andere", "everything else"), "deny")]
    cx = [30, 190, 360, 660]
    y0 = 350
    d.fg.append(f'<rect class="row alt" x="16" y="{y0}" width="768" height="28" rx="4"/>')
    d.fg.append("".join(d._text(x, y0 + 18, [h], "t", "start") for x, h in zip(cx, hdr)))
    for i, (a, b, c, act) in enumerate(rows):
        y = y0 + 30 + i * 28
        d.fg.append(f'<rect class="row" x="16" y="{y}" width="768" height="28"/><path class="rl" d="M16 {y+28} H784"/>')
        d.fg.append(d._text(cx[0], y + 18, [a], "s", "start") + d._text(cx[1], y + 18, [b], "s", "start") + d._text(cx[2], y + 18, [c], "s", "start"))
        lab = L("erlauben", "allow") if act == "allow" else L("verweigern", "deny")
        d.fg.append(f'<g class="act {act}"><rect x="{cx[3]}" y="{y+5}" width="{tw(lab, 11)+18}" height="18" rx="9"/><text x="{cx[3]+9}" y="{y+18}">{e(lab)}</text></g>')
    return d, []

# =================================================================== INTRANET
def intranet_ia(lang):
    L = T(lang)
    d = D(800, 400, L("Informationsarchitektur eines Intranets", "Intranet information architecture"))
    d.box("hub", 290, 16, 220, 60, L("Startseite (Hub)", "Home (hub)"), L("News, Termine, Schnellzugriff", "News, events, quick links"), ic="building", kind="pri")
    portals = [(L("Alle Mitarbeitenden", "All staff"), "users", [L("Unternehmen", "Company"), L("Ansprechpartner", "Contacts"), L("Erste Hilfe", "First aid")]),
               (L("Service & Außendienst", "Service & field"), "gear", [L("Arbeitsanweisungen", "Procedures"), L("Sicherheit", "Safety"), L("Melden & Beantragen", "Report & request")]),
               (L("Verwaltung", "Administration"), "doc", [L("Abläufe", "Processes"), L("Vorlagen", "Templates"), L("Aufgaben-App", "Task app")]),
               (L("Geschäftsleitung", "Management"), "chart", [L("Kennzahlen", "Key figures"), L("Freigaben", "Approvals"), L("Besprechungen", "Meetings")])]
    for i, (t, ic, items) in enumerate(portals):
        x = 16 + i * 196
        d.box(f"p{i}", x, 126, 180, 52, t, ic=ic, kind="acc")
        d.edge("hub", f"p{i}", sa="b", sb="t", lpos=.5)
        for j, it in enumerate(items):
            yy = 206 + j * 46
            d.box(f"p{i}{j}", x + 22, yy, 158, 36, it, kind="soft")
            d.path([(x + 11, 178), (x + 11, yy + 18), (x + 22, yy + 18)], arrow=False)
    d.box("perm", 16, 352, 768, 34, L("Berechtigungen über Entra-ID-Gruppen: Jede Rolle sieht, was sie braucht.", "Permissions via Entra ID groups: each role sees what it needs."), ic=None, kind="soft", center=True)
    return d, []

def intranet_arch(lang):
    L = T(lang)
    d = D(800, 360, L("Technischer Aufbau eines SharePoint-Intranets", "Technical structure of a SharePoint intranet"))
    d.zone("z", 200, 16, 584, 328, "SharePoint Online", "acc")
    d.icon("u", 90, 180, L("Mitarbeitende", "Staff"), L("Browser, Teams, App", "Browser, Teams, app"), "users")
    d.box("hub", 230, 50, 200, 56, L("Hub-Website", "Hub site"), L("Navigation, News", "Navigation, news"), ic="building", kind="pri")
    d.box("s1", 230, 150, 200, 52, L("Portal-Websites", "Portal sites"), L("je Rolle", "per role"), ic="folder")
    d.box("s2", 230, 250, 200, 52, L("Bibliotheken", "Libraries"), L("Dokumente, Vorlagen", "Documents, templates"), ic="doc")
    d.box("a1", 520, 50, 240, 52, "Power Apps", L("eingebettete Anwendungen", "embedded apps"), ic="app")
    d.box("a2", 520, 150, 240, 52, "Microsoft Forms", L("Meldungen, Anträge", "reports, requests"), ic="form")
    d.box("a3", 520, 250, 240, 52, "Power Automate", L("Freigaben, Benachrichtigungen", "approvals, notifications"), ic="flow")
    d.edge("u", "hub", sa="r", sb="l"); d.edge("hub", "s1", sa="b", sb="t"); d.edge("s1", "s2", sa="b", sb="t")
    d.edge("hub", "a1"); d.edge("s1", "a2"); d.edge("a2", "a3", sa="b", sb="t"); d.edge("a3", "s2", L("speichert", "stores"))
    return d, []

# =================================================================== APPROACH
def approach(lang):
    L = T(lang)
    d = D(800, 250, L("Vorgehensmodell", "Delivery model"))
    ph = [(L("Analyse", "Analysis"), "search", L("Ist-Aufnahme\nAnforderungen", "Current state\nrequirements")),
          (L("Konzept", "Design"), "doc", L("Lösungsskizze\nAufwand", "Solution outline\neffort")),
          ("Pilot", "gear", L("Test mit\nechten Daten", "Test with\nreal data")),
          ("Rollout", "users", L("Einführung\nEinweisung", "Go-live\ntraining")),
          (L("Betrieb", "Operate"), "book", L("Dokumentation\nBetreuung", "Documentation\nsupport"))]
    for i, (t, ic, s) in enumerate(ph):
        x = 16 + i * 156
        k = "pri" if i == 2 else ""
        d.box(f"p{i}", x, 30, 140, 64, t, L("Phase ", "Phase ") + str(i + 1), ic=ic, kind=k)
        d.fg.append(d._text(x + 70, 130, s.split("\n"), "s", "middle", 15))
        if i: d.edge(f"p{i-1}", f"p{i}")
    d.path([(86, 170), (86, 200), (710, 200), (710, 170)], arrow=False, dashed=True)
    d.note(398, 224, L("Nach jeder Phase entscheiden Sie, ob es weitergeht.", "You decide after every phase whether to continue."), "middle")
    return d, []

# =================================================================== SOLUTIONS MATRIX
def matrix(lang, sols):
    L = T(lang)
    cols = ["SharePoint", "Automate", "Apps", "Teams", "Entra ID", L("Netzwerk", "Network")]
    d = D(800, 70 + len(sols) * 30, L("Lösungen und eingesetzte Technologien", "Solutions and technologies used"))
    x0 = 330
    for j, c in enumerate(cols):
        d.fg.append(d._text(x0 + j * 76 + 30, 34, [c], "s", "middle"))
    for i, (title, flags) in enumerate(sols):
        y = 58 + i * 30
        d.fg.append(f'<rect class="row{" alt" if i % 2 else ""}" x="16" y="{y-17}" width="768" height="30" rx="4"/>')
        d.fg.append(d._text(30, y + 2, [title], "t", "start"))
        for j, f in enumerate(flags):
            if f:
                d.fg.append(f'<circle class="mdot" cx="{x0 + j*76 + 30}" cy="{y-2}" r="6.5"/>')
    return d, []

# =================================================================== SOLUTION DIAGRAMS
def s_project(lang):
    L = T(lang)
    d = D(800, 330, L("BPMN: Projektsteuerung mit Phasenprüfung", "BPMN: project control with phase gates"))
    d.lane(16, 16, 768, 130, L("Projektleitung", "Project lead"))
    d.lane(16, 146, 768, 170, L("Automatisierung", "Automation"))
    d.event("s", 76, 230, "start", L("neues Projekt", "new project"))
    d.task("t0", 120, 204, 150, 52, L("Karte mit\nChecklisten anlegen", "Create card\nwith checklists"), "gear")
    d.task("t1", 330, 55, 150, 52, L("Phase bearbeiten", "Work on phase"), "user")
    d.task("t2", 520, 55, 150, 52, L("Karte in nächste\nPhase schieben", "Move card to\nnext phase"), "user")
    d.gw("g", 595, 230, L("Checkliste vollständig?", "Checklist complete?"), above=False)
    d.task("t3", 650, 204, 120, 52, L("zurück +\nKommentar", "move back +\ncomment"), "mail")
    d.task("t4", 330, 204, 170, 52, L("nächste Checkliste,\nTitel aktualisieren", "next checklist,\nupdate title"), "gear")
    d.event("e", 744, 81, "end", L("Abschluss", "completed"))
    d.edge("s", "t0")
    d.path([(195, 204), (195, 81), (330, 81)])
    d.edge("t1", "t2")
    d.edge("t2", "g", sa="b", sb="t")
    d.edge("g", "t4", L("ja", "yes"), sa="l", sb="r")
    d.edge("g", "t3", L("nein", "no"), sa="r", sb="l")
    d.path([(405, 204), (405, 107)])
    d.path([(710, 204), (710, 125), (450, 125), (450, 107)])
    d.path([(670, 70), (728, 70)], L("letzte", "last"))
    return d, []

def s_requests(lang):
    L = T(lang)
    d = D(800, 440, L("BPMN: digitaler Antrag mit Freigabe", "BPMN: digital request with approval"))
    d.lane(16, 16, 768, 104, L("Mitarbeitende", "Employee"))
    d.lane(16, 120, 768, 104, "Power Automate")
    d.lane(16, 224, 768, 104, L("Vorgesetzte", "Manager"))
    d.lane(16, 328, 768, 104, L("Verwaltung", "Administration"))
    d.event("s", 80, 60, "start", L("Formular abgeschickt", "Form submitted"), "form")
    d.task("t1", 140, 146, 150, 52, L("Antrag speichern,\nFreigabe starten", "Store request,\nstart approval"), "gear")
    d.task("t2", 330, 250, 140, 52, L("Antrag prüfen", "Review request"), "user")
    d.gw("g", 530, 276, L("genehmigt?", "approved?"), right=True)
    d.task("t3", 600, 354, 130, 52, L("Bestellung\nausführen", "Fulfil\nrequest"), "user")
    d.task("t4", 600, 146, 130, 52, L("Ablehnung mit\nBegründung", "Rejection\nwith reason"), "mail")
    d.event("e1", 760, 380, "end")
    d.event("e2", 760, 60, "end", L("informiert", "informed"))
    d.edge("s", "t1", sa="r", sb="t")
    d.edge("t1", "t2", sa="r", sb="t")
    d.edge("t2", "g")
    d.edge("g", "t3", L("ja", "yes"), sa="b", sb="l")
    d.edge("t3", "e1")
    d.edge("g", "t4", L("nein", "no"), sa="t", sb="l")
    d.path([(665, 146), (665, 60), (744, 60)])
    return d, []

def s_comms(lang):
    L = T(lang)
    d = D(800, 300, L("BPMN: automatische Erinnerungsserie", "BPMN: automated reminder sequence"))
    d.lane(16, 16, 768, 268, "Power Automate")
    d.event("s", 80, 120, "timer", L("täglich", "daily"), "clock")
    d.task("t1", 120, 94, 140, 52, L("fällige Einträge\nfiltern", "filter due\nrecords"), "gear")
    d.gw("g", 310, 120, L("Stufe?", "step?"))
    d.task("m1", 380, 36, 130, 46, L("E-Mail 1:\nErinnerung", "Email 1:\nreminder"), "mail")
    d.task("m2", 380, 97, 130, 46, L("E-Mail 2:\nNachfassen", "Email 2:\nfollow-up"), "mail")
    d.task("m3", 380, 158, 130, 46, L("E-Mail 3:\nletzter Hinweis", "Email 3:\nfinal notice"), "mail")
    d.task("t2", 560, 94, 140, 52, L("Status in Liste\nfortschreiben", "update status\nin list"), "gear")
    d.event("e", 744, 120, "end")
    d.edge("s", "t1"); d.edge("t1", "g")
    for m in ("m1", "m2", "m3"):
        d.edge("g", m, sa="r", sb="l", lpos=.4); d.edge(m, "t2", sa="r", sb="l", lpos=.6)
    d.edge("t2", "e")
    d.box("n", 120, 222, 580, 44, L("Datenbasis: SharePoint-Liste mit einem Eintrag je Vertrag, Gerät oder Kunde", "Data source: SharePoint list with one entry per contract, device or customer"), ic="table", kind="soft")
    d.path([(190, 222), (190, 146)], dashed=True)
    d.path([(630, 146), (630, 222)], dashed=True)
    return d, []

def s_tracker(lang):
    L = T(lang)
    d = D(800, 330, L("Architektur: Aufgaben- und Besprechungs-Tracker", "Architecture: task and meeting tracker"))
    d.icon("u", 80, 150, L("Team", "Team"), L("Browser, Teams", "browser, Teams"), "users")
    d.zone("z", 170, 16, 614, 298, "Microsoft 365", "")
    d.box("app", 200, 120, 190, 64, "Power Apps", L("Übersicht, Kennzahlen,\nStatus", "overview, KPIs,\nstatus"), ic="app", kind="pri")
    d.box("lst", 470, 50, 280, 56, L("SharePoint-Liste", "SharePoint list"), L("Aufgaben, Verantwortliche, Fristen", "tasks, owners, due dates"), ic="table")
    d.box("pa", 470, 140, 280, 56, "Power Automate", L("Fälligkeit prüfen, Erinnern", "check due dates, remind"), ic="flow")
    d.box("tm", 470, 230, 130, 52, "Teams", ic="chat")
    d.box("ol", 620, 230, 130, 52, "Outlook", ic="mail")
    d.edge("u", "app", sa="r", sb="l")
    d.edge("app", "lst", L("lesen, schreiben", "read, write"), sa="r", sb="l", both=True)
    d.edge("lst", "pa", sa="b", sb="t"); d.edge("pa", "tm", sa="b", sb="t"); d.edge("pa", "ol", sa="b", sb="t")
    return d, []

def s_inbox(lang):
    L = T(lang)
    d = D(800, 260, L("BPMN: eingehende E-Mails Vorgängen zuordnen", "BPMN: assigning incoming emails to cases"))
    d.lane(16, 16, 768, 230, "Power Automate")
    d.event("s", 80, 100, "message", L("E-Mail im\nSammelpostfach", "Email in\nshared mailbox"), "mail")
    d.task("t1", 130, 74, 150, 52, L("Referenznummer\naus Betreff lesen", "Read reference\nfrom subject"), "gear")
    d.gw("g", 340, 100, L("gefunden?", "found?"), right=True)
    d.task("t2", 410, 40, 150, 46, L("Vorgang zuordnen,\nVerlauf speichern", "Assign to case,\nstore history"), "gear")
    d.task("t3", 590, 40, 120, 46, L("Team\ninformieren", "Notify\nteam"), "mail")
    d.task("t4", 410, 170, 150, 46, L("„Zu klären“\nmarkieren", "Flag\n“to clarify”"), "gear")
    d.event("e1", 750, 63, "end"); d.event("e2", 750, 193, "end")
    d.edge("s", "t1"); d.edge("t1", "g")
    d.edge("g", "t2", L("ja", "yes"), sa="t", sb="l"); d.edge("t2", "t3"); d.edge("t3", "e1")
    d.edge("g", "t4", L("nein", "no"), sa="b", sb="l"); d.edge("t4", "e2")
    return d, []

def s_data(lang):
    L = T(lang)
    d = D(800, 300, L("Datenfluss: Bereinigung und Migration", "Data flow: cleansing and migration"))
    d.zone("zq", 16, 16, 170, 268, L("Quellen", "Sources"))
    for i, (t, ic) in enumerate([(L("Excel-Datei A", "Excel file A"), "excel"), (L("Excel-Datei B", "Excel file B"), "excel"), ("CSV-Export", "doc")]):
        d.box(f"q{i}", 30, 50 + i * 76, 142, 52, t, ic=ic)
    d.zone("zp", 216, 16, 220, 268, "Power Query", "acc")
    for i, t in enumerate([L("zusammenführen", "append"), L("aufteilen, typisieren", "split, type"), L("Dubletten entfernen", "remove duplicates"), L("prüfen", "validate")]):
        d.box(f"p{i}", 232, 48 + i * 58, 188, 42, t, ic="funnel" if i == 2 else None, kind="soft")
        if i: d.edge(f"p{i-1}", f"p{i}", sa="b", sb="t")
    d.box("sp", 470, 116, 140, 64, L("SharePoint-\nListe", "SharePoint\nlist"), ic="table", kind="pri")
    d.zone("zn", 632, 16, 152, 268, L("Nutzung", "Usage"))
    for i, (t, ic) in enumerate([("Power Apps", "app"), ("Power Automate", "flow"), (L("Berichte", "Reports"), "chart")]):
        d.box(f"n{i}", 642, 50 + i * 76, 132, 52, t, ic=ic)
        d.edge("sp", f"n{i}", sa="r", sb="l", lpos=.5)
    for i in range(3): d.edge(f"q{i}", "zp", sa="r", sb="l")
    d.edge("zp", "sp")
    return d, []

def s_legacy(lang):
    L = T(lang)
    d = D(800, 330, L("Architektur: Anbindung eines Altsystems ohne Schnittstelle", "Architecture: connecting a legacy system without an API"))
    d.zone("zo", 16, 16, 330, 298, L("Lokal (On-Premises)", "On-premises"))
    d.box("app", 36, 60, 150, 64, L("Fachanwendung", "Business app"), L("ohne offene API", "no open API"), ic="desktopapp")
    d.box("rpa", 36, 200, 150, 64, "Power Automate\nDesktop", L("auf eigener VM", "on dedicated VM"), ic="robot", kind="pri")
    d.box("gw", 210, 200, 120, 64, L("Daten-\ngateway", "Data\ngateway"), ic="lock")
    d.edge("rpa", "app", L("Oberfläche bedienen", "drives the UI"), sa="t", sb="b")
    d.edge("rpa", "gw", both=True)
    d.zone("zc", 386, 16, 398, 298, "Microsoft 365", "acc")
    d.box("cf", 410, 200, 160, 64, L("Cloud-Flow", "Cloud flow"), L("startet, überwacht", "triggers, monitors"), ic="flow")
    d.box("sp", 600, 200, 160, 64, "SharePoint / Excel", L("Zielablage", "target store"), ic="table")
    d.box("crit", 410, 54, 350, 96, L("Prüfkriterien vor Freigabe", "Criteria before go-live"),
          L("Stabilität bei Updates, Fehlerbehandlung,\nLaufzeit, Pflegeaufwand, Lizenzbedarf", "stability on updates, error handling,\nrun time, maintenance, licensing"), ic="check", kind="soft")
    d.edge("gw", "cf", both=True); d.edge("cf", "sp")
    return d, []

def s_incident(lang):
    L = T(lang)
    d = D(800, 300, L("Ablauf bei einem Sicherheitsvorfall (angelehnt an NIST SP 800-61)", "Security incident response (based on NIST SP 800-61)"))
    ph = [(L("Erkennen", "Detect"), "search", [L("Warnungen prüfen", "review alerts"), L("Umfang abschätzen", "assess scope")]),
          (L("Eindämmen", "Contain"), "lock", [L("Konten sperren", "lock accounts"), L("Zugänge kappen", "cut access")]),
          (L("Analysieren", "Analyse"), "doc", [L("Protokolle sichern", "preserve logs"), L("Ursache finden", "find root cause")]),
          (L("Beseitigen", "Eradicate"), "shield", [L("Passwörter, MFA", "passwords, MFA"), L("Lücken schließen", "close gaps")]),
          (L("Nachbereiten", "Lessons learned"), "book", [L("Bericht an Leitung", "report to mgmt"), L("Maßnahmenplan", "action plan")])]
    for i, (t, ic, items) in enumerate(ph):
        x = 16 + i * 156
        d.box(f"p{i}", x, 30, 140, 60, t, ic=ic, kind="pri" if i == 1 else "")
        for j, it in enumerate(items):
            d.box(f"p{i}{j}", x, 120 + j * 46, 140, 36, it, kind="soft", center=True)
        d.path([(x + 70, 90), (x + 70, 120)], arrow=False, dashed=True)
        if i: d.edge(f"p{i-1}", f"p{i}")
    d.path([(710, 220), (710, 260), (86, 260), (86, 220)], L("Erkenntnisse fließen in die Prävention", "Findings feed back into prevention"))
    return d, []

def s_docs(lang):
    L = T(lang)
    d = D(800, 340, L("Struktur einer IT-Dokumentation", "Structure of IT documentation"))
    d.box("root", 300, 16, 200, 56, L("IT-Betriebshandbuch", "IT operations manual"), ic="book", kind="pri")
    br = [(L("Infrastruktur", "Infrastructure"), "server", [L("Netzwerkplan", "Network diagram"), L("Systeminventar", "System inventory"), L("Zugangsdaten-Tresor", "Credential vault")]),
          (L("Sicherheit", "Security"), "shield", [L("Berechtigungskonzept", "Access concept"), L("Backup-Konzept", "Backup concept"), L("Notfallhandbuch", "Emergency manual")]),
          (L("Betrieb", "Operations"), "gear", [L("Arbeitsanweisungen (SOP)", "Procedures (SOP)"), L("Checklisten", "Checklists"), L("Änderungsprotokoll", "Change log")]),
          (L("Menschen", "People"), "users", [L("Onboarding", "Onboarding"), L("Schulungen", "Training"), L("Ansprechpartner", "Contacts")])]
    for i, (t, ic, items) in enumerate(br):
        x = 16 + i * 196
        d.box(f"b{i}", x, 116, 180, 50, t, ic=ic, kind="acc")
        d.edge("root", f"b{i}", sa="b", sb="t", lpos=.5)
        for j, it in enumerate(items):
            yy = 190 + j * 46
            d.box(f"b{i}{j}", x + 22, yy, 158, 36, it, kind="soft")
            d.path([(x + 11, 166), (x + 11, yy + 18), (x + 22, yy + 18)], arrow=False)
    return d, []

# =================================================================== ABOUT / CERTS / CONTACT
def competence(lang):
    L = T(lang)
    d = D(800, 360, L("Kompetenzprofil", "Competence profile"))
    d.box("c", 300, 150, 200, 60, "Hashmat Bahadari", L("IT & Digitale Automatisierung", "IT & Digital Automation"), kind="pri", center=True)
    items = [(16, 30, L("Informationssicherheit", "Information security"), "ISO 27001, CEH", "shield"),
             (16, 150, "Microsoft 365 & Azure", "AZ-500, SC-900, AZ-900", "cloud"),
             (16, 270, L("Netzwerk & Infrastruktur", "Network & infrastructure"), "Fortinet, Windows Server", "switch"),
             (564, 30, "Power Platform", "Automate, Apps, Forms", "flow"),
             (564, 150, L("Intranet & Wissen", "Intranet & knowledge"), "SharePoint", "book"),
             (564, 270, L("Sprachen", "Languages"), L("Deutsch, Englisch, Persisch", "German, English, Persian"), "chat")]
    for i, (x, y, t, s, ic) in enumerate(items):
        d.box(f"i{i}", x, y, 220, 60, t, s, ic=ic)
        d.edge("c", f"i{i}", sa="l" if x < 300 else "r", sb="r" if x < 300 else "l")
    return d, []

def cert_map(lang):
    L = T(lang)
    d = D(800, 330, L("Zertifizierungen und Leistungsbereiche", "Certifications and service areas"))
    cs = [(L("Sicherheit & Audit", "Security & audit"), "ISO 27001, CEH, IAM", "shield"),
          ("Microsoft & Azure", "AZ-500, SC-900, AZ-900, MCITP", "cloud"),
          (L("Netzwerk & Grundlagen", "Networking & foundations"), "Security+, Network+, NSE", "switch")]
    for i, (t, s, ic) in enumerate(cs):
        d.box(f"c{i}", 16, 30 + i * 100, 270, 64, t, s, ic=ic, kind="acc")
    sv = [(L("Systemadministration", "System administration"), "server"), ("Microsoft Cloud", "cloud"), (L("Automatisierung", "Automation"), "flow"), (L("Intranet & Dokumentation", "Intranet & documentation"), "book")]
    for i, (t, ic) in enumerate(sv):
        d.box(f"s{i}", 514, 20 + i * 78, 270, 54, t, ic=ic)
    links = [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 0)]
    for a, b in links:
        d.curve(f"c{a}", f"s{b}")
    return d, []

def contact_flow(lang):
    L = T(lang)
    d = D(800, 150, L("Ablauf einer Anfrage", "How an enquiry works"))
    st = [(L("Kontakt", "Contact"), L("Termin oder E-Mail", "booking or email"), "mail"), (L("Erstgespräch", "Intro call"), L("30 Min., kostenlos", "30 min, free"), "chat"),
          (L("Angebot", "Proposal"), L("schriftlich", "in writing"), "doc"), (L("Umsetzung", "Delivery"), L("in Etappen", "in stages"), "gear"),
          (L("Betreuung", "Support"), L("nach Bedarf", "as needed"), "users")]
    for i, (t, s, ic) in enumerate(st):
        d.box(f"s{i}", 16 + i * 156, 40, 140, 64, t, s, ic=ic, kind="pri" if i == 0 else "")
        if i: d.edge(f"s{i-1}", f"s{i}")
    return d, []
