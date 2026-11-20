/**
 * VIBESHIELD Authentication / Signup Page Scripts
 * Handles interactive tabs for GUARDIAN, SUPPLY CHAIN, and CODE
 */

document.addEventListener('DOMContentLoaded', () => {
  const categoryData = {
    'guardian': {
      heading: 'Protect your code before threats find it.',
      desc: 'Identify hidden security vulnerabilities and protect your applications from potential attacks.',
      image: '/static/images/guardian_illustration.jpg',
      alt: 'VIBESHIELD Guardian Security Illustration'
    },
    'supply-chain': {
      heading: 'Discover risks across your dependencies.',
      desc: 'Analyze third-party packages, dependencies, and external libraries to uncover hidden security risks.',
      image: '/static/images/supply_chain_illustration.jpg',
      alt: 'VIBESHIELD Supply Chain Risk Analysis Illustration'
    },
    'code': {
      heading: 'Find vulnerabilities before deployment.',
      desc: 'Scan AI-generated and vibe-coded applications to identify insecure code, exposed secrets, and potential security weaknesses.',
      image: '/static/images/code_illustration.jpg',
      alt: 'VIBESHIELD Code Vulnerability Detection Illustration'
    }
  };

  const tabs = document.querySelectorAll('.auth-tab-pill');
  const headingEl = document.getElementById('categoryHeading');
  const descEl = document.getElementById('categoryDesc');
  const illustrationEl = document.getElementById('categoryIllustration');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const selected = tab.dataset.tab;
      if (!selected || !categoryData[selected]) return;
      if (tab.classList.contains('active')) return;

      // Update Tab Pill styles
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const data = categoryData[selected];

      // Smooth crossfade animation
      if (illustrationEl) {
        illustrationEl.classList.add('fade-out');
        if (headingEl) headingEl.style.opacity = '0.4';
        if (descEl) descEl.style.opacity = '0.4';

        setTimeout(() => {
          illustrationEl.src = data.image;
          illustrationEl.alt = data.alt;
          if (headingEl) headingEl.textContent = data.heading;
          if (descEl) descEl.textContent = data.desc;

          illustrationEl.classList.remove('fade-out');
          if (headingEl) headingEl.style.opacity = '1';
          if (descEl) descEl.style.opacity = '1';
        }, 120);
      }
    });
  });

  // Preload images into browser cache for instant tab switches
  Object.values(categoryData).forEach(item => {
    const img = new Image();
    img.src = item.image;
  });
});
