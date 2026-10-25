def imprint_page(lang):
    key = "imprint"
    phone = f"<br>Telefon: {e(C['phone'])}" if C["phone"] else ""
    vat_de = f"<h2>Umsatzsteuer-ID</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: {e(C['vat_id'])}</p>" if C["vat_id"] else ""
    addr = f'{e(C["legal_name"])}<br>{e(C["street"])}<br>{e(C["city"])}<br>Deutschland'
    if lang == "de":
        h1, lead = "Impressum", "Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)"
        txt = f'''<h2>Anbieter</h2><p>{addr}</p>
<h2>Kontakt</h2><p>E-Mail: <a href="mailto:{C["email"]}">{e(C["email"])}</a>{phone}<br>Website: <a href="{C["base_url"]}">{e(C["website"])}</a></p>
{vat_de}
<h2>Verantwortlich für den Inhalt</h2><p>Verantwortlich nach § 18 Abs. 2 MStV:<br>{addr}</p>
<h2>Haftung für Inhalte</h2><p>Die Inhalte dieser Seiten wurden mit Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte kann ich jedoch keine Gewähr übernehmen. Als Diensteanbieter bin ich für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich.</p>
<h2>Haftung für Links</h2><p>Diese Website enthält Links zu externen Websites Dritter, auf deren Inhalte ich keinen Einfluss habe. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter verantwortlich. Bei Bekanntwerden von Rechtsverletzungen entferne ich derartige Links umgehend.</p>
<h2>Urheberrecht</h2><p>Die Inhalte und Grafiken dieser Website unterliegen dem deutschen Urheberrecht. Vervielfältigung und Verwendung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung. Produktnamen wie Microsoft 365, Azure oder Trello sind Marken ihrer jeweiligen Inhaber.</p>
<h2>Verbraucherstreitbeilegung</h2><p>Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>'''
    else:
        h1, lead = "Legal notice", "Information pursuant to Section 5 of the German Digital Services Act (DDG). The German version is legally binding."
        txt = f'''<h2>Provider</h2><p>{addr.replace("Deutschland", "Germany")}</p>
<h2>Contact</h2><p>Email: <a href="mailto:{C["email"]}">{e(C["email"])}</a>{phone.replace("Telefon", "Phone")}<br>Website: <a href="{C["base_url"]}">{e(C["website"])}</a></p>
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

