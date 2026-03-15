document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav-links-wrap a');
  
  function updateActiveLink() {
    const currentPath = window.location.pathname;
    const currentHash = window.location.hash;

    navLinks.forEach(link => {
      const linkHref = link.getAttribute('href');
      link.classList.remove('active');

      if (linkHref === '/' && currentPath === '/' && !currentHash) {
          // Explicitly Home (Inicio) only if no hash
          link.classList.add('active');
      } else if (linkHref.includes('#') && currentHash && linkHref.endsWith(currentHash)) {
          // Matching hash (e.g. #grid-servicios)
          link.classList.add('active');
      } else if (!linkHref.includes('#') && linkHref !== '/' && currentPath.startsWith(linkHref)) {
          // Matching other paths (e.g. /designer/)
          link.classList.add('active');
      }
    });
  }

  // Listen for hash changes (clicking nav links or manual hash entry)
  window.addEventListener('hashchange', updateActiveLink);
  // Initial check
  updateActiveLink();
  
  // Also handle click for immediate feedback (smooth scroll triggers hashchange later)
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      setTimeout(updateActiveLink, 50);
    });
  });
});
