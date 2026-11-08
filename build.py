#!/usr/bin/env python3
"""Build the CV page: cv.md -> dist/index.html (one file, CSS inlined).

cv.md must start with three things, in this order:
    # Full Name
    **Job Title**
    location · email · github.com/user · linkedin.com/in/user
Everything after that is normal Markdown (## sections, ### roles, - bullets).

Run:   python3 build.py        (needs the `Markdown` package, see requirements.txt)
View:  cd dist && python3 -m http.server 8000   then open http://localhost:8000
If Julio-Gema-CV.pdf exists in this folder, it is copied to dist/ and linked from the header.
"""

import html
import json
import os
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
SITE_URL = os.environ.get("SITE_URL", "https://juliogema.github.io/cv/")
PDF_NAME = "Julio-Gema-CV.pdf"


def contact_items(line):
    items, links, email = [], [], None
    for part in (p.strip() for p in line.split("·") if p.strip()):
        safe = html.escape(part)
        if "@" in part:
            email = part
            items.append(f'<li><a href="mailto:{safe}">{safe}</a></li>')
        elif part.startswith(("github.com/", "linkedin.com/")):
            links.append(f"https://{part}")
            items.append(f'<li><a href="https://{safe}">{safe}</a></li>')
        else:
            items.append(f"<li>{safe}</li>")
    return items, links, email


def short_description(rest):
    match = re.search(r"## Summary\s+(.+?)(?:\n\n|\Z)", rest, re.S)
    text = " ".join(match.group(1).split()) if match else ""
    if len(text) > 200:
        text = text[:200].rsplit(" ", 1)[0] + "..."
    return text


def main():
    text = (ROOT / "cv.md").read_text(encoding="utf-8")
    match = re.match(r"\s*# (.+?)\n+\*\*(.+?)\*\*\n+(.+?)\n+(.*)$", text, re.S)
    if not match:
        raise SystemExit("cv.md must start with '# Name', '**Title**' and a contact line")
    name, title, contact, rest = (g.strip() for g in match.groups())

    body = markdown.markdown(rest, extensions=["sane_lists"])
    # A paragraph that is only bold text is a sub-heading (for example a group of bullets).
    body = re.sub(r"<p><strong>([^<]+)</strong></p>", r"<h4>\1</h4>", body)
    # The line right under a role heading holds the dates.
    body = re.sub(r"(</h3>\s*)<p>", r'\1<p class="meta">', body)

    items, links, email = contact_items(contact)
    DIST.mkdir(exist_ok=True)
    if (ROOT / PDF_NAME).exists():
        shutil.copy2(ROOT / PDF_NAME, DIST / PDF_NAME)
        items.append(f'<li><a href="{PDF_NAME}">PDF</a></li>')

    description = short_description(rest)
    person = {"@context": "https://schema.org", "@type": "Person", "name": name, "jobTitle": title, "url": SITE_URL}
    if email:
        person["email"] = email
    if links:
        person["sameAs"] = links
    jsonld = json.dumps(person, ensure_ascii=False).replace("</", "<\\/")

    page = (ROOT / "theme" / "template.html").read_text(encoding="utf-8")
    values = {
        "name": html.escape(name),
        "title": html.escape(title),
        "description": html.escape(description, quote=True),
        "url": html.escape(SITE_URL, quote=True),
        "jsonld": jsonld,
        "style": (ROOT / "theme" / "style.css").read_text(encoding="utf-8"),
        "contact": "\n".join(items),
        "body": body,
    }
    for key, value in values.items():
        page = page.replace("{{" + key + "}}", value)
    (DIST / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {DIST / 'index.html'} ({len(page) // 1024} KB)")


if __name__ == "__main__":
    main()
