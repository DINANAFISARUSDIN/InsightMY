/* ================================================
   InsightMY Analysis — Main Script (Flask Version)
   ================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Dark Mode ── */
  const THEME_KEY = 'insightmy-theme';
  const html = document.documentElement;

  const applyTheme = (theme) => {
    html.setAttribute('data-theme', theme);
    document.querySelectorAll('.btn-darkmode').forEach(btn => {
      const icon = btn.querySelector('i');
      if (!icon) return;
      if (theme === 'dark') {
        icon.className = 'fas fa-sun';
        btn.setAttribute('title', 'Light mode');
      } else {
        icon.className = 'fas fa-moon';
        btn.setAttribute('title', 'Dark mode');
      }
    });
    localStorage.setItem(THEME_KEY, theme);
  };

  const savedTheme = localStorage.getItem(THEME_KEY) || 'light';
  applyTheme(savedTheme);

  document.querySelectorAll('.btn-darkmode').forEach(btn => {
    btn.addEventListener('click', () => {
      const current = html.getAttribute('data-theme') || 'light';
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  });

  /* ── Active Nav Link (Dibetulkan untuk Flask Routes) ── */
  const currentPath = window.location.pathname; // Mengambil path semasa (Contoh: /about atau /dashboard atau /)
  
  document.querySelectorAll('.nav-link').forEach(link => {
    // Ambil nilai path daripada attribute href
    const hrefValue = link.getAttribute('href');
    
    // Pastikan class active dibuang dahulu untuk proses pembersihan
    link.classList.remove('active');
    
    // Logik semakan: Jika path URL semasa tepat sepadan dengan nilai href, aktifkan menu tersebut
    if (currentPath === hrefValue) {
      link.classList.add('active');
    }
    // Skenario tambahan untuk mengendalikan root domain '/' jika terdapat perbezaan penulisan
    else if (currentPath === '/' && (hrefValue === '/' || hrefValue === 'index.html')) {
      link.classList.add('active');
    }
  });

  /* ── AOS Init ── */
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 650,
      easing: 'ease-out-cubic',
      once: true,
      offset: 60,
    });
  }

  /* ── Scroll To Top ── */
  const scrollBtn = document.getElementById('scrollTop');
  if (scrollBtn) {
    window.addEventListener('scroll', () => {
      scrollBtn.classList.toggle('visible', window.scrollY > 400);
    });
    scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ── Animated Counter ── */
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = +el.getAttribute('data-count');
          const suffix = el.getAttribute('data-suffix') || '';
          const duration = 1400;
          const start = performance.now();
          const animate = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.floor(ease * target).toLocaleString() + suffix;
            if (progress < 1) requestAnimationFrame(animate);
          };
          const animateWrapper = (now) => animate(now);
          requestAnimationFrame(animateWrapper);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach(el => observer.observe(el));
  }

  /* ── Animated Bars ── */
  const bars = document.querySelectorAll('.bar-fill[data-width]');
  if (bars.length) {
    const barObs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.width = entry.target.getAttribute('data-width');
          barObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    bars.forEach(b => {
      b.style.width = '0';
      barObs.observe(b);
    });
  }

  /* ── Dashboard Loader ── */
  const loader = document.getElementById('dashboardLoader');
  const iframeWrap = document.getElementById('dashboardIframeWrap');
  const iframe = document.getElementById('powerBiFrame');
  if (loader && iframeWrap && iframe) {
    setTimeout(() => {
      loader.style.display = 'none';
      iframeWrap.classList.add('loaded');
    }, 2200);

    iframe.addEventListener('load', () => {
      loader.style.display = 'none';
      iframeWrap.classList.add('loaded');
    });
  }

  /* ── Navbar Collapse on Link Click (mobile) ── */
  document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
    link.addEventListener('click', () => {
      const toggler = document.querySelector('.navbar-toggler');
      const navCollapse = document.querySelector('.navbar-collapse');
      if (navCollapse && navCollapse.classList.contains('show')) {
        toggler && toggler.click();
      }
    });
  });

  /* ── Insight card number animation (insights page) ── */
  const insightNums = document.querySelectorAll('.insight-anim-num');
  if (insightNums.length) {
    const numObs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.style.opacity = '1';
          e.target.style.transform = 'translateY(0)';
          numObs.unobserve(e.target);
        }
      });
    }, { threshold: 0.3 });
    insightNums.forEach(n => {
      n.style.opacity = '0';
      n.style.transform = 'translateY(12px)';
      n.style.transition = 'all .5s ease';
      numObs.observe(n);
    });
  }

});