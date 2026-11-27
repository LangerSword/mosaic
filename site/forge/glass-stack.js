const CSS = `:host{--paper:#f3efe6;--paper-2:#e9e2d5;--ink:#15130f;--muted:#6c655a;--line:#d4ccbd;--clay:#c64a2e;--cobalt:#0d2340;--ease:cubic-bezier(.22,1,.36,1);display:block;color:var(--ink);font-family:ui-sans-serif,system-ui,sans-serif;line-height:1.4}*{box-sizing:border-box}button{font:inherit;color:inherit}button:focus-visible{outline:2px solid var(--cobalt);outline-offset:3px}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
:host{display:block;--glass-key:var(--paper);--glass-deep:#13233e;--glass-ink:var(--paper);--glass-fill:rgba(31,53,82,.62);--glass-edge:rgba(255,255,255,.34);}
.stage{position:relative;display:grid;place-items:center;min-height:218px;overflow:hidden;background:radial-gradient(100% 100% at 30% 20%,#315b82 0%,#13233e 52%,#09111c 100%)}
.stage:before,.stage:after{content:"";position:absolute;border-radius:50%;filter:blur(1px);opacity:.7;pointer-events:none}
.stage:before{width:150px;height:150px;left:-30px;top:-40px;background:radial-gradient(circle,#f6a15a,transparent 68%)}
.stage:after{width:170px;height:170px;right:-20px;bottom:-50px;background:radial-gradient(circle,#4a7fd1,transparent 68%)}
.glass{position:relative;z-index:1;width:min(88%,286px);padding:18px;color:var(--glass-ink);background:var(--glass-fill);border:1px solid var(--glass-edge);box-shadow:inset 0 1px 0 rgba(255,255,255,.45),0 22px 50px rgba(3,10,19,.4);backdrop-filter:blur(16px) saturate(1.16);transform:perspective(700px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .25s var(--ease),background .2s var(--ease)}
.glass.is-active{background:rgba(255,255,255,.2);border-color:rgba(255,255,255,.7)}
.eyebrow{font:8px/1.3 ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase;color:rgba(241,238,230,.7)}
.glass strong{display:block;max-width:8ch;margin:18px 0 10px;font:400 clamp(2rem,5vw,3.1rem)/.86 var(--display,ui-serif);letter-spacing:-.05em;text-transform:uppercase}
.glass p{max-width:24ch;margin:0 0 17px;color:rgba(241,238,230,.78);font-size:12px;line-height:1.45}
.glass button{min-height:34px;padding:0 10px;border:1px solid rgba(255,255,255,.56);background:rgba(8,18,32,.34);color:var(--glass-ink);font:700 8px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer}
.glass button:hover{background:var(--glass-key);color:#0b1424}
.status{margin:0;padding:10px 14px;color:var(--ascii-dim,#8fa1bb);background:#09111c;font:9px/1.4 ui-monospace,monospace}
@supports not (backdrop-filter: blur(1px)){.glass{background:#1b2d45}}
@media (prefers-reduced-motion:reduce){.glass{transform:none!important}}
`;
class MosaicGlassStack extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({mode:'open'});
    root.innerHTML = `<style>${CSS}</style><div class="stage"><div class="glass"><span class="eyebrow">glass / 01</span><strong>One lens.</strong><p>A translucent object over a strong field; a solid card when blur is not available.</p><button type="button" aria-pressed="false">Select lens</button></div></div><p class="status" role="status" aria-live="polite">One object. One specular edge. One readable layer.</p>`;
    const stage = root.querySelector('.stage'), glass = root.querySelector('.glass'), button = root.querySelector('button'), status = root.querySelector('.status');
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let active = false;
    const toggle = () => {
      active = !active;
      glass.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
      button.textContent = active ? 'Lens selected' : 'Select lens';
      status.textContent = active ? 'Selected. The edge and label carry the state.' : 'One object. One specular edge. One readable layer.';
      this.dispatchEvent(new CustomEvent('mosaic-glass-select', {bubbles:true,composed:true,detail:{active}}));
    };
    button.addEventListener('click', toggle);
    if (!reduced) {
      stage.addEventListener('pointermove', (event) => {
        const rect = stage.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - .5;
        const y = (event.clientY - rect.top) / rect.height - .5;
        glass.style.setProperty('--rx', `${(-y * 6).toFixed(2)}deg`);
        glass.style.setProperty('--ry', `${(x * 9).toFixed(2)}deg`);
      });
      stage.addEventListener('pointerleave', () => { glass.style.setProperty('--rx','0deg'); glass.style.setProperty('--ry','0deg'); });
    }
  }
}
customElements.define('mosaic-glass-stack', MosaicGlassStack);
