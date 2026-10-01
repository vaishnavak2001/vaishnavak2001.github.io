import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const base = process.env.PORTFOLIO_URL || 'http://127.0.0.1:4178';
const identity = await fetch(base);
assert.equal(identity.headers.get('x-portfolio-preview'), 'vaishnav-ak', 'The target is not this portfolio preview. Stop before capturing or interacting.');
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const errors = [];
const report = [];
fs.mkdirSync('local_scratch/screenshots', { recursive: true });
try {
  for (const [name, viewport] of Object.entries({ desktop: { width: 1440, height: 1000 }, mobile: { width: 390, height: 844 } })) {
    const context = await browser.newContext({ viewport, reducedMotion: 'reduce' });
    const page = await context.newPage();
    page.on('pageerror', error => errors.push(`${name}: ${error.message}`));
    page.on('response', response => { if (response.status() >= 400 && response.url().startsWith(base)) errors.push(`${name}: ${response.status()} ${response.url()}`); });
    for (const route of ['/', '/work/', '/work/support-agent/', '/lab/', '/about/', '/resume/', '/404.html']) {
      await page.goto(base + route);
      await page.evaluate(() => document.fonts.ready);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
      assert.equal(overflow, false, `${name} ${route}: horizontal overflow`);
      const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
      report.push({ viewport: name, route, violations: results.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target) })) });
      const serious = results.violations.filter(v => ['serious', 'critical'].includes(v.impact));
      errors.push(...serious.map(v => `${name} ${route}: ${v.id} ${JSON.stringify(v.nodes.map(n => n.target))}`));
      if (['/', '/work/', '/lab/', '/about/', '/resume/'].includes(route)) await page.screenshot({ path: `local_scratch/screenshots/${name}-${route === '/' ? 'home' : route.replaceAll('/', '')}.png`, fullPage: true });
      if (route === '/') await page.screenshot({ path: `local_scratch/screenshots/${name}-hero.png` });
    }
    await page.goto(base + '/');
    await page.getByRole('button', { name: 'Data', exact: true }).click();
    await page.waitForFunction(() => document.querySelector('[data-scene-description]').textContent.includes('Raw signals'));
    assert.equal(await page.getByRole('button', { name: 'Data', exact: true }).getAttribute('aria-pressed'), 'true');
    assert.equal(await page.locator('[data-motion-toggle]').getAttribute('aria-label'), 'Play animation');
    if (name === 'mobile') {
      await page.getByRole('button', { name: 'Menu' }).click();
      assert.equal(await page.locator('#navigation').isVisible(), true);
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('#navigation').isVisible(), false);
    }
    await page.goto(base + '/work/');
    await page.getByRole('button', { name: 'Personal', exact: true }).click();
    assert.equal(await page.locator('.work-item:visible').count(), 2);
    await page.getByRole('button', { name: 'All work' }).click();
    assert.equal(await page.locator('.work-item:visible').count(), 9);
    await page.goto(base + '/lab/#support');
    const support = page.locator('#support');
    for (let i = 0; i < 4; i++) await support.getByRole('button', { name: 'Next step' }).click();
    assert.equal(await support.getByRole('button', { name: 'Next step' }).isDisabled(), true);
    assert.equal(await support.locator('.step-count').textContent(), 'Step 5 of 5');
    await support.getByRole('button', { name: 'Replay' }).click();
    assert.equal(await support.locator('.step-count').textContent(), 'Step 1 of 5');
    await page.goto(base + '/resume/');
    const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('link', { name: 'Download résumé' }).click()]);
    assert.equal(download.suggestedFilename(), 'Vaishnav_AK_Resume.pdf');
    await context.close();
  }
  const noJS = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
  const page = await noJS.newPage();
  await page.goto(base + '/');
  assert.equal(await page.locator('#navigation').isVisible(), true);
  assert.equal(await page.locator('.scene-fallback').isVisible(), true);
  await page.goto(base + '/lab/');
  assert.equal(await page.locator('.static-steps[open]').count(), 4);
  assert.equal(await page.locator('.static-steps li:visible').count(), 20);
  await noJS.close();
  fs.writeFileSync('local_scratch/browser-report.json', JSON.stringify({ errors, report }, null, 2));
  assert.deepEqual(errors, [], errors.join('\n'));
  console.log('Desktop, mobile, accessibility, navigation, filters, walkthroughs, reduced motion, PDF download, and no-JS checks passed.');
} finally { await browser.close(); }
