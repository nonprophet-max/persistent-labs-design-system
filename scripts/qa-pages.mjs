import {createRequire} from 'node:module';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {resolve,dirname,extname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const require=createRequire(import.meta.url),{chromium}=require('playwright');
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..'),dist=resolve(root,'dist-pages');
const manifest=JSON.parse(await readFile(resolve(root,'build/pages-manifest.json')));
const output=resolve(root,process.env.QA_OUTPUT||'reviews/pages/evidence');
await mkdir(output,{recursive:true});
let server,base=process.env.SITE_URL;
if(!base){
  const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.woff2':'font/woff2','.json':'application/json'};
  server=createServer(async(req,res)=>{
    try{
      let pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
      if(pathname.endsWith('/'))pathname+='index.html';
      const path=resolve(dist,'.'+pathname);
      if(!path.startsWith(dist+'/')){res.writeHead(403).end();return}
      const content=await readFile(path);res.writeHead(200,{'Content-Type':mime[extname(path)]||'text/plain'});res.end(content);
    }catch{res.writeHead(404,{'Content-Type':'text/html'});res.end(await readFile(resolve(dist,'404.html')))}
  });
  await new Promise(done=>server.listen(0,'127.0.0.1',done));
  base=`http://127.0.0.1:${server.address().port}/`;
}
const failures=[],errors=[],requests=[],matrix=[],interactions=[];
let browser;
const check=(condition,type,details={})=>{if(!condition)failures.push({type,...details})};
try{
  browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
  const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  page.on('pageerror',error=>errors.push({url:page.url(),error:error.message}));
  page.on('requestfailed',request=>requests.push({url:request.url(),error:request.failure()?.errorText}));
  for(const route of manifest){
    const response=await page.goto(new URL(route.path,base).href);
    check(response.status()===200,'http-status',{path:route.path,status:response.status()});
    await page.evaluate(()=>document.fonts.ready);
    const structure=await page.evaluate(()=>{
      const ids=[...document.querySelectorAll('[id]')].map(el=>el.id);
      return {h1:document.querySelectorAll('h1').length,duplicates:ids.filter((id,i)=>ids.indexOf(id)!==i),
        headings:[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(el=>({level:+el.tagName[1],text:el.textContent})),
        activeTop:[...document.querySelectorAll('.quick-nav [aria-current="page"]')].map(a=>a.pathname),
        products:[...document.querySelectorAll('.product-section')].map(el=>el.id),
        productLinks:[...document.querySelectorAll('.rail-nav a')].filter(a=>/^\/products\/[^/]+\/$/.test(a.pathname)).map(a=>({path:a.pathname,hash:a.hash})),
        fonts:[...document.fonts].filter(font=>font.status==='loaded').map(font=>font.family.replaceAll('"',''))};
    });
    check(structure.h1===1&&!structure.duplicates.length,'structure',{path:route.path,structure});
    for(let i=1;i<structure.headings.length;i++)check(structure.headings[i].level<=structure.headings[i-1].level+1,'heading-order',{path:route.path,heading:structure.headings[i]});
    const expectedTop=route.path.startsWith('/products/')?'/products/':route.path;
    check(JSON.stringify(structure.activeTop)===JSON.stringify(route.path==='/'?[]:[expectedTop]),'active-top',{path:route.path,actual:structure.activeTop});
    const expectedProduct=/^\/products\/([^/]+)\/$/.exec(route.path)?.[1];
    check(JSON.stringify(structure.products)===JSON.stringify(expectedProduct?[expectedProduct]:[]),'page-isolation',{path:route.path,actual:structure.products});
    check(structure.productLinks.length===5&&structure.productLinks.every(a=>!a.hash),'product-page-links',{path:route.path});
    for(const family of ['Red Hat Display','Red Hat Text','Red Hat Mono'])check(structure.fonts.includes(family),'font-loading',{path:route.path,family});
    for(const theme of ['light','dark']){
      await page.evaluate(theme=>document.documentElement.dataset.theme=theme,theme);
      for(const width of [320,390,768,1024,1440]){
        await page.setViewportSize({width,height:1000});await page.evaluate(()=>scrollTo(0,0));
        const result=await page.evaluate(()=>{
          const rgba=s=>{const a=s.match(/[\d.]+/g)?.map(Number);return a&&a.length>=3?[...a.slice(0,3),a[3]??1]:null};
          const over=(a,b)=>[...a.slice(0,3).map((v,i)=>v*a[3]+b[i]*(1-a[3])),1];
          const bg=el=>{const chain=[];for(let p=el;p;p=p.parentElement)chain.unshift(p);let c=[255,255,255,1];for(const p of chain){const b=rgba(getComputedStyle(p).backgroundColor);if(b)c=over(b,c)}return c};
          const lum=c=>c.slice(0,3).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
          const contrast=[],overflow=[],targets=[];let textPairs=0;
          for(const el of document.querySelectorAll('body *')){
            const s=getComputedStyle(el),r=el.getBoundingClientRect();
            if(!r.width||!r.height||s.visibility==='hidden'||s.display==='none'||s.opacity==='0'||el.closest('svg,.sr-only,.cover-art,script,style'))continue;
            if(r.right>innerWidth+1&&r.left>=0&&!el.closest('.table-wrap,.codeblock'))overflow.push({tag:el.tagName,class:el.className,text:el.textContent.slice(0,50)});
            if(el.matches('button,.utility,.nav-link,.quick-nav a,.page-card,.cover-products a')&&!el.disabled&&(r.width<43.5||r.height<43.5))targets.push({text:el.textContent,width:r.width,height:r.height});
            if(![...el.childNodes].some(n=>n.nodeType===Node.TEXT_NODE&&n.textContent.trim())||el.matches('script,style,option'))continue;
            const fg=rgba(s.color);if(!fg)continue;const background=bg(el),l=[lum(over(fg,background)),lum(background)].sort((a,b)=>a-b),ratio=(l[1]+.05)/(l[0]+.05);
            const threshold=parseFloat(s.fontSize)>=24||(parseFloat(s.fontSize)>=18.66&&parseFloat(s.fontWeight)>=700)?3:4.5;textPairs++;
            if(ratio+.015<threshold)contrast.push({text:el.textContent.trim().slice(0,70),ratio,threshold});
          }
          return {pageOverflow:document.documentElement.scrollWidth>innerWidth+1,overflow,contrast,targets,textPairs};
        });
        matrix.push({path:route.path,theme,width,...result});
        check(!result.pageOverflow&&!result.overflow.length&&!result.contrast.length&&!result.targets.length,'render',{path:route.path,theme,width,...result});
        if([390,1440].includes(width))await page.screenshot({path:resolve(output,`${route.path.split('/').filter(Boolean).join('-')||'home'}-${theme}-${width}.png`)});
      }
    }
    await page.setViewportSize({width:390,height:844});
    await page.getByRole('button',{name:'Contents',exact:true}).click();
    check(await page.locator('.nav-link').first().evaluate(el=>el===document.activeElement),'menu-focus',{path:route.path});
    await page.keyboard.press('Escape');
    check(await page.locator('#menu-toggle').getAttribute('aria-expanded')==='false'&&await page.locator('#menu-toggle').evaluate(el=>el===document.activeElement),'menu-escape',{path:route.path});
    interactions.push({path:route.path,check:'mobile menu focus and Escape'});
  }
  // Exercise real document navigation and history, including every product page.
  for(const route of manifest.slice(1)){
    await page.goto(base);
    const selector=route.path.startsWith('/products/')&&route.path!=='/products/'?`.rail-nav a[href="${route.path}"]`:`.quick-nav a[href="${route.path}"]`;
    if(selector.startsWith('.rail'))await page.getByRole('button',{name:'Contents',exact:true}).click();
    await page.locator(selector).click();
    await page.waitForLoadState('load');
    check(new URL(page.url()).pathname===route.path,'document-navigation',{target:route.path,url:page.url()});
    await page.reload();check(new URL(page.url()).pathname===route.path,'direct-reload',{target:route.path});
    interactions.push({path:route.path,check:'link navigation and direct reload'});
  }
  await page.setViewportSize({width:1440,height:1000});await page.goto(new URL('/products/fireflow/',base).href);
  await page.locator('#theme-toggle').click();const chosen=await page.locator('html').getAttribute('data-theme');
  await page.locator('.quick-nav a[href="/tokens/"]').click();await page.waitForLoadState('load');check(await page.locator('html').getAttribute('data-theme')===chosen,'theme-across-pages');
  await page.goBack();check(new URL(page.url()).pathname==='/products/fireflow/','browser-back');
  await page.goForward();check(new URL(page.url()).pathname==='/tokens/','browser-forward');
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('QA simulated denial'))}}));
  await page.locator('#copy-tokens').click();await page.waitForFunction(()=>document.querySelector('#copy-tokens').textContent==='Tokens selected');
  check((await page.locator('#live-status').textContent()).includes('Clipboard unavailable'),'clipboard-fallback');
  for(const kind of ['css','json']){const download=page.waitForEvent('download');await page.locator(`[data-download="${kind}"]`).click();check((await download).suggestedFilename()===`persistent-labs.tokens.${kind}`,'token-download',{kind})}
  await page.goto(new URL('/foundations/#components',base).href);await page.locator('#validate-field').click();check(await page.locator('#run-name').getAttribute('aria-invalid')==='true','field-error');
  await page.locator('#run-name').fill('Review');await page.locator('#validate-field').click();check(await page.locator('#run-name').getAttribute('aria-invalid')==='false','field-recovery');
  for(const product of ['fireflow','unfazed','lanni','privateinference','galactica']){
    await page.goto(new URL(`/products/${product}/`,base).href);const button=page.locator('.product-ui [data-demo]');const feedback=await button.getAttribute('data-demo');await button.click();check(await page.locator('#live-status').textContent()===feedback,'product-feedback',{product});
  }
  await page.goto(new URL('/products/fireflow/',base).href);await page.locator('.core-part[href="#memorytree"]').click();check(new URL(page.url()).hash==='#memorytree','nested-memory-navigation');
  check(await page.locator('.core-spec').count()===3,'fireflow-core-parts');
  check(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior)==='auto','reduced-motion');
  if(process.env.SITE_URL){
    for(const path of ['reviews/pages/review.md','src/pages.js','plugins/persistent-labs-brand/skills/persistent-labs-brand/SKILL.md','reference/original-design-bible.html','.git/config'])check((await page.request.get(new URL(path,base).href)).status()===404,'private-path',{path});
  }
  // Netlify's asynchronous hosting badge can be cancelled by deliberate page navigation.
  // Keep these observations in the report, without treating them as broken site assets.
  const hostingWarnings=requests.filter(request=>request.error==='net::ERR_ABORTED'&&new URL(request.url).origin===new URL(base).origin&&new URL(request.url).pathname==='/.netlify/scripts/hud');
  const failedSiteRequests=requests.filter(request=>!hostingWarnings.includes(request));
  check(!errors.length,'runtime-errors',{errors});check(!failedSiteRequests.length,'failed-requests',{requests:failedSiteRequests});
  const artifacts=[];for(const route of manifest)artifacts.push({path:route.path,sha256:createHash('sha256').update(await readFile(resolve(dist,'.'+route.path,'index.html'))).digest('hex')});
  const report={date:new Date().toISOString(),site:process.env.SITE_URL||'local HTTP preview',passed:failures.length===0,browser:await browser.version(),pages:manifest.length,artifacts,matrix,interactions,failures,errors,requests,hostingWarnings,limitations:['Chromium only; no Safari, Firefox or assistive-technology audit.','Contrast scan covers solid composited backgrounds.','Screenshots require separate visual review.','Artifact hashes identify the local build; Netlify adds its hosting badge to served HTML.']};
  await writeFile(resolve(output,'browser-qa.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({passed:report.passed,pages:manifest.length,renderCombinations:matrix.length,failures,errors,requests},null,2));
  process.exitCode=failures.length?1:0;
}finally{await browser?.close();if(server)await new Promise(done=>server.close(done))}
