/* EMG Consulting Group — site behaviour */
(function () {
  'use strict';

  /* ---- sticky header state ---- */
  var header = document.getElementById('header');
  var hero = document.querySelector('.hero');

  function solidify() {
    if (!header) return;
    // solid once we've scrolled past most of the hero, or immediately on pages with no hero
    var trigger = hero ? Math.min(hero.offsetHeight - 90, 420) : 10;
    header.classList.toggle('is-solid', window.scrollY > trigger);
  }
  solidify();
  window.addEventListener('scroll', solidify, { passive: true });
  window.addEventListener('resize', solidify);

  /* ---- mobile nav ---- */
  var burger = document.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      burger.setAttribute('aria-expanded', String(open));
    });
    document.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('nav-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
        document.body.classList.remove('nav-open');
        burger.setAttribute('aria-expanded', 'false');
        burger.focus();
      }
    });
  }

  /* ---- reveal on scroll ---- */
  var reveals = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    reveals.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---- current year ---- */
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---- mark current page in nav ---- */
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === here && !a.classList.contains('btn')) {
      a.setAttribute('aria-current', 'page');
    }
  });
})();

/* ---- reference portfolio lightbox ---- */
(function () {
  'use strict';
  var lb = document.getElementById('lb');
  if (!lb) return;
  var img = document.getElementById('lb-img');
  var cap = document.getElementById('lb-cap');
  var shots = [].slice.call(document.querySelectorAll('.pf-shot'));
  var i = 0;

  function show(n) {
    i = (n + shots.length) % shots.length;
    var a = shots[i];
    var entry = a.closest('.pf-entry');
    img.src = a.getAttribute('href');
    img.alt = 'Reference portfolio page ' + a.dataset.lb;
    var h3 = entry.querySelector('h3');
    var meta = entry.querySelector('.pf-meta');
    cap.innerHTML = '<b>' + (h3 ? h3.textContent : '') + '</b>' +
      'Page ' + a.dataset.lb + (meta ? ' &middot; ' + meta.textContent : '');
  }
  function open(n) { show(n); lb.setAttribute('open', ''); document.body.style.overflow = 'hidden'; }
  function close() { lb.removeAttribute('open'); document.body.style.overflow = ''; img.src = ''; }

  shots.forEach(function (a, n) {
    a.addEventListener('click', function (e) { e.preventDefault(); open(n); });
  });
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(i - 1); });
  lb.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(i + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  window.addEventListener('keydown', function (e) {
    if (!lb.hasAttribute('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(i - 1);
    if (e.key === 'ArrowRight') show(i + 1);
  });

  /* highlight the chapter currently in view */
  var links = [].slice.call(document.querySelectorAll('.pf-nav a'));
  var chapters = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('on'); });
          var k = chapters.indexOf(en.target);
          if (k > -1) links[k].classList.add('on');
        }
      });
    }, { rootMargin: '-15% 0px -70% 0px' });
    chapters.forEach(function (c) { if (c) io.observe(c); });
  }
})();
