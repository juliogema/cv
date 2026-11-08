# Julio Gema

Software engineer working in Go on cloud backend services: usage-based billing and metering, login-capacity controls, audit logging and data migrations.

## CV

- Web page: [juliogema.github.io/cv](https://juliogema.github.io/cv/)
- Source text: [cv.md](cv.md)

## About this project

This repository holds my CV as a single Markdown file and builds it into a web page that is published with GitHub Pages. I edit only `cv.md`; the page is generated from it.

The page is rendered with the [JSON Resume](https://jsonresume.org) theme [clinical-precision](https://www.npmjs.com/package/jsonresume-theme-clinical-precision).

### How it works

```
cv.md  ->  build/resume.json  ->  dist/index.html  ->  GitHub Pages
        (build.py)          (render.mjs + theme)    (workflow)
```

1. [build.py](build.py) reads `cv.md` and converts it to a JSON Resume file, `build/resume.json`.
2. [render.mjs](render.mjs) renders that file with the theme (a React and styled-components theme, so it runs on Node).
3. `build.py` adds a meta description, a canonical link, social tags and JSON-LD to the page head, and writes `dist/index.html`.
4. The GitHub Actions workflow in [.github/workflows/pages.yml](.github/workflows/pages.yml) runs the build and deploys `dist/` on every push to `main`.

### Files

| File | Purpose |
| --- | --- |
| `cv.md` | The CV content. The only file to edit for content changes. |
| `build.py` | Converts `cv.md` to JSON Resume, calls the renderer, adds the head tags. |
| `render.mjs` | Renders the JSON Resume file with the theme. |
| `package.json`, `package-lock.json` | Pin the theme, React and React DOM versions. |
| `.github/workflows/pages.yml` | Builds and deploys to GitHub Pages. |

### Format of `cv.md`

The converter expects this structure:

```markdown
# Full Name

**Job Title**

Location · email · github.com/user · linkedin.com/in/user

## Summary
## Skills        (- **Group:** item, item, ...)
## Experience    (### Role, Company, then "Month YYYY to Present · Place",
                  a one-line summary and - bullets)
## Education     (Degree in Area, School, Year)
## Languages     (optional, - **Language:** Level)
## Interests     (optional, - **Topic:** item, item, ...)
```

Notes:

- JSON Resume has one flat bullet list per job, so bold sub-headings inside a role (for example "Billing and metering") are not shown on the page.
- The page is written for the `SITE_URL` environment variable, which defaults to `https://juliogema.github.io/cv/`.

### Build and preview locally

Requires Node 22 and Python 3.

```bash
npm ci
python3 build.py
cd dist && python3 -m http.server 8000   # then open http://localhost:8000
```

If a file named `Julio-Gema-CV.pdf` exists in the repository root, `build.py` copies it to `dist/`. The page does not link to it.

### Deploy

Push to `main`. The workflow builds the page and publishes it. GitHub Pages must be set to deploy from **GitHub Actions** in the repository settings.

### Changing the theme

Change `THEME` in `build.py` and install the matching `jsonresume-theme-*` package with npm. Update the import in `render.mjs` to match.

## Contact

- Email: juliogema.personal@gmail.com
- LinkedIn: [linkedin.com/in/juliogema](https://www.linkedin.com/in/juliogema)
- GitHub: [github.com/juliogema](https://github.com/juliogema)
