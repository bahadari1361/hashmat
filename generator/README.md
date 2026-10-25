# Generator (keep locally – do not upload to the website repository)
content.py  – all text and contact data (CONFIG: address, phone, VAT ID for the Impressum)
diagrams.py – all diagrams (BPMN, reference architectures, network topology)
build.py    – page templates;  legal.py – Impressum / Datenschutz

Rebuild:  OUT=../website python3 build.py
