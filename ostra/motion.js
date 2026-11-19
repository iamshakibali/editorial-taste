/* =========================================================
   Editorial Taste — motion.js
   Smooth scroll · hero intro · reveals · masked text · image unmask ·
   statement words · count-up · nav hide/show · button label roll.

   Progressive by design: without JS, or with prefers-reduced-motion,
   every element is simply visible in its final state.
   HTML API (see references/motion.md):
     .reveal                  fade + rise
     data-reveal="text"       words rise out of masks
     data-reveal="image"      image unmasks from the bottom and settles
     data-stagger="80"        children of this element reveal in sequence (ms step)
     data-words               statement: words light up as they cross the reading line
     data-count               number counts up when it enters the viewport
     style="--d: .3s"         extra delay for one element
   ========================================================= */
(() => {
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const easeOutExpo = (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));
  const nav = document.getElementById('nav');

  /* ---------- 1. Smooth scroll (Lenis, if loaded) ---------- */
  let lenis = null;
  if (!reduced && typeof window.Lenis === 'function') {
    lenis = new window.Lenis({ autoRaf: true, lerp: 0.09, smoothWheel: true });
    window.__lenis = lenis; // the drawer calls __lenis.stop()/start()
  }

  // In-page anchors: glide with the same curve, land below the fixed nav, move focus.
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href^="#"]');
    if (!link) return;
    const hash = link.getAttribute('href');
    let target = null;
    try { target = hash.length > 1 ? document.querySelector(hash) : null; } catch { return; }
    if (!target) return;
    e.preventDefault();
    const offset = -(nav ? nav.offsetHeight : 0);
    if (lenis) lenis.scrollTo(target, { offset, duration: 1.4, easing: easeOutExpo, force: true });
    else window.scrollTo({ top: target.getBoundingClientRect().top + scrollY + offset, behavior: reduced ? 'auto' : 'smooth' });
    history.pushState(null, '', hash);
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  });

  /* ---------- 2. Word splitting (screen readers keep the original text) ---------- */
  function splitWords(el, makeWord) {
    if (el.dataset.split) return [];
    el.dataset.split = 'true';
    const label = el.textContent.replace(/\s+/g, ' ').trim();
    const visual = document.createElement('span');
    visual.setAttribute('aria-hidden', 'true');
    const words = [];
    const walk = (from, into) => {
      from.childNodes.forEach((node) => {
        if (node.nodeType === Node.TEXT_NODE) {
          // split on normal whitespace only, so &nbsp; keeps words together
          node.textContent.split(/([ \t\n\r]+)/).forEach((part) => {
            if (!part) return;
            if (/^[ \t\n\r]+$/.test(part)) { into.appendChild(document.createTextNode(' ')); return; }
            const w = makeWord(part);
            words.push(w.inner);
            into.appendChild(w.outer);
          });
        } else if (node.nodeType === Node.ELEMENT_NODE) {
          const shell = node.cloneNode(false);
          into.appendChild(shell);
          walk(node, shell);
        }
      });
    };
    walk(el, visual);
    const sr = document.createElement('span');
    sr.className = 'sr-only';
    sr.textContent = label;
    el.replaceChildren(sr, visual);
    return words;
  }
  const maskedWord = (text) => {
    const outer = document.createElement('span'); outer.className = 'tw';
    const inner = document.createElement('span'); inner.className = 'tw__i'; inner.textContent = text;
    outer.appendChild(inner);
    return { outer, inner };
  };
  const plainWord = (text) => {
    const s = document.createElement('span'); s.className = 'w'; s.textContent = text;
    return { outer: s, inner: s };
  };
  const ms = (el) => {
    const v = getComputedStyle(el).getPropertyValue('--d').trim();
    return v.endsWith('ms') ? parseFloat(v) : v.endsWith('s') ? parseFloat(v) * 1000 : 0;
  };

  /* ---------- 3. Count-up ---------- */
  function countUp(el) {
    const final = el.textContent;
    const m = final.match(/-?\d+(?:[.,]\d+)?/);
    if (!m) return;
    const value = parseFloat(m[0].replace(',', '.'));
    const decimals = (m[0].split(/[.,]/)[1] || '').length;
    const pre = final.slice(0, m.index);
    const post = final.slice(m.index + m[0].length);
    el.style.minWidth = `${el.getBoundingClientRect().width}px`; // no width jitter while counting
    const start = performance.now() + ms(el);
    const tick = (now) => {
      const p = Math.max(0, Math.min((now - start) / 1600, 1));
      el.textContent = pre + (value * easeOutExpo(p)).toFixed(decimals).replace('.', m[0].includes(',') ? ',' : '.') + post;
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = final;
    };
    requestAnimationFrame(tick);
  }

  /* ---------- 4. Statement: words light up at the reading line ---------- */
  document.querySelectorAll('[data-words]').forEach((el) => {
    const words = splitWords(el, plainWord);
    if (reduced) { words.forEach((w) => w.classList.add('is-on')); return; }
    const wio = new IntersectionObserver((entries) => {
      entries.forEach((e) => e.target.classList.toggle('is-on', e.boundingClientRect.top < innerHeight * 0.62));
    }, { rootMargin: '0px 0px -38% 0px' });
    words.forEach((w) => wio.observe(w));
  });

  /* ---------- 5. Nav hides on scroll down, returns on scroll up ---------- */
  if (nav && !reduced) {
    let last = scrollY;
    let ticking = false;
    const update = () => {
      const y = scrollY;
      if (Math.abs(y - last) > 6) {
        const drawerOpen = document.querySelector('.drawer.is-open');
        const hide = y > last && y > innerHeight * 0.6 && !drawerOpen && !nav.matches(':focus-within');
        nav.classList.toggle('is-hidden', hide);
        last = y;
      }
      ticking = false;
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  }

  /* ---------- 6. Button label roll (fine pointers only) ---------- */
  if (finePointer && !reduced) {
    document.querySelectorAll('.btn:not(.btn--icon), .nav__link').forEach((btn) => {
      const text = [...btn.childNodes].find((n) => n.nodeType === Node.TEXT_NODE && n.textContent.trim());
      if (!text) return;
      const label = text.textContent.trim();
      const roll = document.createElement('span');
      roll.className = 'roll';
      const a = document.createElement('span'); a.textContent = label;
      const b = document.createElement('span'); b.textContent = label; b.setAttribute('aria-hidden', 'true');
      roll.append(a, b);
      btn.replaceChild(roll, text);
    });
  }

  /* ---------- 7. Reveals (run once fonts and the hero image are ready) ---------- */
  function initReveals() {
    document.querySelectorAll('[data-stagger]').forEach((group) => {
      const step = parseFloat(group.dataset.stagger) || 80;
      [...group.children].forEach((child, i) => {
        child.style.setProperty('--d', `${ms(child) + Math.min(i * step, 400)}ms`);
      });
    });

    document.querySelectorAll('[data-reveal="text"]').forEach((el) => {
      const base = ms(el);
      splitWords(el, maskedWord).forEach((w, i) => w.style.setProperty('--d', `${base + Math.min(i * 40, 600)}ms`));
    });

    const targets = [...document.querySelectorAll('.reveal, [data-reveal], [data-count]')];
    if (reduced || !('IntersectionObserver' in window)) {
      targets.forEach((t) => t.classList.add('is-in'));
      return;
    }
    const pending = new Set(targets);
    const reveal = (t) => {
      if (!pending.delete(t)) return;
      t.classList.add('is-in');
      if (t.hasAttribute('data-count') && !reduced) countUp(t);
    };
    // A fully clipped element (image unmask) is invisible to IntersectionObserver: watch its parent.
    const watched = (t) => (t.matches('[data-reveal="image"]') ? t.parentElement : t);
    const owners = new Map();
    targets.forEach((t) => { const w = watched(t); owners.set(w, [...(owners.get(w) || []), t]); });
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        (owners.get(e.target) || []).forEach(reveal);
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    owners.forEach((_, w) => io.observe(w));

    // Catch-up after jumps (End key, history restore, page reloaded mid-scroll):
    // anything at or above the reading line is revealed instead of staying hidden.
    const sweep = () => pending.forEach((t) => {
      if (watched(t).getBoundingClientRect().top < innerHeight * 0.88) reveal(t);
    });
    let timer;
    addEventListener('scroll', () => { clearTimeout(timer); timer = setTimeout(sweep, 120); }, { passive: true });
    sweep();
  }

  /* ---------- 8. Hero intro: wait briefly for fonts + hero image, then play ---------- */
  const heroImg = document.querySelector('.hero__media img');
  const imageReady = heroImg && !heroImg.complete ? heroImg.decode().catch(() => {}) : Promise.resolve();
  const fontsReady = document.fonts ? document.fonts.ready : Promise.resolve();
  const cap = new Promise((r) => setTimeout(r, 1200));
  Promise.race([Promise.all([imageReady, fontsReady]), cap]).then(() => {
    initReveals();
    requestAnimationFrame(() => root.classList.add('is-loaded'));
  });
})();
