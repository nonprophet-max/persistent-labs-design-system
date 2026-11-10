import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';

const require=createRequire(import.meta.url),{chromium}=require('playwright');
if(!process.env.SITE_URL)throw new Error('Set SITE_URL to the built library root, including its deployment path.');
const base=process.env.SITE_URL.endsWith('/')?process.env.SITE_URL:`${process.env.SITE_URL}/`;
const target=new URL('products/alfred/',base).href;
const output=resolve(process.env.QA_OUTPUT||'reviews/alfred-brand/evidence');
await mkdir(output,{recursive:true});
const failures=[],checks=[],requests=[],errors=[];
const check=(ok,name,detail={})=>{checks.push({name,passed:!!ok,...detail});if(!ok)failures.push({name,...detail})};
const browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
try{
  const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  page.on('pageerror',error=>errors.push(error.message));
  page.on('requestfailed',request=>requests.push({url:request.url(),error:request.failure()?.errorText}));
  await page.goto(target);await page.evaluate(()=>document.fonts.ready);
  const root=page.locator('[data-product="alfred"]');
  for(const section of ['meet','logos','colour','type','shape','voice','applications','resources'])
    check(await root.locator(`#alfred-${section}`).count()===1,`section-${section}`);

  const first=root.locator('[data-alfred-copy]').first();
  const expected=await first.getAttribute('data-alfred-copy');
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.alfredCopied=text}}}));
  await first.focus();await page.keyboard.press('Enter');
  await root.locator('[data-alfred-status]').filter({hasText:'Copied'}).waitFor();
  check(await page.evaluate(()=>window.alfredCopied)===expected,'keyboard-copy-exact-value');
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('QA clipboard denied')}}}));
  await first.click();await root.locator('.alfred-copy-fallback').waitFor({state:'visible'});
  check(await root.locator('#alfred-copy-text').inputValue()===expected,'copy-fallback-exact-value');
  check(await root.locator('#alfred-copy-text').evaluate(el=>document.activeElement===el&&el.selectionEnd-el.selectionStart===el.value.length),'copy-fallback-selected-and-focused');
  await root.locator('[data-alfred-close-copy]').click();
  check(await first.evaluate(el=>document.activeElement===el),'copy-fallback-restores-focus');

  const text='Life, handled. Привет, Альфред. <A useful brand> — €229';
  await root.locator('#alfred-sample').fill(text);
  check(await root.locator('[data-alfred-sample-heading]').textContent()===text&&await root.locator('[data-alfred-sample-body]').textContent()===text,'editable-specimen-literal-multilingual-text');
  await root.locator('#alfred-sample').fill('');
  check((await root.locator('[data-alfred-sample-heading]').textContent()).length>0,'empty-specimen-readable-default');
  await root.locator('#alfred-sample').fill('Life, handled.');

  for(const view of ['light','dark','both']){
    const button=root.locator(`[data-alfred-view="${view}"]`);
    await button.focus();await page.keyboard.press('Enter');
    check(await button.getAttribute('aria-pressed')==='true',`asset-view-${view}-pressed`);
    for(const board of ['light','dark'])check(await root.locator(`[data-alfred-logo="${board}"]`).isVisible()===(view==='both'||view===board),`asset-view-${view}-${board}`);
  }

  const fonts=await page.evaluate(()=>({
    loaded:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family.replaceAll('"','')),
    heading:getComputedStyle(document.querySelector('[data-alfred-sample-heading]')).fontFamily,
    body:getComputedStyle(document.querySelector('[data-alfred-sample-body]')).fontFamily
  }));
  check(fonts.loaded.some(f=>f.includes('Instrument Serif'))&&fonts.heading.includes('Instrument Serif'),'instrument-serif-loaded',fonts);
  check(fonts.loaded.some(f=>f.includes('Outfit'))&&fonts.body.includes('Outfit'),'outfit-loaded',fonts);

  const downloads=await root.locator('#alfred-resources a[href]').evaluateAll(links=>links.map(a=>({href:a.href,text:a.textContent,download:a.hasAttribute('download')})));
  check(downloads.some(a=>new URL(a.href).pathname.endsWith('.zip')),'complete-skill-download-present');
  for(const item of downloads){
    if(new URL(item.href).origin!==new URL(base).origin)continue;
    const response=await page.request.get(item.href);
    check(response.status()===200,'resource-http',{href:item.href,status:response.status()});
    if(new URL(item.href).pathname.endsWith('.zip')){
      const bytes=await response.body();check(bytes[0]===0x50&&bytes[1]===0x4b,'skill-download-is-zip',{href:item.href});
    }
  }

  for(const theme of ['light','dark'])for(const width of [320,390,768,1440]){
    await page.setViewportSize({width,height:1000});
    await page.evaluate(theme=>{document.documentElement.dataset.theme=theme;scrollTo(0,0)},theme);
    const sizing=await root.evaluate(el=>({
      overflow:document.documentElement.scrollWidth>innerWidth+1,
      targets:[...el.querySelectorAll('button,input,textarea')].filter(c=>!c.hidden&&c.getBoundingClientRect().width&&getComputedStyle(c).display!=='none').map(c=>({text:c.textContent.slice(0,40),height:c.getBoundingClientRect().height,width:c.getBoundingClientRect().width})).filter(c=>c.height<43.5||c.width<43.5)
    }));
    check(!sizing.overflow&&!sizing.targets.length,'responsive-controls',{theme,width,...sizing});
    if([390,1440].includes(width)){
      await page.screenshot({path:resolve(output,`alfred-page-${theme}-${width}.png`)});
      for(const section of ['meet','logos','colour','type','shape','voice','applications','resources'])
        await root.locator(`#alfred-${section}`).screenshot({path:resolve(output,`alfred-${section}-${theme}-${width}.png`),style:'.site-bar,.mobile-bar,.skip {visibility:hidden!important}'});
    }
  }
  await page.setViewportSize({width:390,height:1000});
  await root.locator('#alfred-sample').fill('A long label and specimen '.repeat(25));
  await first.evaluate(el=>{el.textContent='Copy this colour value for the selected Alfred application'});
  await root.evaluate(el=>{
    const sizes=[...el.querySelectorAll('*')].filter(node=>[...node.childNodes].some(c=>c.nodeType===Node.TEXT_NODE&&c.textContent.trim())).map(node=>[node,parseFloat(getComputedStyle(node).fontSize)*2]);
    for(const [node,size] of sizes)node.style.setProperty('font-size',`${size}px`,'important');
  });
  check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'long-text-and-enlarged-copy-no-page-overflow');

  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
  const plain=await nojs.newPage();await plain.goto(target);
  for(const section of ['meet','logos','colour','type','shape','voice','applications','resources'])
    check(await plain.locator(`#alfred-${section}`).isVisible(),`no-js-section-${section}`);
  check(await plain.locator('#alfred-resources a[href$=".zip"]').count()>0,'no-js-skill-download');
  await nojs.close();
  check(!errors.length,'no-runtime-errors',{errors});check(!requests.length,'no-failed-requests',{requests});
  const report={date:new Date().toISOString(),target,browser:await browser.version(),passed:!failures.length,checks,failures,errors,requests,limitations:['Chromium only; no screen-reader certification.','Font loading is checked here; glyph coverage requires separate file inspection.','Screenshots require independent visual review.']};
  await writeFile(resolve(output,'alfred-qa.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({passed:report.passed,checks:checks.length,failures,errors,requests},null,2));
  process.exitCode=failures.length?1:0;
}finally{await browser.close()}
