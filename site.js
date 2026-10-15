/* Shared by every page of kevinckma.github.io (main site, research portal and its login page).
   1. Light / dark theme: follows the device setting until the visitor picks one with the
      nav button; the choice is remembered (localStorage) and shared by all pages.
   2. "Skip to content" link for keyboard users.
   3. Keyboard access to enlargeable images and their popups (Enter/Space opens,
      focus moves into the popup, Tab stays there, Escape/Close returns focus).
   Loaded synchronously in <head> so the theme is set before the page is drawn. */
(function () {
  var KEY = 'theme', root = document.documentElement;
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function saved() { try { var t = localStorage.getItem(KEY); return t === 'dark' || t === 'light' ? t : null; } catch (e) { return null; } }
  function system() { return mq && mq.matches ? 'dark' : 'light'; }
  function apply(t) {
    root.setAttribute('data-theme', t);
    var b = document.querySelector('.theme-toggle');
    if (b) {
      b.setAttribute('aria-pressed', String(t === 'dark'));
      b.title = t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    }
  }
  apply(saved() || system());
  if (mq && mq.addEventListener) mq.addEventListener('change', function () { if (!saved()) apply(system()); });
  window.addEventListener('storage', function (e) { if (e.key === KEY) apply(saved() || system()); });

  var ICONS = '<svg class="ti-moon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>' +
    '<svg class="ti-sun" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>';

  function addToggle() {
    var links = document.querySelector('nav .nav-links');
    if (!links || links.querySelector('.theme-toggle')) return;
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'theme-toggle';
    b.setAttribute('aria-label', 'Dark mode');
    b.innerHTML = ICONS;
    b.addEventListener('click', function () {
      var t = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(KEY, t); } catch (e) {}
      apply(t);
    });
    links.appendChild(b);
    apply(root.getAttribute('data-theme'));
  }

  function addSkipLink() {
    var main = document.querySelector('main');
    if (!main || document.querySelector('.skip-link')) return;
    if (!main.id) main.id = 'main';
    if (!main.hasAttribute('tabindex')) main.setAttribute('tabindex', '-1');
    var a = document.createElement('a');
    a.className = 'skip-link'; a.href = '#' + main.id; a.textContent = 'Skip to content';
    a.addEventListener('click', function (e) { e.preventDefault(); main.focus(); main.scrollIntoView(); });
    document.body.insertBefore(a, document.body.firstChild);
  }

  // Enlargeable images and the popups that show them
  var ZOOM = '.abs-thumb, .zoomable, .sphoto, .ms-fig img, .ms-pub-fig img, .post-fig img';
  var DIALOGS = '#lightbox, #lb, #ms-lb';
  function markZoomables() {
    document.querySelectorAll(ZOOM).forEach(function (el) {
      if (el.hasAttribute('data-kb')) return;
      el.setAttribute('data-kb', '');
      el.tabIndex = 0;
      el.setAttribute('role', 'button');
      el.setAttribute('aria-haspopup', 'dialog');
      var alt = (el.getAttribute('alt') || '').trim();
      el.setAttribute('aria-label', alt ? 'Enlarge image: ' + alt : 'Enlarge image');
    });
  }
  document.addEventListener('keydown', function (e) {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches && e.target.matches('[data-kb]')) {
      e.preventDefault(); e.target.click();
    }
  });

  var opener = null, openDialog = null;
  function setupDialog(d) {
    if (d.hasAttribute('data-kb')) return;
    d.setAttribute('data-kb', '');
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-modal', 'true');
    if (!d.hasAttribute('aria-label')) d.setAttribute('aria-label', 'Enlarged image');
    var c = document.createElement('button');
    c.type = 'button'; c.className = 'lb-close'; c.setAttribute('aria-label', 'Close');
    c.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"/></svg>';
    c.addEventListener('click', function (e) { e.stopPropagation(); d.classList.remove('open'); });
    d.appendChild(c);
    new MutationObserver(function () {
      var open = d.classList.contains('open');
      if (open && openDialog !== d) {
        openDialog = d;
        opener = document.activeElement && document.activeElement !== document.body ? document.activeElement : null;
        c.focus();
      } else if (!open && openDialog === d) {
        openDialog = null;
        if (opener && document.contains(opener)) opener.focus();
        opener = null;
      }
    }).observe(d, { attributes: true, attributeFilter: ['class'] });
  }
  // keep keyboard focus inside an open popup (its only control is the Close button)
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Tab' && openDialog) { e.preventDefault(); openDialog.querySelector('.lb-close').focus(); }
  });

  function init() {
    addToggle(); addSkipLink(); markZoomables();
    document.querySelectorAll(DIALOGS).forEach(setupDialog);
    var pending = false;   // pages that add images later (e.g. the digest feed)
    new MutationObserver(function () {
      if (pending) return; pending = true;
      setTimeout(function () { pending = false; markZoomables(); document.querySelectorAll(DIALOGS).forEach(setupDialog); }, 50);
    }).observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
