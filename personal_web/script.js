/* =============================================
   Language toggle
   ============================================= */
let currentLang = 'en';

function switchLang(lang) {
  currentLang = lang;
  document.documentElement.lang = lang === 'en' ? 'en' : 'zh';

  document.body.classList.add('lang-switching');

  document.querySelectorAll('[data-en][data-zh]').forEach(el => {
    el.textContent = el.dataset[lang];
  });

  document.querySelectorAll('.lang-toggle__en, .lang-toggle__zh').forEach(span => {
    const isEn = span.classList.contains('lang-toggle__en');
    span.hidden = lang === 'en' ? !isEn : isEn;
  });

  setTimeout(() => document.body.classList.remove('lang-switching'), 200);
}

document.getElementById('langToggle').addEventListener('click', () => {
  switchLang(currentLang === 'en' ? 'zh' : 'en');
});

document.getElementById('langToggleMobile').addEventListener('click', () => {
  switchLang(currentLang === 'en' ? 'zh' : 'en');
  closeMenu();
});

/* =============================================
   Hamburger menu
   ============================================= */
const hamburger = document.getElementById('hamburger');
const overlay = document.getElementById('mobileOverlay');
let menuOpen = false;

function openMenu() {
  menuOpen = true;
  hamburger.classList.add('is-open');
  hamburger.setAttribute('aria-expanded', 'true');
  overlay.classList.add('is-open');
  overlay.removeAttribute('aria-hidden');
  document.body.style.overflow = 'hidden';
}

function closeMenu() {
  menuOpen = false;
  hamburger.classList.remove('is-open');
  hamburger.setAttribute('aria-expanded', 'false');
  overlay.classList.remove('is-open');
  overlay.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

hamburger.addEventListener('click', () => {
  menuOpen ? closeMenu() : openMenu();
});

overlay.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', closeMenu);
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && menuOpen) closeMenu();
});

/* =============================================
   Active nav link via Intersection Observer
   ============================================= */
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav__links a[href^="#"]');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      navLinks.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
      });
    }
  });
}, { rootMargin: `-${64}px 0px -60% 0px`, threshold: 0 });

sections.forEach(s => observer.observe(s));

/* =============================================
   Nav shadow on scroll
   ============================================= */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.style.borderBottomColor = window.scrollY > 20
    ? 'rgba(42,42,42,0.8)'
    : 'var(--color-border)';
}, { passive: true });
