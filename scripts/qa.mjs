import { createRequire } from 'node:module';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const output=resolve(root,process.env.QA_OUTPUT||'reviews/evidence');
await mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
const failures=[],warnings=[],matrix=[],errors=[];
const file=resolve(root,'index.html');
const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
page.on('pageerror',error=>errors.push(error.message));
page.on('requestfailed',request=>warnings.push({type:'request',url:request.url(),error:request.failure()?.errorText}));
await page.goto(pathToFileURL(file).href);
await page.evaluate(()=>document.fonts.ready);
const structure=await page.evaluate(()=>{
  const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);
  const duplicateIds=ids.filter((x,i)=>ids.indexOf(x)!==i);
  const brokenAnchors=[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash);
  const headings=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h=>({level:+h.tagName.slice(1),text:h.textContent}));
  return {duplicateIds,brokenAnchors,headings,h1Count:document.querySelectorAll('h1').length,fonts:[...document.fonts].map(x=>({family:x.family,status:x.status}))};
});
if(structure.duplicateIds.length||structure.brokenAnchors.length||structure.h1Count!==1)failures.push({type:'structure',...structure});
for(const family of ['Red Hat Display','Red Hat Text','Red Hat Mono']){
  if(!structure.fonts.some(f=>f.family.replaceAll('"','')===family&&f.status==='loaded'))failures.push({type:'font-not-loaded',family});
}
for(let i=1;i<structure.headings.length;i++)if(structure.headings[i].level>structure.headings[i-1].level+1)failures.push({type:'heading-order',heading:structure.headings[i]});

// Composite ancestor backgrounds and element colors. This is a targeted check,
// not a general accessibility engine; gradients/images are separately reviewed.
async function scan(){return page.evaluate(()=>{
  const rgba=s=>{const a=s.match(/[\d.]+/g)?.map(Number);return a&&a.length>=3?[...a.slice(0,3),a[3]??1]:null};
  const over=(a,b)=>[...a.slice(0,3).map((v,i)=>v*a[3]+b[i]*(1-a[3])),1];
  const bg=el=>{const chain=[];for(let p=el;p;p=p.parentElement)chain.unshift(p);let c=[255,255,255,1];for(const p of chain){const b=rgba(getComputedStyle(p).backgroundColor);if(b)c=over(b,c)}return c};
  const lum=c=>c.slice(0,3).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
  const bad=[],overflow=[],smallTargets=[];let tested=0;
  for(const el of document.querySelectorAll('body *')){
    const s=getComputedStyle(el),r=el.getBoundingClientRect();
    if(!r.width||!r.height||s.visibility==='hidden'||s.display==='none'||s.opacity==='0'||el.closest('svg,.sr-only,.cover-art,script,style'))continue;
    if(r.right>innerWidth+1&&r.left>=0&&!el.closest('.table-wrap,.codeblock'))overflow.push({tag:el.tagName,class:el.className,text:el.textContent.slice(0,50),right:r.right});
    if(el.matches('button,.utility,.nav-link,.quick-nav a')&&!el.disabled&&(r.width<43.5||r.height<43.5))smallTargets.push({text:el.textContent,width:r.width,height:r.height});
    const directText=[...el.childNodes].some(n=>n.nodeType===Node.TEXT_NODE&&n.textContent.trim());
    if(!directText||el.matches('script,style,option'))continue;
    const foreground=rgba(s.color);if(!foreground)continue;const background=bg(el);const f=over(foreground,background);const l=[lum(f),lum(background)].sort((a,b)=>a-b);const ratio=(l[1]+.05)/(l[0]+.05);const large=parseFloat(s.fontSize)>=24||(parseFloat(s.fontSize)>=18.66&&parseFloat(s.fontWeight)>=700);const threshold=large?3:4.5;tested++;
    if(ratio+.015<threshold)bad.push({text:el.textContent.trim().slice(0,70),tag:el.tagName,class:el.className,color:s.color,background,ratio,threshold});
  }
  return {pageOverflow:document.documentElement.scrollWidth>innerWidth+1,overflow,bad,smallTargets,tested};
})}

async function captureElement(locator,path){
  const viewport=page.viewportSize();
  const height=Math.ceil(await locator.evaluate(el=>el.getBoundingClientRect().height));
  if(height+100>viewport.height)await page.setViewportSize({...viewport,height:height+100});
  await locator.screenshot({path,style:'.site-bar,.mobile-bar { visibility: hidden !important; }'});
  if(height+100>viewport.height)await page.setViewportSize(viewport);
}

for(const theme of ['light','dark']){
  await page.evaluate(t=>{document.documentElement.dataset.theme=t},theme);
  for(const width of [320,390,768,1024,1440]){
    await page.setViewportSize({width,height:1000});await page.evaluate(()=>scrollTo(0,0));
    const result=await scan();matrix.push({theme,width,...result});
    if(result.pageOverflow||result.overflow.length||result.bad.length||result.smallTargets.length)failures.push({type:'render',theme,width,...result});
    if([390,1440].includes(width)){
      await page.screenshot({path:resolve(output,`cover-${theme}-${width}.png`)});
      for(const id of ['shape','fireflow','unfazed','lanni','privateinference','galactica']){
        const target=page.locator('#'+id);await target.scrollIntoViewIfNeeded();
        await captureElement(target.locator('.product-cover,.nest,.radii').first(),resolve(output,`${id}-${theme}-${width}.png`));
        if(id!=='shape')await captureElement(target.locator('.product-ui'),resolve(output,`${id}-ui-${theme}-${width}.png`));
        if(id==='fireflow')await captureElement(target.locator('.fireflow-core'),resolve(output,`fireflow-architecture-${theme}-${width}.png`));
      }
    }
  }
}
await page.setViewportSize({width:390,height:844});
await page.goto(pathToFileURL(file).href);
await page.getByRole('button',{name:'Contents',exact:true}).click();
if(await page.locator('#menu-toggle').getAttribute('aria-expanded')!=='true')failures.push({type:'menu-open'});
if(!await page.locator('.nav-link').first().evaluate(el=>el===document.activeElement))failures.push({type:'menu-focus'});
await page.keyboard.press('Escape');
if(await page.locator('#menu-toggle').getAttribute('aria-expanded')!=='false')failures.push({type:'menu-escape'});
await page.getByRole('button',{name:'Contents',exact:true}).click();
await page.locator('.nav-link[href="#shape"]').click();
if(!page.url().endsWith('#shape'))failures.push({type:'navigation'});
await page.getByRole('button',{name:'Contents',exact:true}).click();
await page.locator('#theme-toggle').click();
if(await page.locator('html').getAttribute('data-theme')!=='dark')failures.push({type:'theme-change'});
await page.reload();
if(await page.locator('html').getAttribute('data-theme')!=='dark')failures.push({type:'theme-persistence'});
await page.setViewportSize({width:1440,height:1000});
const architecture=await page.evaluate(()=>({
  products:[...document.querySelectorAll('.product-section')].map(el=>el.id),
  coreParts:[...document.querySelectorAll('#fireflow .core-spec')].map(el=>el.id),
  standaloneMemory:!!document.querySelector('.nav-link[href="#memorytree"],.portfolio-row[href="#memorytree"],section#memorytree'),
  memoryLinkTarget:document.querySelector('#memorytree')?.closest('section')?.id
}));
if(JSON.stringify(architecture.products)!==JSON.stringify(['fireflow','unfazed','lanni','privateinference','galactica'])||JSON.stringify(architecture.coreParts)!==JSON.stringify(['orchestration-engine','memorytree','flamechorus'])||architecture.standaloneMemory||architecture.memoryLinkTarget!=='fireflow')failures.push({type:'product-hierarchy',architecture});
await page.locator('#fireflow .core-part[href="#memorytree"]').click();
if(!page.url().endsWith('#memorytree'))failures.push({type:'memory-component-navigation'});
await page.locator('#fireflow [data-demo]').click();
if(!(await page.locator('#fireflow .product-ui > .ui-result').textContent()).includes('step 02'))failures.push({type:'fireflow-feedback'});
await page.locator('#validate-field').click();
if(await page.locator('#run-name').getAttribute('aria-invalid')!=='true')failures.push({type:'field-error'});
await page.locator('#run-name').fill('Design review');await page.locator('#validate-field').click();
if(await page.locator('#run-name').getAttribute('aria-invalid')!=='false')failures.push({type:'field-recovery'});
await page.locator('#privateinference [data-demo]').click();
if(!(await page.locator('#privateinference .ui-result').last().textContent()).includes('not been specified'))failures.push({type:'demo-feedback'});
await page.locator('.quick-nav a[href="#brand"]').click();
if(!page.url().endsWith('#brand'))failures.push({type:'top-navigation'});
if(await page.locator('.galactica-title[aria-label="Galactica.com"] circle[fill="#F7931A"]').count()!==1)failures.push({type:'galactica-orange-dot'});
await page.locator('#galactica [data-demo]').click();
if(!(await page.locator('#galactica .product-ui > .ui-result').textContent()).includes('No data was shared'))failures.push({type:'galactica-feedback'});
await page.locator('#copy-tokens').click();
await page.waitForFunction(()=>/copied|selected/i.test(document.querySelector('#copy-tokens').textContent),{},{timeout:5000}).catch(()=>{});
if(!(await page.locator('#copy-tokens').textContent()).match(/copied|selected/i))failures.push({type:'copy-feedback'});
await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('QA simulated denial'))}}));
await page.locator('#copy-tokens').click();
await page.waitForFunction(()=>document.querySelector('#copy-tokens').textContent==='Tokens selected');
if(!(await page.locator('#live-status').textContent()).includes('Clipboard unavailable'))failures.push({type:'copy-fallback'});
const reduced=await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior);
if(reduced!=='auto')failures.push({type:'reduced-motion'});
await page.setViewportSize({width:640,height:1000});
const narrow=await scan();if(narrow.pageOverflow)failures.push({type:'reflow-640'});
if(errors.length)failures.push({type:'runtime',errors});
const html=await readFile(file);
const report={date:new Date().toISOString(),artifact:'index.html',sha256:createHash('sha256').update(html).digest('hex'),browser:await browser.version(),passed:failures.length===0,failures,warnings,matrix,structure,architecture,interactionChecks:['mobile menu','Escape','anchor navigation','theme toggle + persistence','field error + recovery','demo feedback','copy feedback','reduced motion','640px reflow','five-product hierarchy','nested MemoryTree navigation','FireFlow feedback routing'],limitations:['Automated contrast scan uses solid composited backgrounds; does not certify WCAG conformance.','No assistive-technology, Safari or Firefox test performed.','Screenshots require visual review.']};
await writeFile(resolve(output,'browser-qa.json'),JSON.stringify(report,null,2)+'\n');
await browser.close();
console.log(JSON.stringify({passed:report.passed,failures:failures.map(f=>({type:f.type,theme:f.theme,width:f.width,bad:f.bad?.slice(0,12),overflow:f.overflow?.slice(0,5),targets:f.smallTargets?.slice(0,5)})),matrix:matrix.map(m=>({width:m.width,theme:m.theme,textPairs:m.tested})),warnings,evidence:output},null,2));
process.exitCode=failures.length?1:0;
