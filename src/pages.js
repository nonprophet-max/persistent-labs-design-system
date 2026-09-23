(()=>{
  const root=document.documentElement,rail=document.querySelector('.rail'),menu=document.querySelector('#menu-toggle');
  const announce=message=>{document.querySelector('#live-status').textContent=message};
  function closeMenu(returnFocus=false){rail.classList.remove('open');menu.setAttribute('aria-expanded','false');if(returnFocus)menu.focus()}
  menu.addEventListener('click',()=>{const open=rail.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));if(open)rail.querySelector('.nav-link').focus()});
  document.addEventListener('keydown',event=>{
    if(!rail.classList.contains('open'))return;
    if(event.key==='Escape'){closeMenu(true);return}
    if(event.key==='Tab'){
      const controls=[menu,...rail.querySelectorAll('a,button')],first=controls[0],last=controls.at(-1);
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus()}
      if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus()}
    }
  });
  document.querySelectorAll('.nav-link,.quick-nav a').forEach(link=>link.addEventListener('click',()=>{
    closeMenu();
    if(link.pathname===location.pathname&&link.hash){const target=document.getElementById(decodeURIComponent(link.hash.slice(1)));if(target){target.setAttribute('tabindex','-1');target.focus({preventScroll:true})}}
  }));
  document.addEventListener('click',event=>{if(rail.classList.contains('open')&&!rail.contains(event.target)&&!menu.contains(event.target))closeMenu()});
  matchMedia('(min-width:901px)').addEventListener('change',event=>{if(event.matches)closeMenu()});
  const themeButton=document.querySelector('#theme-toggle');
  function setTheme(theme){root.dataset.theme=theme;themeButton.textContent=theme==='dark'?'Switch to light view':'Switch to dark view';themeButton.setAttribute('aria-pressed',String(theme==='dark'));try{localStorage.setItem('persistent-bible-theme',theme)}catch{}}
  themeButton.addEventListener('click',()=>setTheme(root.dataset.theme==='dark'?'light':'dark'));
  let saved;try{saved=localStorage.getItem('persistent-bible-theme')}catch{}setTheme(saved==='dark'?'dark':'light');
  const localLinks=[...document.querySelectorAll('.nav-link')].filter(link=>link.pathname===location.pathname&&link.hash);
  if('IntersectionObserver' in window&&localLinks.length){
    const observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting)localLinks.forEach(link=>{if(link.hash==='#'+entry.target.id)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current')})}},{rootMargin:'-12% 0px -65% 0px',threshold:0});
    document.querySelectorAll('section[id]').forEach(section=>observer.observe(section));
  }
  const copyButton=document.querySelector('#copy-tokens');
  copyButton?.addEventListener('click',async()=>{
    const text=document.querySelector('#tokens-src').textContent;
    try{copyButton.textContent='Copying…';await Promise.race([navigator.clipboard.writeText(text),new Promise((_,reject)=>setTimeout(()=>reject(new Error('Clipboard timeout')),1200))]);copyButton.textContent='Tokens copied';announce('CSS tokens copied to clipboard.')}
    catch{const range=document.createRange();range.selectNodeContents(document.querySelector('#tokens-src'));const selection=getSelection();selection.removeAllRanges();selection.addRange(range);copyButton.textContent='Tokens selected';announce('Clipboard unavailable. Tokens selected. Use your system copy shortcut.')}
    setTimeout(()=>copyButton.textContent='Copy CSS tokens',2500);
  });
  document.querySelectorAll('[data-demo]').forEach(button=>button.addEventListener('click',()=>{const feedback=button.closest('.product-ui,.specimen').querySelector(':scope > .ui-result,:scope > .demo-feedback');feedback.textContent=button.dataset.demo;announce(button.dataset.demo)}));
  document.querySelector('#validate-field')?.addEventListener('click',()=>{const input=document.querySelector('#run-name'),hint=document.querySelector('#run-hint');const invalid=!input.value.trim();input.setAttribute('aria-invalid',String(invalid));hint.classList.toggle('error',invalid);hint.textContent=invalid?'Enter a run name to continue.':'Example validated. No workflow has been created.';announce(hint.textContent);if(invalid)input.focus()});
  document.querySelectorAll('[data-download]').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();const kind=link.dataset.download;const content=kind==='css'?document.querySelector('#tokens-src').textContent:document.querySelector('#token-json').textContent;const url=URL.createObjectURL(new Blob([content],{type:kind==='css'?'text/css':'application/json'}));const anchor=document.createElement('a');anchor.href=url;anchor.download='persistent-labs.tokens.'+kind;anchor.click();setTimeout(()=>URL.revokeObjectURL(url),1000);announce('Token download started.')}));
})();
