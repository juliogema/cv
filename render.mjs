// Renders build/resume.json with the clinical-precision theme to stdout.
import fs from "node:fs";
import { render } from "jsonresume-theme-clinical-precision";

const resume = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
process.stdout.write(await render(resume));
