// Actual keyboard observation through an owned, temporary Chrome profile.
import {spawn} from 'node:child_process';
import {mkdtemp, readFile, writeFile, mkdir, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join, resolve} from 'node:path';
import {createHash} from 'node:crypto';

const root = resolve('.');
const html = join(root, 'materials/ch08/practice/e05-keyboard-walkthrough.html');
const out = join(root, 'materials/ch08/browser-observation');
const profile = await mkdtemp(join(tmpdir(), 'jiaocai-e05-'));
await mkdir(out, {recursive: true});
const chrome = spawn('/usr/bin/google-chrome', ['--headless=new', '--no-first-run',
  '--disable-background-networking', '--disable-component-update', '--disable-gpu', '--disable-dev-shm-usage',
  '--remote-debugging-port=0', `--user-data-dir=${profile}`, 'about:blank'],
  {stdio: ['ignore', 'ignore', 'ignore']});
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
let socket;
try {
  let port;
  for (let i = 0; i < 100; i++) {
    try { port = (await readFile(join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]; break; }
    catch { await pause(100); }
  }
  if (!port) throw new Error('Owned Chrome startup exceeded10-second budget');
  const target = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: 'PUT'})).json();
  socket = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {socket.addEventListener('open', resolve, {once:true}); socket.addEventListener('error', reject, {once:true});});
  let id = 0;
  const pending = new Map();
  const requests = [];
  socket.addEventListener('message', event => {
    const data = JSON.parse(event.data);
    if (data.method === 'Network.requestWillBeSent') requests.push(data.params.request.url);
    if (data.id && pending.has(data.id)) {
      const {resolve, reject, timer} = pending.get(data.id); clearTimeout(timer); pending.delete(data.id);
      data.error ? reject(new Error(JSON.stringify(data.error))) : resolve(data.result);
    }
  });
  const call = (method, params={}) => new Promise((resolve, reject) => {
    const next = ++id; const timer = setTimeout(()=>{pending.delete(next);reject(new Error(`${method} timeout`));}, 10000);
    pending.set(next, {resolve, reject, timer}); socket.send(JSON.stringify({id:next, method, params}));
  });
  await call('Page.enable'); await call('Network.enable');
  await call('Emulation.setDeviceMetricsOverride', {width:1280,height:1000,deviceScaleFactor:1,mobile:false});
  await call('Page.navigate', {url:`file://${html}`});
  await pause(300);
  const version = await call('Browser.getVersion');
  await call('Page.bringToFront');
  const observe = async () => (await call('Runtime.evaluate', {expression:`JSON.stringify({id:document.activeElement.id,tag:document.activeElement.tagName,value:document.activeElement.value,focusVisible:document.activeElement.matches(':focus-visible'),outline:getComputedStyle(document.activeElement).outline,labels:[...document.querySelectorAll('label')].map(l=>({for:l.htmlFor,text:l.textContent})),values:[...document.querySelectorAll('input,textarea')].map(e=>({id:e.id,value:e.value}))})`,returnByValue:true})).result.value;
  const key = async (name, modifiers=0) => {
    const code = {Tab:9,ArrowUp:38}[name];
    await call('Input.dispatchKeyEvent',{type:'keyDown',key:name,code:name,windowsVirtualKeyCode:code,nativeVirtualKeyCode:code,modifiers});
    await call('Input.dispatchKeyEvent',{type:'keyUp',key:name,code:name,windowsVirtualKeyCode:code,nativeVirtualKeyCode:code,modifiers});
    await pause(30);
  };
  const observations = [];
  const screen = async name => {
    const data = (await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false})).data;
    const bytes=Buffer.from(data,'base64'); await writeFile(join(out,name),bytes);
    return {file:`materials/ch08/browser-observation/${name}`,sha256:createHash('sha256').update(bytes).digest('hex')};
  };
  const initial = JSON.parse(await observe());
  const captured = new Set();
  for(let i=1;i<=10;i++) {
    await key('Tab'); let state=JSON.parse(await observe());
    if(state.id==='project-id') await call('Input.insertText',{text:'SYN-01'});
    if(state.id==='topic') await call('Input.insertText',{text:'键盘练习'});
    if(state.id==='exercise-date'&&!captured.has(state.id)) await key('ArrowUp');
    if(state.id==='notes') await call('Input.insertText',{text:'仅使用虚构练习输入'});
    state=JSON.parse(await observe());
    const screenshot = captured.has(state.id) && state.focusVisible ? null : await screen(`forward-${i}.png`);
    captured.add(state.id);
    observations.push({step:i,key:'Tab',...state,screenshot});
    if(state.id==='notes') break;
  }
  const unique=[...new Set(observations.map(o=>o.id))];
  await writeFile(join(root,'materials/ch08/browser-forward-trace.json'),JSON.stringify(observations,null,2)+'\n');
  if(JSON.stringify(unique)!==JSON.stringify(['project-id','topic','exercise-date','notes'])) throw new Error(`Unexpected focus route: ${JSON.stringify(unique)}`);
  // A date control's native calendar button can retain focus inside the host
  // without matching host :focus-visible. Observe its actual outer outline.
  if(observations.some(o=>o.outline!=='rgb(23, 78, 166) solid 3px')) throw new Error('Visible keyboard outline missing');
  const reverse=[];
  for(let i=1;i<=10;i++) {await key('Tab',8);const state=JSON.parse(await observe());reverse.push({step:i,key:'Shift+Tab',...state});if(state.id==='project-id')break;}
  if(reverse.at(-1).id!=='project-id')throw new Error('Reverse navigation did not reach first field');
  if(requests.some(url=>!url.startsWith('file:')&&!url.startsWith('data:')&&url!=='about:blank'))throw new Error('External page request observed');
  const result={checks:'PASS',html_sha256:createHash('sha256').update(await readFile(html)).digest('hex'),version,route:'Owned temporary headless Chrome through loopback CDP; Chrome MCP new_page failed because its shared profile was already occupied.',initial,forward:observations,reverse,requests,actual_unique_field_route:unique,limits:'One Linux Chrome headless environment. Native date parts may consume several Tab steps. No student trial, second browser engine, screen reader or physical keyboard/human acceptance.'};
  await writeFile(join(root,'materials/ch08/browser-verification.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({checks:result.checks,fields:unique,tabs:observations.length,reverse_tabs:reverse.length,version:version.product}));
} catch (error) {
  await writeFile(join(root,'materials/ch08/browser-failure-latest.json'),JSON.stringify({checks:'FAIL',reason:String(error),scope:'Owned temporary browser; no page publication or user profile mutation.'},null,2)+'\n');
  throw error;
} finally {
  socket?.close(); chrome.kill('SIGTERM');
  await new Promise(resolve => {if(chrome.exitCode!==null)resolve();else {chrome.once('exit',resolve);setTimeout(resolve,2000);}});
  await rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:200});
}
