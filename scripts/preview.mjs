// Local preview of this repository's Jekyll/Liquid subset, for machines without Ruby.
// Production remains Jekyll. This helper does not deploy or replace the Jekyll build.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { Liquid } from 'liquidjs';
import YAML from 'yaml';

const root = process.cwd();
const output = path.join(root, '_site');
const config = YAML.parse(await fs.readFile('_config.yml', 'utf8'));
const site = { ...config, data: {} };
for (const name of await fs.readdir('_data')) if (name.endsWith('.json')) site.data[name.slice(0, -5)] = JSON.parse(await fs.readFile(path.join('_data', name), 'utf8'));
const liquid = new Liquid({ root: ['_layouts', '_includes'], extname: '.html', jekyllInclude: true });
liquid.registerFilter('relative_url', url => (site.baseurl || '') + '/' + String(url).replace(/^\//, ''));
liquid.registerFilter('absolute_url', url => site.url + (site.baseurl || '') + '/' + String(url).replace(/^\//, ''));
function parse(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  return match ? { data: YAML.parse(match[1]) || {}, body: text.slice(match[0].length) } : { data: {}, body: text };
}
async function renderLayout(name, content, page) {
  const template = parse(await fs.readFile(path.join('_layouts', name + '.html'), 'utf8'));
  const rendered = await liquid.parseAndRender(template.body, { site, page, content });
  return template.data.layout ? renderLayout(template.data.layout, rendered, page) : rendered;
}
if (!process.argv.includes('--serve-only')) {
await fs.mkdir(output, { recursive: true });
for (const dir of ['assets', 'images', 'resume']) await fs.cp(path.join(root, dir), path.join(output, dir), { recursive: true });
const files = (await fs.readdir(root)).filter(f => f.endsWith('.html'));
for (const name of await fs.readdir('_work')) if (name.endsWith('.md')) files.push('_work/' + name);
for (const file of files) {
  const parsed = parse(await fs.readFile(file, 'utf8'));
  const isWork = file.startsWith('_work/');
  const url = parsed.data.permalink || (isWork ? `/work/${path.basename(file, '.md')}/` : file === 'index.html' ? '/' : '/' + file);
  const page = { ...(isWork ? { layout: 'case-study' } : {}), ...parsed.data, url };
  let content = await liquid.parseAndRender(parsed.body, { site, page });
  if (page.layout) content = await renderLayout(page.layout, content, page);
  const destination = path.join(output, url.endsWith('/') ? url + 'index.html' : url);
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.writeFile(destination, content);
}
console.log(`Local Liquid preview rendered ${files.length} pages to _site (production build uses Jekyll).`);
}
if (process.argv.includes('--serve') || process.argv.includes('--serve-only')) {
  const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.pdf': 'application/pdf', '.woff2': 'font/woff2' };
  http.createServer(async (req, res) => {
    res.setHeader('X-Portfolio-Preview', 'vaishnav-ak');
    try {
      const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
      let file = path.resolve(output, '.' + pathname);
      if (!file.startsWith(output + path.sep) && file !== output) { res.writeHead(403); return res.end(); }
      if ((await fs.stat(file)).isDirectory()) file = path.join(file, 'index.html');
      res.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
      res.end(await fs.readFile(file));
    } catch {
      res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(await fs.readFile(path.join(output, '404.html')));
    }
  }).listen(4178, '127.0.0.1', () => console.log('Preview: http://127.0.0.1:4178/'));
}
