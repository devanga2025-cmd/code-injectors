/**
 * VIBESHIELD Landing Page Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile drawer navigation toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');

  if (mobileToggle && mobileDrawer) {
    mobileToggle.addEventListener('click', () => {
      const isOpen = mobileDrawer.classList.toggle('open');
      mobileToggle.setAttribute('aria-expanded', isOpen);
    });
  }

  // Header shadow on scroll
  const siteHeader = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
      siteHeader?.classList.add('scrolled');
    } else {
      siteHeader?.classList.remove('scrolled');
    }
  }, { passive: true });

  // Hero Email Form AJAX Submission
  const heroForm = document.getElementById('heroEmailForm');
  const heroInput = document.getElementById('heroEmailInput');
  const heroBtn = document.getElementById('heroSubmitBtn');
  const formFeedback = document.getElementById('formFeedback');

  if (heroForm && heroInput) {
    heroForm.addEventListener('submit', async (e) => {
      const email = heroInput.value.trim();
      if (!email || !email.includes('@')) {
        return; // standard HTML5 validation will trigger
      }

      e.preventDefault();
      
      const originalText = heroBtn.innerHTML;
      heroBtn.disabled = true;
      heroBtn.innerHTML = '<span>Booking...</span>';

      try {
        const formData = new FormData(heroForm);
        const response = await fetch(heroForm.action || window.location.pathname, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
          },
          body: formData
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
          formFeedback.className = 'form-feedback success';
          formFeedback.innerHTML = `✓ ${data.message || 'Demo booked! We will reach out shortly.'}`;
          formFeedback.classList.remove('hidden');
          heroInput.value = '';
          setTimeout(() => {
            heroBtn.innerHTML = '<span>Booked!</span>';
          }, 400);
        } else {
          formFeedback.className = 'form-feedback error';
          formFeedback.textContent = data.message || 'Something went wrong. Please try again.';
          formFeedback.classList.remove('hidden');
          heroBtn.innerHTML = originalText;
          heroBtn.disabled = false;
        }
      } catch (err) {
        // Fallback to normal form submit if fetch fails
        heroForm.submit();
      }
    });
  }

  // Modal Functionality for "Book a Demo"
  const demoModal = document.getElementById('demoModal');
  const closeDemoModal = document.getElementById('closeDemoModal');
  const demoModalForm = document.getElementById('demoModalForm');

  window.openDemoModal = function(e) {
    if (e) e.preventDefault();
    if (demoModal) {
      demoModal.classList.add('active');
      document.body.style.overflow = 'hidden';
      const firstInput = demoModal.querySelector('input');
      if (firstInput) firstInput.focus();
    }
  };

  window.closeModal = function() {
    if (demoModal) {
      demoModal.classList.remove('active');
      document.body.style.overflow = '';
    }
  };

  if (closeDemoModal) {
    closeDemoModal.addEventListener('click', window.closeModal);
  }

  if (demoModal) {
    demoModal.addEventListener('click', (e) => {
      if (e.target === demoModal) {
        window.closeModal();
      }
    });
  }

  // Escape key closes modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && demoModal?.classList.contains('active')) {
      window.closeModal();
    }
  });

  if (demoModalForm) {
    demoModalForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = demoModalForm.querySelector('button[type="submit"]');
      const emailVal = demoModalForm.querySelector('input[name="email"]').value;
      
      submitBtn.disabled = true;
      submitBtn.textContent = 'Scheduling Demo...';

      try {
        const formData = new FormData(demoModalForm);
        const resp = await fetch('/api/lead/', {
          method: 'POST',
          body: formData
        });
        const res = await resp.json();
        if (resp.ok) {
          demoModalForm.innerHTML = `
            <div style="text-align: center; padding: 24px 0;">
              <div style="width: 52px; height: 52px; border-radius: 50%; background: #E8FAF5; color: #20C9A3; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px; font-size: 24px;">✓</div>
              <h3 style="font-size: 1.3rem; color: #304B45; margin-bottom: 8px;">Demo Request Confirmed!</h3>
              <p style="color: #6C7D8E; font-size: 0.95rem;">We have registered <strong>${emailVal}</strong>. A VIBESHIELD security specialist will send your calendar invitation shortly.</p>
              <button onclick="closeModal()" class="btn btn-primary" style="margin-top: 24px; width: 100%;">Close</button>
            </div>
          `;
        }
      } catch (err) {
        demoModalForm.submit();
      }
    });
  }
});
