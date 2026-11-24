
const CSS = `:host{--paper:#f3efe6;--paper-2:#e9e2d5;--ink:#15130f;--muted:#6c655a;--line:#d4ccbd;--clay:#c64a2e;--cobalt:#0d2340;--ease:cubic-bezier(.22,1,.36,1);display:block;color:var(--ink);font-family:ui-sans-serif,system-ui,sans-serif;line-height:1.4}*{box-sizing:border-box}button{font:inherit;color:inherit}button:focus-visible{outline:2px solid var(--cobalt);outline-offset:3px}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
:host{--track:#e9e2d5;--handle:#15130f} .track{position:relative;height:54px;border:1px solid var(--line);background:var(--track);overflow:hidden;touch-action:pan-y} .fill{position:absolute;inset:0 auto 0 0;width:100%;background:var(--clay);transform:scaleX(0);transform-origin:left} .handle{position:absolute;top:4px;left:4px;width:46px;height:46px;border:0;background:var(--handle);color:var(--paper);font:700 16px/1 ui-monospace,monospace;cursor:grab;touch-action:none;z-index:2} .hint{position:absolute;inset:0;display:grid;place-items:center;padding-left:50px;color:var(--muted);font:10px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;pointer-events:none} .status{margin:10px 0 0;color:var(--muted);font-size:12px}`;
class MosaicSwipeConfirm extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root=this.attachShadow({mode:'open'});
    root.innerHTML=`<style>${CSS}</style><div class="track"><span class="fill" aria-hidden="true"></span><button class="handle" type="button" aria-label="Swipe to delete">→</button><span class="hint">Swipe to delete</span></div><p class="status" role="status" aria-live="polite">Drag the handle to confirm.</p>`;
    const track=root.querySelector('.track'), fill=root.querySelector('.fill'), handle=root.querySelector('.handle'), status=root.querySelector('.status'); let active=false, start=0, max=0, x=0, done=false;
    const set=(value)=>{ x=Math.max(0,Math.min(max,value)); fill.style.transform=`scaleX(${max?x/max:0})`; handle.style.transform = `translateX(${x}px)`; };
    const finish=()=>{ done=true; active=false; set(max); handle.textContent='✓'; status.textContent='Confirmed.'; this.dispatchEvent(new CustomEvent('mosaic-confirm',{bubbles:true,composed:true,detail:{kind:'swipe-confirm'}})); };
    const reset=()=>{ if(done)return; active=false; handle.style.transform='translateX(0)'; fill.style.transform='scaleX(0)'; x=0; status.textContent='Released. Nothing was deleted.'; };
    handle.addEventListener('pointerdown',e=>{ if(done)return; active=true; start=e.clientX-x; max=track.clientWidth-54; handle.setPointerCapture?.(e.pointerId); });
    handle.addEventListener('pointermove',e=>{ if(!active)return; set(e.clientX-start); if(max && x/max>=.8) finish(); });
    handle.addEventListener('pointerup',()=>{ if(!done) reset(); });
    handle.addEventListener('pointercancel',reset);
    handle.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); if(!done) finish(); } });
    window.addEventListener('resize',()=>{ max=track.clientWidth-54; if(done)set(max); });
  }
}
customElements.define('mosaic-swipe-confirm', MosaicSwipeConfirm);
