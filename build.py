#!/usr/bin/env python3
"""Build the CV page: cv.md -> build/resume.json -> dist/index.html.

cv.md must start with three things, in this order:
    # Full Name
    **Job Title**
    location · email · github.com/user · linkedin.com/in/user
then ## Summary, ## Skills (- **Group:** a, b), ## Experience (### Role, Company
then a "Month YYYY to Present · Place" line, a one-line summary, and - bullets),
## Education, and optionally ## Languages and ## Interests (- **Name:** a, b).

The page is rendered by the JSON Resume theme clinical-precision (see package.json).
Run:   npm ci && python3 build.py
View:  cd dist && python3 -m http.server 8000   then open http://localhost:8000
If Julio-Gema-CV.pdf exists in this folder, it is copied to dist/.
"""

import html
import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"
SITE_URL = os.environ.get("SITE_URL", "https://juliogema.github.io/cv/")
PDF_NAME = "Julio-Gema-CV.pdf"
THEME = "clinical-precision"


def month(text):
    if text.strip().lower() == "present":
        return None
    return datetime.strptime(text.strip(), "%B %Y").strftime("%Y-%m")


def to_resume(text):
    m = re.match(r"\s*# (.+?)\n+\*\*(.+?)\*\*\n+(.+?)\n+(.*)$", text, re.S)
    if not m:
        raise SystemExit("cv.md must start with '# Name', '**Title**' and a contact line")
    name, title, contact, rest = (g.strip() for g in m.groups())

    location, email, profiles = "", "", []
    for part in (p.strip() for p in contact.split("·") if p.strip()):
        if "@" in part:
            email = part
        elif part.startswith("github.com/"):
            profiles.append({"network": "GitHub", "username": part.split("/", 1)[1], "url": f"https://{part}"})
        elif part.startswith("linkedin.com/"):
            profiles.append({"network": "LinkedIn", "username": part.rstrip("/").split("/")[-1], "url": f"https://www.{part}"})
        else:
            location = part

    sections = {h: b.strip() for h, b in re.findall(r"## (.+?)\n(.*?)(?=\n## |\Z)", rest, re.S)}

    skills = []
    for line in sections["Skills"].splitlines():
        s = re.match(r"- \*\*(.+?):\*\* (.+)", line)
        if s:
            # split on commas that are not inside parentheses
            skills.append({"name": s[1], "keywords": re.split(r",\s*(?![^()]*\))", s[2])})

    languages = [{"language": m[1], "fluency": m[2]}
                 for m in re.finditer(r"- \*\*(.+?):\*\* (.+)", sections.get("Languages", ""))]
    interests = [{"name": m[1], "keywords": re.split(r",\s*", m[2])}
                 for m in re.finditer(r"- \*\*(.+?):\*\* (.+)", sections.get("Interests", ""))]

    work = []
    for block in re.split(r"(?m)^### ", sections["Experience"])[1:]:
        head, dates, summary, bullets = re.match(r"(.+?)\n\n(.+?)\n\n(.+?)\n\n(.*)", block, re.S).groups()
        position, company = head.split(", ", 1)
        span, _, place = dates.partition(" · ")
        start, end = span.split(" to ")
        entry = {"name": company, "position": position, "location": place, "summary": summary,
                 "startDate": month(start), "highlights": [
                     re.sub(r"\*\*(.+?)\*\*", r"\1", b) for b in re.findall(r"(?m)^- (.+)$", bullets)]}
        if month(end):
            entry["endDate"] = month(end)
        work.append(entry)

    edu = re.match(r"(.+?) in (.+?), (.+), (\d{4})", sections["Education"])
    degree, area, school, year = edu.groups()
    return {
        "basics": {"name": name, "label": title, "email": email, "location": {"region": location},
                   "summary": sections["Summary"], "profiles": profiles},
        "work": work,
        "education": [{"institution": school, "area": area, "studyType": degree, "endDate": year}],
        "skills": skills,
        "languages": languages,
        "interests": interests,
        "meta": {"theme": THEME},
    }


def head_extras(resume):
    basics = resume["basics"]
    summary = " ".join(basics["summary"].split())
    description = summary if len(summary) <= 200 else summary[:200].rsplit(" ", 1)[0] + "..."
    person = {"@context": "https://schema.org", "@type": "Person", "name": basics["name"],
              "jobTitle": basics["label"], "url": SITE_URL, "email": basics["email"],
              "sameAs": [p["url"] for p in basics["profiles"]]}
    jsonld = json.dumps(person, ensure_ascii=False).replace("</", "<\\/")
    title = html.escape(f"{basics['name']} | {basics['label']}", quote=True)
    desc = html.escape(description, quote=True)
    url = html.escape(SITE_URL, quote=True)
    return (f'<meta name="description" content="{desc}">\n<link rel="canonical" href="{url}">\n'
            f'<meta property="og:type" content="profile">\n<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{url}">\n'
            f'<script type="application/ld+json">{jsonld}</script>\n')


def main():
    resume = to_resume((ROOT / "cv.md").read_text(encoding="utf-8"))
    BUILD.mkdir(exist_ok=True)
    DIST.mkdir(exist_ok=True)
    (BUILD / "resume.json").write_text(json.dumps(resume, indent=2, ensure_ascii=False), encoding="utf-8")

    page = subprocess.run(["node", "render.mjs", str(BUILD / "resume.json")], cwd=ROOT,
                          check=True, capture_output=True, text=True).stdout
    page = page.replace("</head>", head_extras(resume) + "</head>", 1)
    (DIST / "index.html").write_text(page, encoding="utf-8")
    if (ROOT / PDF_NAME).exists():
        shutil.copy2(ROOT / PDF_NAME, DIST / PDF_NAME)
    print(f"wrote {DIST / 'index.html'} ({len(page) // 1024} KB)")


if __name__ == "__main__":
    main()
