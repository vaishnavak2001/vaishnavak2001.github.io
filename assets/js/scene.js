/* A local, procedural point sculpture. No data or requests leave the browser. */
(() => {
  'use strict';
  const shell = document.querySelector('[data-scene]');
  if (!shell) return;
  const canvas = shell.querySelector('canvas');
  const ctx = canvas.getContext('2d', { alpha: true });
  const controls = [...shell.querySelectorAll('[data-shape]')];
  shell.querySelector('.scene-controls').hidden = false;
  const description = shell.querySelector('[data-scene-description]');
  const link = shell.querySelector('[data-scene-link]');
  const pause = shell.querySelector('[data-motion-toggle]');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const base = link.getAttribute('href').split('/work/')[0];
  const states = {
    data: { text: 'Raw signals. Structured into something useful.', path: 'cloud-data-pipeline' },
    prediction: { text: 'Learning from patterns. Anticipating demand.', path: 'demand-forecasting' },
    agent: { text: 'Reasoning with context. Acting through tools.', path: 'support-agent' },
    action: { text: 'From a question to a grounded next step.', path: 'client-analytics' }
  };
  let mode = 'agent', paused = reduce.matches, visible = true;
  let width = 1, height = 1, time = 0, last = 0, frame = 0;
  let pointerX = 0, pointerY = 0, tiltX = 0, tiltY = 0;
  const count = matchMedia('(max-width: 760px)').matches ? 3200 : 7200;
  const points = Array.from({ length: count }, (_, i) => ({ i, x: 0, y: 0, z: 0 }));
  const TAU = Math.PI * 2;
  function target(i, shape) {
    const u = (i % 100) / 100 * TAU;
    const v = Math.floor(i / 100) / Math.ceil(count / 100) * TAU;
    if (shape === 'agent') {
      const r = 1.05 + .38 * Math.cos(v + u * 2);
      return [r * Math.cos(u), r * Math.sin(u), .44 * Math.sin(v + u * 2)];
    }
    if (shape === 'data') {
      const a = i % 16, b = Math.floor(i / 16) % 12, c = Math.floor(i / 192);
      return [(a - 7.5) * .17, (b - 5.5) * .17, (c - Math.floor(count / 192) / 2) * .15];
    }
    if (shape === 'prediction') {
      const y = 1 - 2 * (i + .5) / count;
      const r = Math.sqrt(1 - y * y);
      const a = i * 2.3999632297;
      const wave = 1 + .09 * Math.sin(a * 3 + y * 9);
      return [Math.cos(a) * r * wave * 1.22, y * 1.22, Math.sin(a) * r * wave * 1.22];
    }
    const t = (i % 100) / 99;
    const lane = Math.floor(i / 100) / Math.ceil(count / 100) - .5;
    return [(t - .5) * 2.9, Math.sin(t * TAU * 1.25 + lane * 1.8) * .6 + lane * .75, lane * 1.4 + Math.cos(t * TAU) * .2];
  }
  let targets = points.map(p => target(p.i, mode));
  for (const p of points) [p.x, p.y, p.z] = targets[p.i];
  function updatePause() {
    pause.setAttribute('aria-label', paused ? 'Play animation' : 'Pause animation');
    pause.innerHTML = paused
      ? '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="m9 6 9 6-9 6Z" fill="currentColor"/></svg>'
      : '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6v12M15 6v12" stroke="currentColor" stroke-width="2"/></svg>';
  }
  function project(x, y, z) {
    const ry = .34 + time * .085 + tiltX;
    const rx = -.62 + tiltY;
    const x1 = x * Math.cos(ry) + z * Math.sin(ry);
    const z1 = z * Math.cos(ry) - x * Math.sin(ry);
    const y1 = y * Math.cos(rx) - z1 * Math.sin(rx);
    const z2 = y * Math.sin(rx) + z1 * Math.cos(rx);
    const roll = -.42;
    const xx = x1 * Math.cos(roll) - y1 * Math.sin(roll);
    const yy = x1 * Math.sin(roll) + y1 * Math.cos(roll);
    const scale = Math.min(width * .235, height * .265) * (3.8 / (3.8 + z2));
    return [width * .51 + xx * scale, height * .45 + yy * scale, z2];
  }
  function draw(immediate = false) {
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);
    tiltX += (pointerX * .28 - tiltX) * .05;
    tiltY += (pointerY * .18 - tiltY) * .05;
    // A sparse orbit gives the sculpture a stable spatial reference.
    ctx.beginPath();
    for (let i = 0; i <= 120; i++) {
      const a = i / 120 * TAU;
      const q = project(Math.cos(a) * 1.72, Math.sin(a) * 1.72, .1);
      if (i === 0) ctx.moveTo(q[0], q[1]); else ctx.lineTo(q[0], q[1]);
    }
    ctx.strokeStyle = 'rgba(150,211,181,.13)'; ctx.lineWidth = .6; ctx.stroke();
    for (const p of points) {
      const t = targets[p.i];
      const ease = immediate ? 1 : .065;
      p.x += (t[0] - p.x) * ease; p.y += (t[1] - p.y) * ease; p.z += (t[2] - p.z) * ease;
      const q = project(p.x, p.y, p.z);
      const depth = Math.max(.1, Math.min(1, (1.7 - q[2]) / 3));
      const pulse = .88 + .12 * Math.sin(p.i * .017 + time * .65);
      ctx.fillStyle = p.i % 41 === 0
        ? `rgba(219,241,153,${depth * pulse})`
        : `rgba(164,225,203,${(.22 + depth * .75) * pulse})`;
      const radius = (p.i % 41 === 0 ? 1.65 : .72) * (.6 + depth);
      ctx.beginPath(); ctx.arc(q[0], q[1], radius, 0, TAU); ctx.fill();
      if (p.i % 100 < 99 && p.i % 4 === 0 && mode === 'agent') {
        const next = targets[Math.min(p.i + 1, count - 1)];
        const r = project(...next);
        ctx.strokeStyle = `rgba(138,203,174,${depth * .13})`;
        ctx.beginPath(); ctx.moveTo(q[0], q[1]); ctx.lineTo(r[0], r[1]); ctx.stroke();
      }
    }
  }
  function animate(timestamp) {
    frame = 0;
    if (paused || !visible || document.hidden) return;
    if (timestamp - last >= 30) {
      time += Math.min((timestamp - last) / 1000, .05);
      last = timestamp; draw();
    }
    frame = requestAnimationFrame(animate);
  }
  function start() { if (ctx && !frame && !paused && visible && !document.hidden) { last = performance.now(); frame = requestAnimationFrame(animate); } }
  function stop() { cancelAnimationFrame(frame); frame = 0; }
  for (const button of controls) button.addEventListener('click', () => {
    mode = button.dataset.shape;
    controls.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    description.textContent = states[mode].text;
    link.href = `${base}/work/${states[mode].path}/`;
    link.setAttribute('aria-label', `Explore the related ${mode} project`);
    targets = points.map(p => target(p.i, mode));
    if (paused || !visible) draw(true); else start();
  });
  if (!ctx) return;
  shell.classList.add('scene-ready'); pause.hidden = false; updatePause();
  pause.addEventListener('click', () => { paused = !paused; updatePause(); if (paused) stop(); else start(); });
  shell.addEventListener('pointermove', event => {
    if (reduce.matches || event.pointerType === 'touch') return;
    const rect = shell.getBoundingClientRect();
    pointerX = (event.clientX - rect.left) / rect.width - .5;
    pointerY = (event.clientY - rect.top) / rect.height - .5;
  });
  shell.addEventListener('pointerleave', () => { pointerX = pointerY = 0; });
  new ResizeObserver(() => {
    width = shell.clientWidth; height = shell.clientHeight;
    const dpr = Math.min(devicePixelRatio || 1, 1.75);
    canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); draw(true);
  }).observe(shell);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; if (visible) start(); else stop(); }).observe(shell);
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); else start(); });
  reduce.addEventListener('change', () => { paused = reduce.matches; pointerX = pointerY = 0; updatePause(); if (paused) { stop(); draw(true); } else start(); });
})();
