document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 32) {
                navbar.classList.add('is-scrolled');
            } else {
                navbar.classList.remove('is-scrolled');
            }
        });
    }

    const revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length) {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.15 });

            revealElements.forEach((element) => observer.observe(element));
        } else {
            revealElements.forEach((element) => element.classList.add('is-visible'));
        }
    }

    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeToggleIcon');
    const storageKey = 'site-theme';

    const applyTheme = (theme) => {
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            if (themeIcon) {
                themeIcon.classList.remove('ri-moon-line');
                themeIcon.classList.add('ri-sun-line');
            }
            if (themeToggle) {
                themeToggle.setAttribute('aria-label', 'Activer le theme clair');
            }
        } else {
            document.documentElement.removeAttribute('data-theme');
            if (themeIcon) {
                themeIcon.classList.remove('ri-sun-line');
                themeIcon.classList.add('ri-moon-line');
            }
            if (themeToggle) {
                themeToggle.setAttribute('aria-label', 'Activer le theme sombre');
            }
        }
    };

    // Set initial icon based on theme set by inline script
    const initialTheme = document.documentElement.getAttribute('data-theme');
    applyTheme(initialTheme);


    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const nextTheme = isDark ? 'light' : 'dark';
            localStorage.setItem(storageKey, nextTheme);
            applyTheme(nextTheme);
        });
    }
});
