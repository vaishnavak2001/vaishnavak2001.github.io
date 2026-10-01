(() => {
  'use strict';
  const menu = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  if (menu && navigation) {
    document.documentElement.classList.add('menu-enabled');
    menu.hidden = false;
    function closeMenu() { menu.setAttribute('aria-expanded', 'false'); navigation.classList.remove('is-open'); }
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('is-open', open);
    });
    navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); } });
    document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
    matchMedia('(min-width: 761px)').addEventListener('change', closeMenu);
  }
  const filters = document.querySelector('.project-filter');
  if (filters) {
    filters.hidden = false;
    const items = [...document.querySelectorAll('.work-item')];
    const status = document.querySelector('.filter-status');
    status.hidden = false; status.textContent = `${items.length} projects`;
    filters.addEventListener('click', event => {
      const button = event.target.closest('[data-filter]');
      if (!button) return;
      const filter = button.dataset.filter;
      let visible = 0;
      for (const item of items) {
        item.hidden = !(filter === 'all' || item.dataset.category === filter || item.dataset.kind === filter);
        if (!item.hidden) visible++;
      }
      filters.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      status.textContent = visible ? `${visible} ${visible === 1 ? 'project' : 'projects'}${filter === 'all' ? '' : ' · ' + filter}` : 'No projects in this category yet. Choose All work to keep exploring.';
    });
  }
  document.querySelectorAll('.walkthrough').forEach(section => {
    const source = [...section.querySelectorAll('.static-steps li')];
    const flow = section.querySelector('.walkthrough-flow');
    const detail = section.querySelector('.step-detail');
    const actions = section.querySelector('.walkthrough-actions');
    if (!source.length || !flow || !detail || !actions) return;
    let current = 0;
    const buttons = [...flow.querySelectorAll('button')];
    const previous = actions.querySelector('[data-previous]');
    const next = actions.querySelector('[data-next]');
    const replay = actions.querySelector('[data-replay]');
    const count = actions.querySelector('.step-count');
    function render(index) {
      current = Math.max(0, Math.min(source.length - 1, index));
      buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === current)));
      detail.querySelector('h3').textContent = source[current].querySelector('strong').textContent;
      detail.querySelector('p').textContent = source[current].querySelector('span').textContent;
      count.textContent = `Step ${current + 1} of ${source.length}`;
      previous.disabled = current === 0; next.disabled = current === source.length - 1;
      replay.hidden = current !== source.length - 1;
      detail.classList.remove('is-changing');
      requestAnimationFrame(() => detail.classList.add('is-changing'));
    }
    buttons.forEach((button, index) => button.addEventListener('click', () => render(index)));
    previous.addEventListener('click', () => render(current - 1));
    next.addEventListener('click', () => render(current + 1));
    replay.addEventListener('click', () => { render(0); buttons[0].focus(); });
    flow.hidden = detail.hidden = actions.hidden = false;
    section.querySelector('.static-steps').open = false;
    section.classList.add('is-enhanced'); render(0);
  });
})();
