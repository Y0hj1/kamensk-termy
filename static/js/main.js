// Main JavaScript for VODA Spa website
// Goals:
// - no JS errors (mobile menu + modals must work)
// - small, predictable behaviour

document.addEventListener('DOMContentLoaded', () => {
  initHeroSlider();
  initMobileMenu();
  initHeaderOffset();
  initGalleryLightbox();
  initHeaderScrollState();
  initBuyModal();
});

// ------------------------------
// Hero slider (dots + auto)
// ------------------------------
function initHeroSlider() {
  const slider = document.querySelector('.hero-slider');
  if (!slider) return;

  const slides = Array.from(slider.querySelectorAll('.slide'));
  const dots = Array.from(slider.querySelectorAll('.dot'));
  if (slides.length <= 1) {
    // still ensure videos (if any) are paused/played correctly
    syncSlideVideos(slides);
    return;
  }

  let index = slides.findIndex(s => s.classList.contains('active'));
  if (index < 0) index = 0;

  let timer = null;
  const INTERVAL_MS = 6000;

  const setActive = (i) => {
    slides.forEach((s, n) => s.classList.toggle('active', n === i));
    dots.forEach((d, n) => d.classList.toggle('active', n === i));
    syncSlideVideos(slides);
    const activeSlide = slides[i];
    const video = activeSlide ? activeSlide.querySelector('video') : null;
    if (video) {
      stop();
      video.addEventListener('ended', function onVideoEnded() {
        video.removeEventListener('ended', onVideoEnded);
        next();
        start();
      }, { once: true });
    } else {
      start();
    }
  };

  const next = () => {
    index = (index + 1) % slides.length;
    setActive(index);
  };

  const prev = () => {
    index = (index - 1 + slides.length) % slides.length;
    setActive(index);
  };

  const start = () => {
    if (timer) return;
    timer = setInterval(next, INTERVAL_MS);
  };
  const stop = () => {
    if (!timer) return;
    clearInterval(timer);
    timer = null;
  };

  // dots navigation
  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      stop();
      index = i;
      setActive(index);
      start();
    });
  });

  // pause on hover (desktop)
  slider.addEventListener('mouseenter', stop);
  slider.addEventListener('mouseleave', start);

  // swipe on touch devices
  let startX = 0;
  let startY = 0;
  let tracking = false;
  let swiping = false;

  const onTouchStart = (e) => {
    if (!e.touches || e.touches.length !== 1) return;
    const t = e.touches[0];
    startX = t.clientX;
    startY = t.clientY;
    tracking = true;
    swiping = false;
    stop();
  };

  const onTouchMove = (e) => {
    if (!tracking || !e.touches || e.touches.length !== 1) return;
    const t = e.touches[0];
    const dx = t.clientX - startX;
    const dy = t.clientY - startY;

    // decide if this is a horizontal swipe (allow vertical scroll otherwise)
    if (!swiping) {
      if (Math.abs(dx) > 10 && Math.abs(dx) > Math.abs(dy)) {
        swiping = true;
      } else if (Math.abs(dy) > 10 && Math.abs(dy) > Math.abs(dx)) {
        tracking = false; // user is scrolling vertically
        start();
        return;
      }
    }

    if (swiping) {
      // prevent page from scrolling while swiping slider
      e.preventDefault();
    }
  };

  const onTouchEnd = (e) => {
    if (!tracking) return;
    tracking = false;

    // If we didn't detect a horizontal swipe, resume autoplay
    if (!swiping) {
      start();
      return;
    }

    // Use changedTouches for end position
    const t = (e.changedTouches && e.changedTouches[0]) ? e.changedTouches[0] : null;
    if (!t) {
      start();
      return;
    }
    const dx = t.clientX - startX;

    const THRESHOLD = 50;
    if (dx <= -THRESHOLD) {
      next();
    } else if (dx >= THRESHOLD) {
      prev();
    }
    start();
  };

  slider.addEventListener('touchstart', onTouchStart, { passive: true });
  slider.addEventListener('touchmove', onTouchMove, { passive: false });
  slider.addEventListener('touchend', onTouchEnd, { passive: true });
  slider.addEventListener('touchcancel', onTouchEnd, { passive: true });

    // pause when tab hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop();
    else start();
  });

  setActive(index);
  const hasVideo = slider.querySelector('.slide.active video');
  if (!hasVideo) start();
}

function syncSlideVideos(slides) {
  slides.forEach(slide => {
    const v = slide.querySelector('video');
    if (!v) return;
    if (slide.classList.contains('active')) {
      v.play().catch(() => {});
    } else {
      v.pause();
      try { v.currentTime = 0; } catch (_) {}
    }
  });
}

// ------------------------------
// Mobile menu (burger)
// ------------------------------
function initMobileMenu() {
  const toggle = document.querySelector('.mobile-menu-toggle');
  const panel = document.getElementById('mobileMenuPanel');
  const overlay = document.getElementById('mobileMenuOverlay');
  const closeBtn = document.getElementById('mobileMenuClose');

  if (!toggle || !panel || !overlay) return;

  toggle.setAttribute('aria-label', 'Меню');
  toggle.setAttribute('aria-expanded', 'false');

  const open = () => {
    overlay.hidden = false;
    panel.hidden = false;
    panel.setAttribute('aria-hidden', 'false');
    toggle.classList.add('active');
    document.body.classList.add('menu-open');
    toggle.setAttribute('aria-expanded', 'true');
  };

  const close = () => {
    overlay.hidden = true;
    panel.hidden = true;
    panel.setAttribute('aria-hidden', 'true');
    toggle.classList.remove('active');
    document.body.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    const willOpen = panel.hidden === true;
    if (willOpen) open(); else close();
  });

  // close on overlay click
  overlay.addEventListener('click', close);

  // close on close button
  if (closeBtn) closeBtn.addEventListener('click', close);

  // close on link click
  panel.querySelectorAll('a').forEach(a => a.addEventListener('click', close));

  // close on Esc
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });
}

// ------------------------------
// Gallery lightbox
// ------------------------------
function initGalleryLightbox() {
  const items = document.querySelectorAll('.gallery-item');
  if (!items.length) return;

  items.forEach(item => {
    item.addEventListener('click', () => {
      const img = item.querySelector('img');
      if (!img) return;
      openLightbox(img.src, img.alt || '');
    });
  });
}

function openLightbox(src, alt) {
  const overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  overlay.innerHTML = `
    <div class="lightbox-content" role="dialog" aria-modal="true">
      <img class="lightbox-image" src="${src}" alt="${escapeHtml(alt)}">
      <button class="lightbox-close" aria-label="Закрыть">&times;</button>
    </div>
  `;

  document.body.appendChild(overlay);
  document.body.style.overflow = 'hidden';

  const close = () => {
    document.body.style.overflow = '';
    overlay.remove();
    document.removeEventListener('keydown', onEsc);
  };
  const onEsc = (e) => { if (e.key === 'Escape') close(); };
  document.addEventListener('keydown', onEsc);

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) close();
  });
  overlay.querySelector('.lightbox-close')?.addEventListener('click', close);
}

function escapeHtml(str) {
  return String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

// ------------------------------
// Header scrolled state
// ------------------------------
function initHeaderScrollState() {
  const header = document.querySelector('.header');
  if (!header) return;

  const onScroll = () => {
    header.classList.toggle('scrolled', window.scrollY > 10);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

// ------------------------------
// Buy modal ("Купить")
// ------------------------------
function initBuyModal() {
  const openBtn = document.getElementById('openBuy');
  const modal = document.getElementById('buyModal');
  const backdrop = document.getElementById('buyBackdrop');
  const closeBtn = document.getElementById('buyClose');
  if (!openBtn || !modal) return;

  const open = () => {
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
  };
  const close = () => {
    modal.hidden = true;
    document.body.style.overflow = '';
  };

  openBtn.addEventListener('click', (e) => { e.preventDefault(); open(); });
  backdrop?.addEventListener('click', close);
  closeBtn?.addEventListener('click', close);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !modal.hidden) close();
  });

  // close when user clicks a link inside modal
  modal.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
}


// ------------------------------
// Header offset (for fixed header)
// ------------------------------
function initHeaderOffset() {
  const header = document.querySelector('.header');
  if (!header) return;

  const apply = () => {
    // offset is the full header height
    const h = header.getBoundingClientRect().height;
    document.documentElement.style.setProperty('--header-offset', `${Math.ceil(h)}px`);
  };

  // Apply after layout, then on resize/orientation changes
  requestAnimationFrame(apply);
  window.addEventListener('resize', () => requestAnimationFrame(apply));
  window.addEventListener('orientationchange', () => setTimeout(apply, 150));
}
