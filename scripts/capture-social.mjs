import { chromium } from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const url = 'http://127.0.0.1:4178/';
const identity = await fetch(url);
assert.equal(identity.headers.get('x-portfolio-preview'), 'vaishnav-ak');
const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, reducedMotion: 'reduce', deviceScaleFactor: 1 });
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({ content: '.site-header{height:80px}.hero{min-height:550px;height:550px;padding-top:28px}.hero h1{font-size:80px}.hero-intro{margin-top:26px}.hero-bottom{display:none}.hero-links{margin-top:18px}.scene-description{bottom:10px}.scene-shell{bottom:5px}.motion-toggle{display:none}' });
  await page.screenshot({ path: 'assets/images/social-preview.png' });
  await fs.copyFile('assets/images/social-preview.png', '_site/assets/images/social-preview.png');
  console.log('Created 1200×630 social preview from the actual portfolio.');
} finally { await browser.close(); }
