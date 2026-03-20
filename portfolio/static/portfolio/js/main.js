/* ── NAVBAR SCROLL ── */
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('navbar');
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

/* ── HAMBURGER MENU ── */
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');
if (hamburger) {
  hamburger.addEventListener('click', () => {
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
    navLinks.style.flexDirection = 'column';
    navLinks.style.position = 'absolute';
    navLinks.style.top = '100%';
    navLinks.style.left = '0';
    navLinks.style.right = '0';
    navLinks.style.background = 'rgba(10,10,15,0.97)';
    navLinks.style.padding = '1rem 1.5rem';
    navLinks.style.gap = '1rem';
    navLinks.style.borderTop = '1px solid rgba(255,255,255,0.07)';
  });
}

/* ── TYPED TEXT ── */
const typedEl = document.getElementById('typed');
const phrases = [
  'Full Stack Developer',
  'Backend Engineer',
  'Django Expert',
  'API Architect',
  'Problem Solver',
];
let phraseIdx = 0;
let charIdx = 0;
let deleting = false;

function typeLoop() {
  const current = phrases[phraseIdx];
  if (!deleting) {
    typedEl.textContent = current.slice(0, charIdx + 1);
    charIdx++;
    if (charIdx === current.length) {
      deleting = true;
      setTimeout(typeLoop, 1800);
      return;
    }
  } else {
    typedEl.textContent = current.slice(0, charIdx - 1);
    charIdx--;
    if (charIdx === 0) {
      deleting = false;
      phraseIdx = (phraseIdx + 1) % phrases.length;
    }
  }
  setTimeout(typeLoop, deleting ? 60 : 100);
}
typeLoop();

/* ── SCROLL ANIMATIONS ── */
const animatedEls = document.querySelectorAll(
  '.project-card, .skill-item, .timeline-card, .contact-item, .section-header'
);
animatedEls.forEach(el => el.classList.add('fade-in-up'));

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 80);
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1 }
);
animatedEls.forEach(el => observer.observe(el));

/* ── SKILL BARS ── */
const skillBars = document.querySelectorAll('.skill-bar-fill');
const barObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const w = entry.target.getAttribute('data-width');
        entry.target.style.width = w + '%';
        barObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.3 }
);
skillBars.forEach(bar => barObserver.observe(bar));

/* ── CONTACT FORM ── */
const form = document.getElementById('contactForm');
const formNote = document.getElementById('formNote');

if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"] span:first-child');
    const originalText = btn.textContent;
    btn.textContent = 'Enviando…';

    setTimeout(() => {
      btn.textContent = originalText;
      formNote.textContent = '✅ ¡Mensaje enviado! Me pondré en contacto pronto.';
      form.reset();
      setTimeout(() => { formNote.textContent = ''; }, 5000);
    }, 1200);
  });
}

/* ── SMOOTH ACTIVE NAV ── */
const sections = document.querySelectorAll('section[id]');
const navItems = document.querySelectorAll('.nav-links a');

window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(sec => {
    if (window.scrollY >= sec.offsetTop - 200) {
      current = sec.getAttribute('id');
    }
  });
  navItems.forEach(a => {
    a.style.color = a.getAttribute('href') === '#' + current
      ? 'var(--blue)'
      : '';
  });
});
