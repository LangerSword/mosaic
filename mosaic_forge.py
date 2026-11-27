"""Deterministic, local component forge for Mosaic.

The forge emits an original starter, not a copied reference. Every component is
a framework-agnostic custom element plus thin framework adapters. The same
state machine runs in plain HTML, React, Next, Svelte, Vue and Astro, and the
motion layer can use CSS or GSAP without forking the behaviour.
"""
from __future__ import annotations

import json
from textwrap import dedent

TOKENS = """--paper:#f3efe6;--paper-2:#e9e2d5;--ink:#15130f;--muted:#6c655a;--line:#d4ccbd;--clay:#c64a2e;--cobalt:#0d2340;--ease:cubic-bezier(.22,1,.36,1);"""

COMMON_CSS = """:host{--paper:#f3efe6;--paper-2:#e9e2d5;--ink:#15130f;--muted:#6c655a;--line:#d4ccbd;--clay:#c64a2e;--cobalt:#0d2340;--ease:cubic-bezier(.22,1,.36,1);display:block;color:var(--ink);font-family:ui-sans-serif,system-ui,sans-serif;line-height:1.4}*{box-sizing:border-box}button{font:inherit;color:inherit}button:focus-visible{outline:2px solid var(--cobalt);outline-offset:3px}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}"""

KINDS = {
    "hold": {"tag": "mosaic-hold", "event": "mosaic-confirm", "label": "Hold to delete", "gsap": False},
    "segmented": {"tag": "mosaic-segmented", "event": "mosaic-select", "label": "View", "gsap": False},
    "thinking": {"tag": "mosaic-thinking", "event": "mosaic-done", "label": "Thinking", "gsap": False},
    "paper-plane": {"tag": "mosaic-paper-plane", "event": "mosaic-sent", "label": "Send", "gsap": True},
    "swipe-confirm": {"tag": "mosaic-swipe-confirm", "event": "mosaic-confirm", "label": "Swipe to delete", "gsap": True},
    "download-ring": {"tag": "mosaic-download-ring", "event": "mosaic-complete", "label": "Download", "gsap": False},
    "checklist": {"tag": "mosaic-checklist", "event": "mosaic-change", "label": "Checklist", "gsap": False},
    "ascii-field": {"tag": "mosaic-ascii-field", "event": "mosaic-ascii-change", "label": "ASCII field", "gsap": False},
    "glass-stack": {"tag": "mosaic-glass-stack", "event": "mosaic-glass-select", "label": "Glass stack", "gsap": False},
    "magnetic-link": {"tag": "mosaic-magnetic-link", "event": "mosaic-follow", "label": "Follow the signal", "gsap": False},
    "cursor-lens": {"tag": "mosaic-cursor-lens", "event": "mosaic-lens", "label": "Aa", "gsap": False},
}

STACKS = {
    "html": {"label": "Plain HTML/CSS/JS", "file": "demo.html", "skills": ["web-workflow", "frontend-design", "accessibility", "web-performance-optimization"]},
    "react": {"label": "React", "file": "index.tsx", "skills": ["react-patterns", "react-ui-patterns", "accessibility", "gsap-react"]},
    "next": {"label": "Next.js App Router", "file": "index.tsx", "skills": ["nextjs-app-router-patterns", "nextjs-best-practices", "react-patterns", "gsap-react"]},
    "svelte": {"label": "Svelte 5", "file": "index.svelte", "skills": ["sveltekit", "frontend-design", "gsap-frameworks"]},
    "vue": {"label": "Vue 3", "file": "index.vue", "skills": ["nuxt4-patterns", "frontend-design", "gsap-frameworks"]},
    "astro": {"label": "Astro", "file": "index.astro", "skills": ["astro", "frontend-design", "gsap-frameworks"]},
}


def _class_name(kind: str) -> str:
    return "Mosaic" + "".join(part.title() for part in kind.split("-"))


def _fix_core(core: str, kind: str) -> str:
    tag = KINDS[kind]["tag"]
    cls = _class_name(kind)
    core = core.replace(f"class {tag} extends", f"class {cls} extends")
    core = core.replace(f"customElements.define('{tag}', {tag})", f"customElements.define('{tag}', {cls})")
    return core


def _core(kind: str, motion: str) -> str:
    meta = KINDS[kind]
    tag = meta["tag"]
    event = meta["event"]
    label = meta["label"]
    gsap = motion == "gsap" and meta["gsap"]
    import_gsap = 'import gsap from "gsap";\n' if gsap else ""
    # The templates are deliberately plain strings: no source input is interpolated
    # into markup; labels are assigned with textContent.
    if kind == "magnetic-link":
        return f'''const CSS = `{COMMON_CSS}
:host{{display:inline-block;--mx:0px;--my:0px}} button{{position:relative;display:inline-flex;align-items:center;gap:12px;min-height:52px;padding:0 18px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);font:700 11px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;transform:translate(var(--mx),var(--my));transition:transform .18s var(--ease),background .18s}} button:hover,button:focus-visible{{background:var(--clay);border-color:var(--clay)}} .arrow{{display:inline-grid;place-items:center;width:28px;height:28px;border:1px solid currentColor;border-radius:50%;font-size:16px;transition:transform .18s}} button:hover .arrow{{transform:rotate(45deg)}} .status{{display:block;margin:10px 0 0;color:var(--muted);font-size:12px}} @media(prefers-reduced-motion:reduce){{button{{transform:none}}}}`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root = this.attachShadow({{mode:'open'}});
    root.innerHTML = `<style>${{CSS}}</style><button type="button" part="control"><span class="label"></span><span class="arrow" aria-hidden="true">↗</span></button><p class="status" role="status" aria-live="polite">Move across the button. It follows, then settles.</p>`;
    const button = root.querySelector('button'), label = root.querySelector('.label'), status = root.querySelector('.status');
    label.textContent = this.getAttribute('label') || '{label}';
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const reset = () => {{ button.style.setProperty('--mx','0px'); button.style.setProperty('--my','0px'); }};
    button.addEventListener('pointermove', e => {{
      if (reduced) return;
      const r = button.getBoundingClientRect();
      button.style.setProperty('--mx', `${{((e.clientX - (r.left + r.width / 2)) * .12).toFixed(1)}}px`);
      button.style.setProperty('--my', `${{((e.clientY - (r.top + r.height / 2)) * .18).toFixed(1)}}px`);
    }});
    button.addEventListener('pointerleave', reset);
    button.addEventListener('blur', reset);
    button.addEventListener('click', () => {{
      status.textContent = 'Signal received. The link holds.';
      this.dispatchEvent(new CustomEvent('{event}', {{bubbles:true, composed:true, detail:{{kind:'magnetic-link'}}}}));
      setTimeout(() => {{ status.textContent = 'Move across the button. It follows, then settles.'; }}, 1600);
    }});
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "cursor-lens":
        return f'''const CSS = `{COMMON_CSS}
:host{{display:block;--x:50%;--y:50%}} .stage{{position:relative;min-height:220px;display:grid;place-items:center;border:1px solid var(--line);background:var(--paper-2);overflow:hidden;cursor:crosshair}} .type{{font-family:Georgia,serif;font-size:clamp(4rem,12vw,9rem);line-height:.8;letter-spacing:-.08em;color:var(--ink);user-select:none}} .lens{{position:absolute;left:0;top:0;width:110px;height:110px;border:1px solid var(--ink);border-radius:50%;background:rgba(243,239,230,.18);backdrop-filter:blur(2px);transform:translate(var(--x),var(--y));pointer-events:none;mix-blend-mode:multiply}} .lens:after{{content:"";position:absolute;inset:9px;border:1px dashed rgba(21,19,15,.45);border-radius:50%}} .status{{margin:10px 0 0;color:var(--muted);font-size:12px}} @media(pointer:coarse){{.lens{{display:none}}}} @media(prefers-reduced-motion:reduce){{.lens{{display:none}}}}`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root = this.attachShadow({{mode:'open'}});
    root.innerHTML = `<style>${{CSS}}</style><div class="stage" part="stage"><span class="type"></span><span class="lens" aria-hidden="true"></span></div><p class="status" role="status" aria-live="polite">Move across the specimen. The lens follows the pointer.</p>`;
    const stage = root.querySelector('.stage'), type = root.querySelector('.type'), lens = root.querySelector('.lens'), status = root.querySelector('.status');
    type.textContent = this.getAttribute('label') || '{label}';
    const reset = () => {{ lens.style.setProperty('--x','50%'); lens.style.setProperty('--y','50%'); status.textContent = 'Move across the specimen. The lens follows the pointer.'; }};
    stage.addEventListener('pointermove', e => {{
      const r = stage.getBoundingClientRect();
      lens.style.setProperty('--x', `${{e.clientX - r.left - 55}}px`);
      lens.style.setProperty('--y', `${{e.clientY - r.top - 55}}px`);
      status.textContent = 'Reading through the lens.';
    }});
    stage.addEventListener('pointerleave', reset);
    stage.addEventListener('click', () => this.dispatchEvent(new CustomEvent('{event}', {{bubbles:true, composed:true, detail:{{kind:'cursor-lens'}}}})));
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "hold":
        return f'''{import_gsap}
const CSS = `{COMMON_CSS}
:host{{--size:52px}} button{{position:relative;width:100%;min-height:var(--size);padding:14px 18px;border:1px solid #5a5145;border-radius:999px;background:transparent;color:var(--paper);overflow:hidden;touch-action:manipulation;cursor:pointer;text-transform:uppercase;letter-spacing:.08em;font-size:11px;font-weight:700}}
.fill{{position:absolute;inset:0 auto 0 0;width:100%;background:var(--clay);transform:scaleX(0);transform-origin:left;z-index:0}}
.label,.status{{position:relative;z-index:1}}.status{{margin:10px 0 0;color:var(--muted);font-size:12px}}
button.is-done{{background:var(--clay);border-color:var(--clay)}}`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root = this.attachShadow({{mode:'open'}});
    root.innerHTML = `<style>${{CSS}}</style><button type="button" part="control"><span class="fill" aria-hidden="true"></span><span class="label"></span></button><p class="status" role="status" aria-live="polite">Hold to confirm.</p>`;
    const button = root.querySelector('button'), fill = root.querySelector('.fill'), labelEl = root.querySelector('.label'), status = root.querySelector('.status');
    labelEl.textContent = this.getAttribute('label') || '{label}';
    let start = 0, raf = 0, holding = false, progress = 0, done = false;
    const paint = (p) => {{ progress = Math.max(0, Math.min(1, p)); fill.style.transform = `scaleX(${{progress}})`; }};
    const finish = () => {{ holding = false; done = true; button.classList.add('is-done'); labelEl.textContent = 'Deleted'; status.textContent = 'Deleted. One action, confirmed.'; this.dispatchEvent(new CustomEvent('{event}', {{bubbles:true, composed:true, detail:{{kind:'hold'}}}})); }};
    const tick = (now) => {{ if (!holding) return; const p = Math.min(1, (now-start)/1200); paint(p); if (p >= 1) finish(); else {{ status.textContent = `Keep holding. ${{Math.round(p*100)}}%.`; raf = requestAnimationFrame(tick); }} }};
    const cancel = () => {{ if (!holding || done) return; holding = false; cancelAnimationFrame(raf); fill.style.transition='transform .3s cubic-bezier(.22,1,.36,1)'; fill.style.transform='scaleX(0)'; labelEl.textContent = this.getAttribute('label') || '{label}'; status.textContent = 'Released. Nothing was deleted.'; }};
    const begin = (e) => {{ if (done) return; if (e.type === 'pointerdown') {{ e.preventDefault(); button.setPointerCapture?.(e.pointerId); }} if (e.type === 'keydown') {{ if (e.repeat) return; e.preventDefault(); }} holding = true; start = performance.now() - progress*1200; fill.style.transition='none'; labelEl.textContent='Keep holding'; status.textContent='Keep holding.'; raf = requestAnimationFrame(tick); }};
    const stop = () => {{ if (!holding) return; cancel(); }};
    button.addEventListener('pointerdown', begin); button.addEventListener('pointerup', stop); button.addEventListener('pointercancel', cancel);
    button.addEventListener('keydown', e => {{ if (e.key === ' ' || e.key === 'Enter') begin(e); }});
    button.addEventListener('keyup', e => {{ if (e.key === ' ' || e.key === 'Enter') stop(); }});
    button.addEventListener('blur', cancel);
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "segmented":
        return f'''const CSS = `{COMMON_CSS}
:host{{--pad:4px}} .track{{display:grid;grid-template-columns:repeat(4,1fr);gap:3px;padding:var(--pad);border:1px solid var(--line);background:var(--paper-2)}}
button{{min-height:40px;border:0;background:transparent;color:var(--muted);font-size:10px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}}
button[aria-selected="true"]{{background:var(--ink);color:var(--paper)}}.read{{display:flex;justify-content:space-between;gap:12px;padding:18px 4px 0;border-bottom:1px solid var(--line);padding-bottom:12px}}strong{{font-size:30px;text-transform:uppercase}}.read span,p{{color:var(--muted);font-size:12px}}`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root = this.attachShadow({{mode:'open'}});
    root.innerHTML = `<style>${{CSS}}</style><div class="track" role="tablist" aria-label="View"><button role="tab" aria-selected="true" data-value="day">Day</button><button role="tab" aria-selected="false" tabindex="-1" data-value="week">Week</button><button role="tab" aria-selected="false" tabindex="-1" data-value="month">Month</button><button role="tab" aria-selected="false" tabindex="-1" data-value="year">Year</button></div><div class="read" aria-live="polite"><strong>Day</strong><span>24 hours · 1 lap</span></div>`;
    const buttons = [...root.querySelectorAll('button')], read = root.querySelector('.read'), values = {{day:['Day','24 hours · 1 lap'],week:['Week','7 days · 5 laps'],month:['Month','30 days · 12 laps'],year:['Year','12 months · 147 laps']}};
    const choose = (button) => {{ buttons.forEach(b => {{ const active = b === button; b.setAttribute('aria-selected', String(active)); b.tabIndex = active ? 0 : -1; }}); const [a,b] = values[button.dataset.value]; read.replaceChildren(); const strong=document.createElement('strong'); strong.textContent=a; const span=document.createElement('span'); span.textContent=b; read.append(strong,span); this.dispatchEvent(new CustomEvent('{event}', {{bubbles:true,composed:true,detail:{{value:button.dataset.value}}}})); }};
    buttons.forEach((button, i) => {{ button.addEventListener('click', () => choose(button)); button.addEventListener('keydown', e => {{ let next; if (e.key==='ArrowRight'||e.key==='ArrowDown') next=buttons[(i+1)%buttons.length]; if (e.key==='ArrowLeft'||e.key==='ArrowUp') next=buttons[(i-1+buttons.length)%buttons.length]; if (e.key==='Home') next=buttons[0]; if (e.key==='End') next=buttons[buttons.length-1]; if(next){{e.preventDefault();choose(next);next.focus();}} }}); }});
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "thinking":
        return f'''const CSS = `{COMMON_CSS}
:host{{--working:var(--clay)}} ol{{display:grid;gap:9px;margin:0 0 18px;padding:0;list-style:none;font:11px/1.4 ui-monospace,monospace}} li{{display:flex;align-items:center;gap:9px;color:var(--muted)}} li i{{display:grid;place-items:center;width:22px;height:22px;border:1px solid var(--line);font:8px/1 ui-monospace,monospace;flex:none}} li.is-done{{color:var(--ink)}} li.is-done i{{background:var(--ink);color:var(--paper);border-color:var(--ink)}} li.is-now{{color:var(--clay)}} li.is-now i{{border-color:var(--clay);color:var(--clay)}} button{{min-height:38px;padding:8px 12px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);font:700 10px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer}} p{{margin:12px 0 0;color:var(--muted);font-size:12px}}`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root = this.attachShadow({{mode:'open'}});
    root.innerHTML = `<style>${{CSS}}</style><ol aria-live="polite"><li data-step><i>01</i>Read the reference</li><li data-step><i>02</i>Name the move</li><li data-step><i>03</i>Compose the system</li><li data-step><i>04</i>Audit the result</li></ol><button type="button">Run the scout</button><p role="status" aria-live="polite">No fake percentage. Each step is real work.</p>`;
    const steps=[...root.querySelectorAll('[data-step]')], button=root.querySelector('button'), status=root.querySelector('p'); let running=false;
    button.addEventListener('click', () => {{ if(running)return; running=true; button.disabled=true; steps.forEach(s=>s.classList.remove('is-done','is-now')); let i=0; const next=()=>{{ steps.forEach((s,n)=>{{s.classList.toggle('is-done',n<i);s.classList.toggle('is-now',n===i);}}); status.textContent=`${{steps[i]?.textContent?.trim()||'Working'}}...`; i++; if(i<steps.length) setTimeout(next, 650); else setTimeout(()=>{{steps.forEach(s=>{{s.classList.add('is-done');s.classList.remove('is-now');}}); status.textContent='Done. Four steps, no fake percentage.'; running=false; button.disabled=false; button.textContent='Run again'; this.dispatchEvent(new CustomEvent('{event}',{{bubbles:true,composed:true,detail:{{steps:steps.length}}}}));}},550); }}; next(); }});
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "paper-plane":
        gsap_code = """const tl = gsap.timeline({onComplete: done});
      tl.to(plane,{x:138,y:-42,rotation:18,duration:.55,ease:'power2.in'});
      tl.to(plane,{opacity:0,duration:.16},'>-.16');
      tl.fromTo(button,{scale:1},{scale:.97,duration:.12,yoyo:true,repeat:1,ease:'power1.inOut'},0);""" if gsap else """plane.classList.add('is-flying'); setTimeout(done, 720);"""
        return f'''{import_gsap}
const CSS = `{COMMON_CSS}
:host{{--plane:#c64a2e}} button{{position:relative;display:inline-flex;align-items:center;gap:12px;min-height:46px;padding:10px 16px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);font:700 10px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;overflow:hidden}} svg{{width:28px;height:28px;overflow:visible}} .status{{margin:10px 0 0;color:var(--muted);font-size:12px}} button.is-sent{{background:var(--paper);color:var(--ink)}} .plane.is-flying{{animation:fly .72s cubic-bezier(.2,.8,.3,1) both}}@keyframes fly{{to{{transform:translate(138px,-42px) rotate(18deg);opacity:0}}}}`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root=this.attachShadow({{mode:'open'}});
    root.innerHTML=`<style>${{CSS}}</style><button type="button"><svg class="plane" viewBox="0 0 28 28" aria-hidden="true"><path d="M2 13 25 3 16 25l-3-9-11-3Z" fill="var(--plane)"/></svg><span class="label"></span></button><p class="status" role="status" aria-live="polite">Ready to send.</p>`;
    const button=root.querySelector('button'), plane=root.querySelector('.plane'), label=root.querySelector('.label'), status=root.querySelector('.status'); label.textContent=this.getAttribute('label')||'{label}'; let sent=false;
    const done=()=>{{ sent=true; button.classList.add('is-sent'); button.disabled=true; label.textContent='Sent'; status.textContent='Sent. The action is complete.'; this.dispatchEvent(new CustomEvent('{event}',{{bubbles:true,composed:true,detail:{{kind:'paper-plane'}}}})); setTimeout(()=>{{ button.classList.remove('is-sent'); button.disabled=false; plane.classList.remove('is-flying'); plane.removeAttribute('style'); label.textContent=this.getAttribute('label')||'{label}'; status.textContent='Ready to send.'; sent=false; }},1400); }};
    button.addEventListener('click',()=>{{ if(sent)return; button.disabled=true; status.textContent='Sending...'; {gsap_code} }});
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "swipe-confirm":
        gsap_code = """gsap.to(handle,{x: x, duration:.08, ease:'none'});""" if gsap else """handle.style.transform = `translateX(${x}px)`;"""
        release_code = """gsap.to(handle,{x:0,duration:.28,ease:'back.out(1.7)'});""" if gsap else """handle.style.transform='translateX(0)';"""
        return f'''{import_gsap}
const CSS = `{COMMON_CSS}
:host{{--track:#e9e2d5;--handle:#15130f}} .track{{position:relative;height:54px;border:1px solid var(--line);background:var(--track);overflow:hidden;touch-action:pan-y}} .fill{{position:absolute;inset:0 auto 0 0;width:100%;background:var(--clay);transform:scaleX(0);transform-origin:left}} .handle{{position:absolute;top:4px;left:4px;width:46px;height:46px;border:0;background:var(--handle);color:var(--paper);font:700 16px/1 ui-monospace,monospace;cursor:grab;touch-action:none;z-index:2}} .hint{{position:absolute;inset:0;display:grid;place-items:center;padding-left:50px;color:var(--muted);font:10px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;pointer-events:none}} .status{{margin:10px 0 0;color:var(--muted);font-size:12px}}`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root=this.attachShadow({{mode:'open'}});
    root.innerHTML=`<style>${{CSS}}</style><div class="track"><span class="fill" aria-hidden="true"></span><button class="handle" type="button" aria-label="Swipe to delete">→</button><span class="hint">Swipe to delete</span></div><p class="status" role="status" aria-live="polite">Drag the handle to confirm.</p>`;
    const track=root.querySelector('.track'), fill=root.querySelector('.fill'), handle=root.querySelector('.handle'), status=root.querySelector('.status'); let active=false, start=0, max=0, x=0, done=false;
    const set=(value)=>{{ x=Math.max(0,Math.min(max,value)); fill.style.transform=`scaleX(${{max?x/max:0}})`; {gsap_code} }};
    const finish=()=>{{ done=true; active=false; set(max); handle.textContent='✓'; status.textContent='Confirmed.'; this.dispatchEvent(new CustomEvent('{event}',{{bubbles:true,composed:true,detail:{{kind:'swipe-confirm'}}}})); }};
    const reset=()=>{{ if(done)return; active=false; {release_code} fill.style.transform='scaleX(0)'; x=0; status.textContent='Released. Nothing was deleted.'; }};
    handle.addEventListener('pointerdown',e=>{{ if(done)return; active=true; start=e.clientX-x; max=track.clientWidth-54; handle.setPointerCapture?.(e.pointerId); }});
    handle.addEventListener('pointermove',e=>{{ if(!active)return; set(e.clientX-start); if(max && x/max>=.8) finish(); }});
    handle.addEventListener('pointerup',()=>{{ if(!done) reset(); }});
    handle.addEventListener('pointercancel',reset);
    handle.addEventListener('keydown',e=>{{ if(e.key==='Enter'||e.key===' '){{ e.preventDefault(); if(!done) finish(); }} }});
    window.addEventListener('resize',()=>{{ max=track.clientWidth-54; if(done)set(max); }});
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "download-ring":
        return f'''const CSS = `{COMMON_CSS}
:host{{--p:0;--ring:var(--clay)}} .ring{{--deg:calc(var(--p) * 360deg);width:132px;height:132px;border-radius:50%;display:grid;place-items:center;background:conic-gradient(var(--ring) var(--deg), var(--line) 0);position:relative}} .ring:before{{content:"";position:absolute;inset:10px;border-radius:50%;background:var(--paper)}} .inner{{position:relative;z-index:1;text-align:center}} strong{{display:block;font-size:25px;line-height:1}} span,p{{font:10px/1.4 ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}} p{{margin:10px 0 0;font-size:12px;text-transform:none;letter-spacing:0}}`;
class {tag} extends HTMLElement {{
  static get observedAttributes(){{ return ['value','label']; }}
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root=this.attachShadow({{mode:'open'}});
    root.innerHTML=`<style>${{CSS}}</style><div class="ring" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="inner"><strong>0%</strong><span data-label>Download</span></div></div><p role="status" aria-live="polite">Progress comes from real bytes, not a timer.</p>`;
    this._ring=root.querySelector('.ring'); this._strong=root.querySelector('strong'); this._status=root.querySelector('p');
    this._render();
  }}
  attributeChangedCallback(){{ if(this.shadowRoot) this._render(); }}
  set progress(value) {{ this.setAttribute('value', String(Math.max(0, Math.min(100, Number(value)||0)))); }}
  get progress() {{ return Number(this.getAttribute('value')||0); }}
  _render() {{
    const value=this.progress; this._ring.style.setProperty('--p', String(value/100)); this._ring.setAttribute('aria-valuenow', String(Math.round(value))); this._strong.textContent=`${{Math.round(value)}}%`; const label=this.getAttribute('label')||'{label}'; this._ring.querySelector('[data-label]').textContent=label;
    this._status.textContent=value>=100?'Complete. The file is ready.':'Progress comes from real bytes, not a timer.';
    if(value>=100 && !this._done){{ this._done=true; this.dispatchEvent(new CustomEvent('{event}',{{bubbles:true,composed:true,detail:{{value}}}})); }}
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "checklist":
        return f'''const CSS = `{COMMON_CSS}
:host{{--done:0}} fieldset{{border:0;margin:0;padding:0}} legend{{font:700 10px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px}} label{{display:flex;align-items:center;gap:10px;min-height:38px;font-size:13px;color:var(--muted);cursor:pointer}} label:has(input:checked){{color:var(--ink)}} input{{appearance:none;width:18px;height:18px;border:1px solid var(--line);border-radius:2px;background:var(--paper)}} input:checked{{background:var(--ink);border-color:var(--ink);box-shadow:inset 0 0 0 4px var(--paper)}} .rail{{height:3px;background:var(--line);margin-top:18px}} .rail span{{display:block;height:100%;width:calc(var(--done)*1%);background:var(--clay);transition:width .25s var(--ease)}} p{{margin:9px 0 0;color:var(--muted);font-size:11px}}`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root=this.attachShadow({{mode:'open'}});
    root.innerHTML=`<style>${{CSS}}</style><fieldset><legend><span data-label>Checklist</span></legend><label><input type="checkbox" checked>Read the reference</label><label><input type="checkbox">Name the move</label><label><input type="checkbox">Compose the system</label><label><input type="checkbox">Audit the result</label></fieldset><div class="rail"><span></span></div><p role="status" aria-live="polite"></p>`;
    const boxes=[...root.querySelectorAll('input')], rail=root.querySelector('.rail span'), status=root.querySelector('p'); root.querySelector('[data-label]').textContent=this.getAttribute('label')||'{label}';
    const update=()=>{{ const done=boxes.filter(b=>b.checked).length; const pct=Math.round(done/boxes.length*100); this.style.setProperty('--done', String(pct)); rail.style.width=`${{pct}}%`; status.textContent=`${{done}} of ${{boxes.length}} complete.`; this.dispatchEvent(new CustomEvent('{event}',{{bubbles:true,composed:true,detail:{{done,total:boxes.length}}}})); }};
    boxes.forEach(b=>b.addEventListener('change',update)); update();
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "ascii-field":
        return f'''const CSS = `{COMMON_CSS}
:host{{--ascii-bg:#0b1424;--ascii-fg:#f1eee6;--ascii-dim:#7083a6;display:block;background:var(--ascii-bg);color:var(--ascii-fg);overflow:hidden}}
.field{{position:relative;min-height:210px;padding:14px;background:radial-gradient(120% 120% at 18% 0%,#183451 0%,transparent 58%),var(--ascii-bg);overflow:hidden}}
pre{{margin:0;font:11px/1.04 ui-monospace,SFMono-Regular,monospace;letter-spacing:.08em;white-space:pre;color:var(--ascii-fg);opacity:.92}}
.toolbar{{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:8px;padding-top:9px;border-top:1px solid rgba(241,238,230,.2);font:8px/1.3 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ascii-dim)}}
.toolbar strong{{color:var(--ascii-fg);font-weight:400}}
button{{min-height:28px;padding:5px 8px;border:1px solid rgba(241,238,230,.35);background:transparent;color:var(--ascii-fg);font:8px/1 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}}
button:hover{{background:var(--ascii-fg);color:var(--ascii-bg)}}
.status{{margin:0;padding:0 14px 12px;color:var(--ascii-dim);font:9px/1.4 ui-monospace,monospace}}`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root = this.attachShadow({{mode:'open'}});
    root.innerHTML = `<style>${{CSS}}</style><div class="field"><pre aria-hidden="true" data-field></pre><div class="toolbar"><span>field / <strong data-mode>sky</strong></span><button type="button" data-shift>Shift ramp</button></div></div><p class="status" role="status" aria-live="polite">A monospace field. Pointer changes the lens; the button changes the ramp.</p>`;
    const field = root.querySelector('.field'), pre = root.querySelector('[data-field]');
    const modeEl = root.querySelector('[data-mode]'), button = root.querySelector('[data-shift]');
    const status = root.querySelector('.status');
    const ramps = [' .:-=+*#%@', ' ·░▒▓█'];
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let mode = 0, pointerX = .5, pointerY = .5, raf = 0, visible = true, last = 0;
    const render = (time) => {{
      const width = Math.max(280, this.clientWidth || 480);
      const cols = Math.max(34, Math.min(72, Math.floor(width / 9)));
      const rows = 18;
      const ramp = ramps[mode];
      const phase = time * .00035;
      const lines = [];
      for (let y = 0; y < rows; y += 1) {{
        let line = '';
        for (let x = 0; x < cols; x += 1) {{
          const nx = x / Math.max(1, cols - 1), ny = y / Math.max(1, rows - 1);
          const lens = Math.max(0, 1 - Math.hypot(nx - pointerX, ny - pointerY) * 2.2);
          const value = (Math.sin(nx * 12 + phase) + Math.cos(ny * 9 - phase * .7) + lens * 1.7) / 3;
          const index = Math.max(0, Math.min(ramp.length - 1, Math.floor((value * .5 + .5) * ramp.length)));
          line += ramp[index];
        }}
        lines.push(line);
      }}
      pre.textContent = lines.join('\\n');
    }};
    const loop = (time) => {{
      if (!visible || document.hidden) return;
      if (time - last > 33) {{ render(time); last = time; }}
      raf = requestAnimationFrame(loop);
    }};
    const kick = () => {{ if (!reduced && visible && !raf) {{ last = 0; raf = requestAnimationFrame(loop); }} }};
    field.addEventListener('pointermove', (event) => {{
      const rect = field.getBoundingClientRect();
      pointerX = Math.max(0, Math.min(1, (event.clientX - rect.left) / Math.max(1, rect.width)));
      pointerY = Math.max(0, Math.min(1, (event.clientY - rect.top) / Math.max(1, rect.height)));
      if (reduced) render(0);
    }});
    field.addEventListener('pointerleave', () => {{ pointerX = .5; pointerY = .5; if (reduced) render(0); }});
    button.addEventListener('click', () => {{
      mode = (mode + 1) % ramps.length;
      modeEl.textContent = mode === 0 ? 'sky' : 'dense';
      status.textContent = mode === 0 ? 'Sky ramp. Pointer changes the lens.' : 'Dense ramp. Same field, different density.';
      this.dispatchEvent(new CustomEvent('{event}', {{bubbles:true, composed:true, detail:{{ramp: mode === 0 ? 'sky' : 'dense'}}}}));
      if (reduced) render(0); else kick();
    }});
    if (reduced) {{ render(0); return; }}
    const io = new IntersectionObserver(([entry]) => {{
      visible = entry.isIntersecting;
      if (visible) kick(); else {{ cancelAnimationFrame(raf); raf = 0; }}
    }}, {{threshold: .05}});
    io.observe(this);
    document.addEventListener('visibilitychange', () => {{ if (document.hidden) {{ cancelAnimationFrame(raf); raf = 0; }} else kick(); }});
    kick();
  }}
}}
customElements.define('{tag}', {tag});
'''
    if kind == "glass-stack":
        return f'''const CSS = `{COMMON_CSS}
:host{{display:block;--glass-key:var(--paper);--glass-deep:#13233e;--glass-ink:var(--paper);--glass-fill:rgba(31,53,82,.62);--glass-edge:rgba(255,255,255,.34);}}
.stage{{position:relative;display:grid;place-items:center;min-height:218px;overflow:hidden;background:radial-gradient(100% 100% at 30% 20%,#315b82 0%,#13233e 52%,#09111c 100%)}}
.stage:before,.stage:after{{content:"";position:absolute;border-radius:50%;filter:blur(1px);opacity:.7;pointer-events:none}}
.stage:before{{width:150px;height:150px;left:-30px;top:-40px;background:radial-gradient(circle,#f6a15a,transparent 68%)}}
.stage:after{{width:170px;height:170px;right:-20px;bottom:-50px;background:radial-gradient(circle,#4a7fd1,transparent 68%)}}
.glass{{position:relative;z-index:1;width:min(88%,286px);padding:18px;color:var(--glass-ink);background:var(--glass-fill);border:1px solid var(--glass-edge);box-shadow:inset 0 1px 0 rgba(255,255,255,.45),0 22px 50px rgba(3,10,19,.4);backdrop-filter:blur(16px) saturate(1.16);transform:perspective(700px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .25s var(--ease),background .2s var(--ease)}}
.glass.is-active{{background:rgba(255,255,255,.2);border-color:rgba(255,255,255,.7)}}
.eyebrow{{font:8px/1.3 ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase;color:rgba(241,238,230,.7)}}
.glass strong{{display:block;max-width:8ch;margin:18px 0 10px;font:400 clamp(2rem,5vw,3.1rem)/.86 var(--display,ui-serif);letter-spacing:-.05em;text-transform:uppercase}}
.glass p{{max-width:24ch;margin:0 0 17px;color:rgba(241,238,230,.78);font-size:12px;line-height:1.45}}
.glass button{{min-height:34px;padding:0 10px;border:1px solid rgba(255,255,255,.56);background:rgba(8,18,32,.34);color:var(--glass-ink);font:700 8px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer}}
.glass button:hover{{background:var(--glass-key);color:#0b1424}}
.status{{margin:0;padding:10px 14px;color:var(--ascii-dim,#8fa1bb);background:#09111c;font:9px/1.4 ui-monospace,monospace}}
@supports not (backdrop-filter: blur(1px)){{.glass{{background:#1b2d45}}}}
@media (prefers-reduced-motion:reduce){{.glass{{transform:none!important}}}}
`;
class {tag} extends HTMLElement {{
  connectedCallback() {{
    if (this.shadowRoot) return;
    const root = this.attachShadow({{mode:'open'}});
    root.innerHTML = `<style>${{CSS}}</style><div class="stage"><div class="glass"><span class="eyebrow">glass / 01</span><strong>One lens.</strong><p>A translucent object over a strong field; a solid card when blur is not available.</p><button type="button" aria-pressed="false">Select lens</button></div></div><p class="status" role="status" aria-live="polite">One object. One specular edge. One readable layer.</p>`;
    const stage = root.querySelector('.stage'), glass = root.querySelector('.glass'), button = root.querySelector('button'), status = root.querySelector('.status');
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let active = false;
    const toggle = () => {{
      active = !active;
      glass.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
      button.textContent = active ? 'Lens selected' : 'Select lens';
      status.textContent = active ? 'Selected. The edge and label carry the state.' : 'One object. One specular edge. One readable layer.';
      this.dispatchEvent(new CustomEvent('{event}', {{bubbles:true,composed:true,detail:{{active}}}}));
    }};
    button.addEventListener('click', toggle);
    if (!reduced) {{
      stage.addEventListener('pointermove', (event) => {{
        const rect = stage.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - .5;
        const y = (event.clientY - rect.top) / rect.height - .5;
        glass.style.setProperty('--rx', `${{(-y * 6).toFixed(2)}}deg`);
        glass.style.setProperty('--ry', `${{(x * 9).toFixed(2)}}deg`);
      }});
      stage.addEventListener('pointerleave', () => {{ glass.style.setProperty('--rx','0deg'); glass.style.setProperty('--ry','0deg'); }});
    }}
  }}
}}
customElements.define('{tag}', {tag});
'''
    raise ValueError(f"unknown kind: {kind}")


def _html_demo(kind: str, motion: str) -> str:
    meta = KINDS[kind]
    tag, event = meta["tag"], meta["event"]
    importmap = "" if motion != "gsap" or not meta["gsap"] else '<script type="importmap">{"imports":{"gsap":"https://cdn.jsdelivr.net/npm/gsap@3.13.0/+esm"}}</script>\n'
    return dedent(f'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Mosaic {kind}</title>
<style>body{{background:#f3efe6;color:#15130f;font-family:ui-sans-serif,system-ui,sans-serif;padding:48px;max-width:720px;margin:auto}}h1{{font:700 12px/1 ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase}}main{{margin-top:32px}}</style>
{importmap}</head>
<body><h1>Mosaic / {kind}</h1><main><{tag}></{tag}></main>
<script type="module" src="./{kind}.js"></script>
<script>document.querySelector('{tag}')?.addEventListener('{event}', e => console.log('{event}', e.detail));</script>
</body></html>''')


def _react_wrapper(kind: str, nextjs: bool) -> str:
    meta = KINDS[kind]
    tag, event, label = meta["tag"], meta["event"], meta["label"]
    client = '"use client";\n\n' if nextjs else ''
    if kind == "download-ring":
        props = 'label = "Download", value = 0'
        types = '{ label?: string; value?: number; onEvent?: (detail: unknown) => void }'
        effect = '''const el = ref.current;
    if (el) el.progress = value;
    if (!el) return;
    const handler = (event: Event) => onEvent?.((event as CustomEvent).detail);
    el.addEventListener("''' + event + '''", handler);
    return () => el.removeEventListener("''' + event + '''", handler);'''
        deps = '[onEvent, value]'
        attrs = 'ref, label, progress: value'
    else:
        props = 'label = ' + json.dumps(label)
        types = '{ label?: string; onEvent?: (detail: unknown) => void }'
        effect = '''const el = ref.current;
    if (!el) return;
    const handler = (event: Event) => onEvent?.((event as CustomEvent).detail);
    el.addEventListener("''' + event + '''", handler);
    return () => el.removeEventListener("''' + event + '''", handler);'''
        deps = '[onEvent]'
        attrs = 'ref, label'
    return dedent(f'''{client}import React, {{ useEffect, useRef }} from "react";
import "./{kind}.js";

export default function Mosaic{kind.title().replace("-", "")}({{ {props}, onEvent }}: {types}) {{
  const ref = useRef<HTMLElement | null>(null);
  useEffect(() => {{
    {effect}
  }}, {deps});
  return React.createElement("{tag}", {{ {attrs} }});
}}
''')


def _svelte_wrapper(kind: str) -> str:
    meta = KINDS[kind]
    tag, event, label = meta["tag"], meta["event"], meta["label"]
    return dedent(f'''<script>
  import {{ onMount }} from "svelte";
  import "./{kind}.js";
  let {{ label = {json.dumps(label)}, onEvent }} = $props();
  let el;
  onMount(() => {{
    const handler = (event) => onEvent?.(event.detail);
    el?.addEventListener("{event}", handler);
    return () => el?.removeEventListener("{event}", handler);
  }});
</script>
<{tag} bind:this={{el}} {{label}}></{tag}>
''')


def _vue_wrapper(kind: str) -> str:
    meta = KINDS[kind]
    tag, event, label = meta["tag"], meta["event"], meta["label"]
    return dedent(f'''<script setup>
import {{ onMounted, onBeforeUnmount, ref }} from "vue";
import "./{kind}.js";
const props = defineProps({{ label: {{ type: String, default: {json.dumps(label)} }} }});
const emit = defineEmits(["event"]);
const el = ref(null);
let handler;
onMounted(() => {{
  handler = (event) => emit("event", event.detail);
  el.value?.addEventListener("{event}", handler);
}});
onBeforeUnmount(() => el.value?.removeEventListener("{event}", handler));
</script>
<template><{tag} ref="el" :label="props.label"></{tag}></template>
''')


def _astro_wrapper(kind: str) -> str:
    meta = KINDS[kind]
    tag, event, label = meta["tag"], meta["event"], meta["label"]
    return dedent(f'''---
import "./{kind}.js";
---
<{tag} label={json.dumps(label)}></{tag}>
<script>
  document.querySelector("{tag}")?.addEventListener("{event}", (event) => {{
    console.log("{event}", event.detail);
  }});
</script>
''')


def forge(kind: str, stack: str = "html", motion: str = "css", brief: str = "") -> str:
    if kind not in KINDS:
        raise ValueError(f"kind must be one of: {', '.join(KINDS)}")
    if stack not in STACKS and stack != "all":
        raise ValueError(f"stack must be one of: {', '.join(list(STACKS) + ['all'])}")
    if motion not in {"css", "gsap"}:
        raise ValueError("motion must be css or gsap")
    brief = (brief or "").strip()[:600]
    targets = list(STACKS) if stack == "all" else [stack]
    meta = KINDS[kind]
    files = [{"path": f"{kind}.js", "language": "javascript", "content": _fix_core(_core(kind, motion), kind)}]
    if "html" in targets:
        files.append({"path": f"{kind}.html", "language": "html", "content": _html_demo(kind, motion)})
    if "react" in targets:
        path = "index.react.tsx" if "next" in targets else "index.tsx"
        files.append({"path": path, "language": "tsx", "content": _react_wrapper(kind, False)})
    if "next" in targets:
        path = "index.next.tsx" if "react" in targets else "index.tsx"
        files.append({"path": path, "language": "tsx", "content": _react_wrapper(kind, True)})
    if "svelte" in targets:
        files.append({"path": "index.svelte", "language": "svelte", "content": _svelte_wrapper(kind)})
    if "vue" in targets:
        files.append({"path": "index.vue", "language": "vue", "content": _vue_wrapper(kind)})
    if "astro" in targets:
        files.append({"path": "index.astro", "language": "astro", "content": _astro_wrapper(kind)})
    deps = ["gsap"] if motion == "gsap" and meta["gsap"] else []
    return json.dumps({
        "ok": True,
        "kind": kind,
        "stack": stack,
        "motion": motion,
        "brief": brief,
        "files": files,
        "deps": deps,
        "notes": [
            "The core is a custom element; the framework files are thin event adapters.",
            "The forge emits a starter, not a copied reference. Verify it in the target app.",
            "GSAP is used only where it earns its weight; the core remains functional without it.",
        ],
        "acceptance": [
            "The component works with pointer and keyboard.",
            "prefers-reduced-motion keeps the state change and removes the decoration.",
            "The event name is stable across all framework adapters.",
            "Labels are set with textContent; no user text is injected as HTML.",
            "The target framework builds with no new global CSS.",
        ],
    }, ensure_ascii=False, indent=2)


TOOL_SPECS = [
    {
        "name": "mosaic_forge",
        "handler": None,
        "emoji": "🛠️",
        "description": "Generate an original component starter for HTML, React, Next, Svelte, Vue or Astro, with CSS or GSAP motion.",
        "schema": {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": sorted(KINDS)},
                "stack": {"type": "string", "enum": list(STACKS) + ["all"]},
                "motion": {"type": "string", "enum": ["css", "gsap"]},
                "brief": {"type": "string"},
            },
            "required": ["kind"],
        },
    },
    {
        "name": "mosaic_stacks",
        "handler": None,
        "emoji": "🧱",
        "description": "Return the framework matrix and the Hermes web skills that pair with each target.",
        "schema": {"type": "object", "properties": {}, "required": []},
    },
]
