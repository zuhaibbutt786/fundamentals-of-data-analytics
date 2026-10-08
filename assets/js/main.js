/* =====================================================
   Fundamentals of Data Analytics - Core JS
   Theme, Progress, Sidebar, Quiz, Search, Collapse + KaTeX + dark fixes
   ===================================================== */

(function () {
  'use strict';

  const courseBase = new URL('../../', document.currentScript.src);
  const storage = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); } catch { /* Reading works without storage. */ } }
  };
  // ----- Theme -----
  const root = document.documentElement;
  const savedTheme = storage.get('da-theme') ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  root.setAttribute('data-theme', savedTheme);

  function toggleTheme() {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    storage.set('da-theme', next);
    updateThemeIcon(next);
  }

  function updateThemeIcon(theme) {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;
    btn.innerHTML = theme === 'dark'
      ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
      : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }
  updateThemeIcon(savedTheme);

  // Load dark-mode structure/formula visibility fixes
  (function loadDarkFixes() {
    if (document.getElementById('dark-mode-fixes-css')) return;
    const link = document.createElement('link');
    link.id = 'dark-mode-fixes-css';
    link.rel = 'stylesheet';
    link.href = new URL('assets/css/dark-mode-fixes.css', courseBase).href;
    link.onerror = function () {
      this.onerror = null;
      this.href = '/fundamentals-of-data-analytics/assets/css/dark-mode-fixes.css';
    };
    document.head.appendChild(link);
  })();

  // ----- Reading Progress -----
  function updateProgress() {
    const bar = document.getElementById('readingProgress');
    if (!bar) return;
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    bar.style.width = Math.min(100, Math.max(0, pct)) + '%';
  }
  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();

  // ----- Sidebar Mobile -----
  const sidebar = document.getElementById('sidebar');
  const menuBtn = document.getElementById('menuToggle');
  if (menuBtn && sidebar) {
    menuBtn.setAttribute('aria-controls', 'sidebar');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.addEventListener('click', () => { sidebar.classList.toggle('open'); menuBtn.setAttribute('aria-expanded', String(sidebar.classList.contains('open'))); });
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 992 && sidebar.classList.contains('open') &&
          !sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
        sidebar.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ----- Collapsible -----
  document.querySelectorAll('[data-collapse]').forEach(header => {
    header.addEventListener('click', () => {
      const target = document.getElementById(header.getAttribute('data-collapse'));
      if (!target) return;
      target.classList.toggle('open');
      header.setAttribute('aria-expanded', String(target.classList.contains('open')));
      const icon = header.querySelector('.collapse-icon');
      if (icon) icon.textContent = target.classList.contains('open') ? '\u2212' : '+';
    });
  });

  // ----- Quiz -----
  window.checkQuiz = function (quizId) {
    const quiz = document.getElementById(quizId);
    if (!quiz) return;
    const correct = quiz.dataset.answer;
    const selected = quiz.querySelector('.quiz-option.selected');
    const feedback = quiz.querySelector('.quiz-feedback');
    if (!selected) {
      if (feedback) {
        feedback.className = 'quiz-feedback show incorrect';
        feedback.textContent = 'Please select an answer first.';
      }
      return;
    }
    const isCorrect = selected.dataset.value === correct;
    quiz.querySelectorAll('.quiz-option').forEach(opt => {
      opt.classList.remove('correct', 'incorrect');
      if (opt.dataset.value === correct) opt.classList.add('correct');
      else if (opt === selected && !isCorrect) opt.classList.add('incorrect');
    });
    if (feedback) {
      feedback.className = 'quiz-feedback show ' + (isCorrect ? 'correct' : 'incorrect');
      feedback.textContent = isCorrect
        ? (quiz.dataset.success || 'Correct! Well done.')
        : (quiz.dataset.fail || 'Not quite. Review the explanation and try again.');
    }
    markProgress(location.pathname + ':' + quizId, isCorrect);
  };

  document.querySelectorAll('.quiz-option').forEach(opt => {
    opt.addEventListener('click', function () {
      const parent = this.closest('.quiz-card');
      if (!parent) return;
      parent.querySelectorAll('.quiz-option').forEach(o => { o.classList.remove('selected'); o.setAttribute('aria-checked', 'false'); });
      this.classList.add('selected'); this.setAttribute('aria-checked', 'true');
    });
  });

  // ----- Flashcards -----
  document.querySelectorAll('.flashcard').forEach(card => {
    card.addEventListener('click', () => { card.classList.toggle('flipped'); card.setAttribute('aria-pressed', String(card.classList.contains('flipped'))); updateFlashcard(card); });
  });

  // ----- Progress -----
  const PROGRESS_KEY = 'da-course-progress';
  function getProgress() {
    try { const data = JSON.parse(storage.get(PROGRESS_KEY) || '{}'); return data && typeof data === 'object' && !Array.isArray(data) ? data : {}; }
    catch { return {}; }
  }
  function saveProgress(data) {
    storage.set(PROGRESS_KEY, JSON.stringify(data));
  }
  function markProgress(id, value) {
    const p = getProgress();
    p[id] = value;
    saveProgress(p);
    updateSidebarProgress();
  }
  window.markLectureComplete = function (lectureId) {
    markProgress('lecture-' + lectureId, true);
  };
  function updateSidebarProgress() {
    const p = getProgress();
    document.querySelectorAll('[data-lecture-id]').forEach(el => {
      const id = el.getAttribute('data-lecture-id');
      const ring = el.querySelector('.progress-ring');
      if (ring) ring.classList.toggle('done', Boolean(p['lecture-' + id]));
    });
  }
  updateSidebarProgress();

  // ----- Search -----
  const searchIndex = window.COURSE_SEARCH_INDEX || [];
  const searchOverlay = document.getElementById('searchOverlay');
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');

  let searchOrigin;
  function openSearch() {
    searchOrigin = document.activeElement;
    if (searchOverlay) {
      searchOverlay.classList.add('open'); searchOverlay.removeAttribute('aria-hidden'); searchOverlay.inert = false;
      if (searchInput) setTimeout(() => searchInput.focus(), 50);
    }
  }
  function closeSearch() {
    if (searchOverlay) { searchOverlay.classList.remove('open'); searchOverlay.setAttribute('aria-hidden', 'true'); searchOverlay.inert = true; searchOrigin?.focus(); }
  }

  document.getElementById('searchBtn')?.addEventListener('click', openSearch);
  document.getElementById('searchClose')?.addEventListener('click', closeSearch);
  searchOverlay?.addEventListener('click', (e) => {
    if (e.target === searchOverlay) closeSearch();
  });
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      openSearch();
    }
    if (e.key === 'Escape') closeSearch();
  });

  searchInput?.addEventListener('input', function () {
    const q = this.value.trim().toLowerCase();
    if (!searchResults) return;
    if (q.length < 2) {
      searchResults.innerHTML = '<div class="search-result-item"><p>Type at least 2 characters\u2026</p></div>';
      return;
    }
    const hits = searchIndex.filter(item =>
      item.title.toLowerCase().includes(q) ||
      item.keywords.toLowerCase().includes(q) ||
      (item.summary || '').toLowerCase().includes(q)
    ).slice(0, 12);
    if (hits.length === 0) {
      searchResults.innerHTML = '<div class="search-result-item"><p>No results found.</p></div>';
      return;
    }
    searchResults.replaceChildren(...hits.map(h => {
      const link = document.createElement('a');
      link.setAttribute('href', new URL(h.url, courseBase).href); link.className = 'search-result-item';
      link.style.display = 'block'; link.style.textDecoration = 'none'; link.style.color = 'inherit';
      const title = document.createElement('h4'), description = document.createElement('p');
      title.textContent = h.title; description.textContent = (h.module || '') + ' · ' + (h.summary || '');
      link.append(title, description); return link;
    }));
  });

  document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);

  // Content remains visible when motion or IntersectionObserver is unavailable.
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('animate-in'); observer.unobserve(e.target); }
    }), { threshold: 0.08 });
    document.querySelectorAll('.card, .callout, .diagram-box, .quiz-card').forEach(el => observer.observe(el));
  }

  function activateByKeyboard(el) {
    el.tabIndex = 0;
    el.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
    });
  }
  function updateFlashcard(card) {
    const flipped = card.classList.contains('flipped');
    card.querySelector('.flashcard-front')?.setAttribute('aria-hidden', String(flipped));
    card.querySelector('.flashcard-back')?.setAttribute('aria-hidden', String(!flipped));
  }
  document.querySelectorAll('.flashcard').forEach(card => {
    card.setAttribute('role', 'button'); card.setAttribute('aria-pressed', 'false');
    activateByKeyboard(card); updateFlashcard(card);
  });
  document.querySelectorAll('[data-collapse]').forEach(el => {
    const id = el.dataset.collapse;
    el.setAttribute('role', 'button'); el.setAttribute('aria-controls', id);
    el.setAttribute('aria-expanded', String(Boolean(document.getElementById(id)?.classList.contains('open'))));
    activateByKeyboard(el);
  });
  document.querySelectorAll('.quiz-card').forEach(quiz => {
    quiz.setAttribute('role', 'group');
    const question = quiz.querySelector('p');
    if (question) { question.id = quiz.id + '-question'; quiz.setAttribute('aria-labelledby', question.id); }
    quiz.querySelector('.quiz-feedback')?.setAttribute('aria-live', 'polite');
    const choices = document.createElement('div'); choices.setAttribute('role', 'radiogroup');
    if (question) choices.setAttribute('aria-labelledby', question.id);
    const options = [...quiz.querySelectorAll('.quiz-option')];
    if (options.length) { options[0].before(choices); options.forEach(opt => choices.append(opt)); }
    quiz.querySelectorAll('.quiz-option').forEach(opt => {
      opt.setAttribute('role', 'radio'); opt.setAttribute('aria-checked', 'false'); activateByKeyboard(opt);
      opt.addEventListener('keydown', e => {
        if (!['ArrowDown','ArrowUp','ArrowLeft','ArrowRight'].includes(e.key)) return;
        e.preventDefault(); const options = [...quiz.querySelectorAll('.quiz-option')];
        const offset = ['ArrowDown','ArrowRight'].includes(e.key) ? 1 : -1;
        const next = options[(options.indexOf(opt) + offset + options.length) % options.length]; next.focus(); next.click();
      });
    });
  });
  const completion = document.querySelector('[data-complete-lecture]');
  if (completion) {
    const key = 'lecture-' + completion.dataset.completeLecture;
    completion.checked = Boolean(getProgress()[key]);
    completion.addEventListener('change', () => markProgress(key, completion.checked));
  }
  if (searchOverlay) {
    searchOverlay.setAttribute('role', 'dialog'); searchOverlay.setAttribute('aria-modal', 'true');
    searchOverlay.setAttribute('aria-label', 'Search all 30 lectures'); searchOverlay.setAttribute('aria-hidden', 'true'); searchOverlay.inert = true;
    searchInput?.setAttribute('aria-label', 'Search course topics');
    searchResults?.setAttribute('aria-live', 'polite');
    if (!document.getElementById('searchClose')) {
      const close = document.createElement('button'); close.id = 'searchClose'; close.textContent = 'Close search';
      close.type = 'button'; close.className = 'search-close'; close.addEventListener('click', closeSearch);
      searchOverlay.querySelector('.search-box')?.prepend(close);
    }
    searchOverlay.addEventListener('keydown', e => {
      if (e.key !== 'Tab') return;
      const items = [...searchOverlay.querySelectorAll('button,input,a[href]')];
      const first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }
  // Every lecture is reachable without relying on JavaScript search.
  if (sidebar) {
    const all = document.createElement('details'); const summary = document.createElement('summary');
    summary.textContent = 'All 30 lectures'; all.append(summary);
    const nav = document.createElement('nav'); nav.setAttribute('aria-label', 'All lectures'); nav.className = 'sidebar-nav';
    (window.COURSE_SEARCH_INDEX || []).forEach(item => {
      const link = document.createElement('a'); link.href = new URL(item.url, courseBase).href; link.textContent = item.title;
      if (new URL(link.href).pathname === location.pathname) link.setAttribute('aria-current', 'page'); nav.append(link);
    });
    all.append(nav); sidebar.append(all);
  }

  // ----- KaTeX -----
  function loadKaTeX() {
    if (window.katex && window.renderMathInElement) {
      renderMathInElement(document.body, {
        delimiters: [
          { left: '\\[', right: '\\]', display: true },
          { left: '\\(', right: '\\)', display: false },
          { left: '$$', right: '$$', display: true }
        ],
        throwOnError: false
      });
      return;
    }
    if (!document.getElementById('katex-css')) {
      const link = document.createElement('link');
      link.id = 'katex-css';
      link.rel = 'stylesheet';
      link.href = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css';
      document.head.appendChild(link);
    }
    function loadScript(src, id) {
      return new Promise((resolve, reject) => {
        if (document.getElementById(id)) { resolve(); return; }
        const s = document.createElement('script');
        s.id = id;
        s.src = src;
        s.onload = resolve;
        s.onerror = reject;
        document.head.appendChild(s);
      });
    }
    loadScript('https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js', 'katex-js')
      .then(function () {
        return loadScript(
          'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js',
          'katex-auto'
        );
      })
      .then(function () {
        if (window.renderMathInElement) {
          renderMathInElement(document.body, {
            delimiters: [
              { left: '\\[', right: '\\]', display: true },
              { left: '\\(', right: '\\)', display: false },
              { left: '$$', right: '$$', display: true }
            ],
            throwOnError: false
          });
        }
      })
      .catch(function () {});
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadKaTeX);
  } else {
    loadKaTeX();
  }

  window.DA = { toggleTheme, markProgress, getProgress, openSearch, closeSearch };
})();
