/* =====================================================
   Fundamentals of Data Analytics - Core JS
   Theme, Progress, Sidebar, Quiz, Search, Collapse
   ===================================================== */

(function () {
  'use strict';

  // ----- Theme -----
  const root = document.documentElement;
  const savedTheme = localStorage.getItem('da-theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  root.setAttribute('data-theme', savedTheme);

  function toggleTheme() {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('da-theme', next);
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
    menuBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 992 && sidebar.classList.contains('open') &&
          !sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }

  // ----- Collapsible Sections -----
  document.querySelectorAll('[data-collapse]').forEach(header => {
    header.addEventListener('click', () => {
      const target = document.getElementById(header.getAttribute('data-collapse'));
      if (!target) return;
      target.classList.toggle('open');
      const icon = header.querySelector('.collapse-icon');
      if (icon) icon.textContent = target.classList.contains('open') ? '−' : '+';
    });
  });

  // ----- Quiz Engine -----
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
    // Track progress
    markProgress(quizId, isCorrect);
  };

  document.querySelectorAll('.quiz-option').forEach(opt => {
    opt.addEventListener('click', function () {
      const parent = this.closest('.quiz-card');
      if (!parent) return;
      parent.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
      this.classList.add('selected');
    });
  });

  // ----- Flashcards -----
  document.querySelectorAll('.flashcard').forEach(card => {
    card.addEventListener('click', () => card.classList.toggle('flipped'));
  });

  // ----- Progress Tracker (localStorage) -----
  const PROGRESS_KEY = 'da-course-progress';
  function getProgress() {
    try { return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}'); }
    catch { return {}; }
  }
  function saveProgress(data) {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(data));
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
      if (ring && p['lecture-' + id]) ring.classList.add('done');
    });
  }
  updateSidebarProgress();

  // ----- Search (simple client-side) -----
  const searchIndex = window.COURSE_SEARCH_INDEX || [];
  const searchOverlay = document.getElementById('searchOverlay');
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');

  function openSearch() {
    if (searchOverlay) {
      searchOverlay.classList.add('open');
      if (searchInput) setTimeout(() => searchInput.focus(), 50);
    }
  }
  function closeSearch() {
    if (searchOverlay) searchOverlay.classList.remove('open');
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
      searchResults.innerHTML = '<div class="search-result-item"><p>Type at least 2 characters…</p></div>';
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
    searchResults.innerHTML = hits.map(h => `
      <a href="${h.url}" class="search-result-item" style="display:block;text-decoration:none;color:inherit;">
        <h4>${h.title}</h4>
        <p>${h.module || ''} · ${h.summary || ''}</p>
      </a>
    `).join('');
  });

  // ----- Theme button -----
  document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);

  // ----- Animate on scroll (simple) -----
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) e.target.classList.add('animate-in');
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.card, .callout, .diagram-box, .quiz-card').forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
  });

  // Expose helpers
  window.DA = { toggleTheme, markProgress, getProgress, openSearch, closeSearch };
})();
