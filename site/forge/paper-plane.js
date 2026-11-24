
const CSS = `:host{--paper:#f3efe6;--paper-2:#e9e2d5;--ink:#15130f;--muted:#6c655a;--line:#d4ccbd;--clay:#c64a2e;--cobalt:#0d2340;--ease:cubic-bezier(.22,1,.36,1);display:block;color:var(--ink);font-family:ui-sans-serif,system-ui,sans-serif;line-height:1.4}*{box-sizing:border-box}button{font:inherit;color:inherit}button:focus-visible{outline:2px solid var(--cobalt);outline-offset:3px}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
:host{--plane:#c64a2e} button{position:relative;display:inline-flex;align-items:center;gap:12px;min-height:46px;padding:10px 16px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);font:700 10px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;overflow:hidden} svg{width:28px;height:28px;overflow:visible} .status{margin:10px 0 0;color:var(--muted);font-size:12px} button.is-sent{background:var(--paper);color:var(--ink)} .plane.is-flying{animation:fly .72s cubic-bezier(.2,.8,.3,1) both}@keyframes fly{to{transform:translate(138px,-42px) rotate(18deg);opacity:0}}`;
class MosaicPaperPlane extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root=this.attachShadow({mode:'open'});
    root.innerHTML=`<style>${CSS}</style><button type="button"><svg class="plane" viewBox="0 0 28 28" aria-hidden="true"><path d="M2 13 25 3 16 25l-3-9-11-3Z" fill="var(--plane)"/></svg><span class="label"></span></button><p class="status" role="status" aria-live="polite">Ready to send.</p>`;
    const button=root.querySelector('button'), plane=root.querySelector('.plane'), label=root.querySelector('.label'), status=root.querySelector('.status'); label.textContent=this.getAttribute('label')||'Send'; let sent=false;
    const done=()=>{ sent=true; button.classList.add('is-sent'); button.disabled=true; label.textContent='Sent'; status.textContent='Sent. The action is complete.'; this.dispatchEvent(new CustomEvent('mosaic-sent',{bubbles:true,composed:true,detail:{kind:'paper-plane'}})); setTimeout(()=>{ button.classList.remove('is-sent'); button.disabled=false; plane.classList.remove('is-flying'); plane.removeAttribute('style'); label.textContent=this.getAttribute('label')||'Send'; status.textContent='Ready to send.'; sent=false; },1400); };
    button.addEventListener('click',()=>{ if(sent)return; button.disabled=true; status.textContent='Sending...'; plane.classList.add('is-flying'); setTimeout(done, 720); });
  }
}
customElements.define('mosaic-paper-plane', MosaicPaperPlane);
