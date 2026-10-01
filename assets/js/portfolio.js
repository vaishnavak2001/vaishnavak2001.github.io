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
    document.querySelector('.work-tools').hidden = false;
    const items = [...document.querySelectorAll('.work-item, .repository-item')];
    const status = document.querySelector('.filter-status');
    const search = document.querySelector('#project-search');
    const reset = document.querySelector('.reset-filters');
    const empty = document.querySelector('.work-empty');
    let filter = 'all';
    const searchable = new Map(items.map(item => [item, item.dataset.search.toLocaleLowerCase()]));
    function renderProjects() {
      const words = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      let cases = 0, repositories = 0;
      for (const item of items) {
        const matchesCategory = filter === 'all' || item.dataset.category === filter || item.dataset.kind === filter;
        item.hidden = !(matchesCategory && words.every(word => searchable.get(item).includes(word)));
        if (!item.hidden) item.classList.contains('work-item') ? cases++ : repositories++;
      }
      filters.querySelectorAll('button').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === filter)));
      document.querySelector('#case-studies').hidden = cases === 0;
      document.querySelector('#repositories').hidden = repositories === 0;
      empty.hidden = cases + repositories > 0;
      reset.hidden = filter === 'all' && words.length === 0;
      status.textContent = `${cases} ${cases === 1 ? 'case study' : 'case studies'} · ${repositories} ${repositories === 1 ? 'repository' : 'repositories'}${filter === 'all' ? '' : ' · ' + filter}`;
    }
    filters.addEventListener('click', event => {
      const button = event.target.closest('[data-filter]');
      if (!button) return;
      filter = button.dataset.filter;
      renderProjects();
    });
    search.addEventListener('input', renderProjects);
    reset.addEventListener('click', () => { search.value = ''; filter = 'all'; renderProjects(); search.focus(); });
    document.querySelectorAll('.collection-nav a').forEach(link => link.addEventListener('click', () => {
      if (document.querySelector(link.hash).hidden) { filter = 'all'; search.value = ''; renderProjects(); }
    }));
    renderProjects();
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
