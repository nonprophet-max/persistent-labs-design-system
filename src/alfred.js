/* Alfred interactions are scoped and optional; essential guidance works without JS. */
(() => {
  document.querySelectorAll('[data-product="alfred"]').forEach(root => {
    const status = root.querySelector('[data-alfred-status]');
    const fallback = root.querySelector('.alfred-copy-fallback');
    const fallbackText = root.querySelector('#alfred-copy-text');
    let lastCopy;
    root.querySelectorAll('[data-alfred-copy]').forEach(button => {
      button.hidden = false;
      button.addEventListener('click', async () => {
        lastCopy = button;
        const text = button.dataset.alfredCopy;
        button.disabled = true;
        status.textContent = 'Copying…';
        try {
          if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
          let timeout;
          try {
            await Promise.race([navigator.clipboard.writeText(text), new Promise((_, reject) => {
              timeout = setTimeout(() => reject(new Error('Clipboard timeout')), 1200);
            })]);
          } finally { clearTimeout(timeout); }
          fallback.hidden = true;
          status.textContent = 'Copied. Ready to paste.';
        } catch (_) {
          fallback.hidden = false;
          fallbackText.value = text;
          fallbackText.focus();
          fallbackText.select();
          status.textContent = 'Clipboard unavailable. Select and copy the text provided.';
        } finally { button.disabled = false; }
      });
    });
    root.querySelector('[data-alfred-close-copy]')?.addEventListener('click', () => {
      fallback.hidden = true;
      status.textContent = '';
      lastCopy?.focus();
    });
    const input = root.querySelector('#alfred-sample');
    input?.addEventListener('input', () => {
      const text = input.value.trim() || 'Your words here.';
      root.querySelector('[data-alfred-sample-heading]').textContent = text;
      root.querySelector('[data-alfred-sample-body]').textContent = text;
    });
    const controls = root.querySelector('[data-alfred-logo-controls]');
    if (controls) {
      controls.hidden = false;
      controls.querySelectorAll('[data-alfred-view]').forEach(button => {
        button.addEventListener('click', () => {
          const view = button.dataset.alfredView;
          controls.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
          root.querySelectorAll('[data-alfred-logo]').forEach(board => { board.hidden = view !== 'both' && board.dataset.alfredLogo !== view; });
        });
      });
    }
  });
})();
