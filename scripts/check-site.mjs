import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';

const root = path.resolve('_site');
assert.ok(fs.existsSync(root), 'Run the Jekyll build first.');
function walk(dir) { return fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]); }
const html = walk(root).filter(f => f.endsWith('.html'));
const failures = [];
for (const file of html) {
  const source = fs.readFileSync(file, 'utf8');
  const rel = path.relative(root, file);
  if (/\{%|\{\{/.test(source)) failures.push(`${rel}: unrendered Liquid`);
  if (!/<h1[\s>]/.test(source)) failures.push(`${rel}: missing h1`);
  if (!/name="description"/.test(source)) failures.push(`${rel}: missing description`);
  for (const match of source.matchAll(/\b(?:href|src|data)="([^"\s]+)"/g)) {
    const url = match[1].replaceAll('&amp;', '&');
    if (/^(https?:|mailto:|tel:|data:)/.test(url)) continue;
    const [pathname, fragment] = url.split('#');
    const target = pathname ? path.resolve(pathname.startsWith('/') ? root : path.dirname(file), '.' + (pathname.startsWith('/') ? pathname : '/' + pathname)) : file;
    const candidates = [target, path.join(target, 'index.html')];
    const found = candidates.find(p => fs.existsSync(p) && fs.statSync(p).isFile());
    if (!found) { failures.push(`${rel}: missing ${url}`); continue; }
    if (fragment && found.endsWith('.html') && !fs.readFileSync(found, 'utf8').includes(`id="${fragment}"`)) failures.push(`${rel}: missing fragment ${url}`);
  }
}
const projects = JSON.parse(fs.readFileSync('_data/case_studies.json', 'utf8'));
for (const project of projects) {
  const page = path.join(root, 'work', project.slug, 'index.html');
  assert.ok(fs.existsSync(page), `Missing case study: ${project.slug}`);
  const source = fs.readFileSync(page, 'utf8');
  if (!source.includes(project.evidence_note)) failures.push(`${project.slug}: evidence qualification missing`);
  if (project.kind === 'Company' && !source.includes('Contributing AI engineer')) failures.push(`${project.slug}: attribution missing`);
}
assert.deepEqual(failures, [], failures.join('\n'));
const repositories = JSON.parse(fs.readFileSync('_data/repositories.json', 'utf8'));
const workPage = fs.readFileSync(path.join(root, 'work', 'index.html'), 'utf8');
assert.equal(new Set(repositories.map(p => p.repo)).size, repositories.length, 'Duplicate repository entries');
for (const repository of repositories) {
  assert.equal(repository.github, `https://github.com/vaishnavak2001/${repository.repo}`);
  assert.ok(workPage.includes(`href="${repository.github}"`), `Repository missing from Work: ${repository.repo}`);
  if (repository.case_study) assert.ok(projects.some(p => p.slug === repository.case_study), `Missing linked case study: ${repository.repo}`);
}
console.log(`Checked ${html.length} HTML pages, local asset/link targets, case-study attribution, and evidence notes.`);
console.log(`Verified ${repositories.length} unique public repository entries and their case-study links.`);
