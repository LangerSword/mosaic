const CSS = `:host{--paper:#f3efe6;--paper-2:#e9e2d5;--ink:#15130f;--muted:#6c655a;--line:#d4ccbd;--clay:#c64a2e;--cobalt:#0d2340;--ease:cubic-bezier(.22,1,.36,1);display:block;color:var(--ink);font-family:ui-sans-serif,system-ui,sans-serif;line-height:1.4}*{box-sizing:border-box}button{font:inherit;color:inherit}button:focus-visible{outline:2px solid var(--cobalt);outline-offset:3px}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
:host{display:block;--x:50%;--y:50%} .stage{position:relative;min-height:220px;display:grid;place-items:center;border:1px solid var(--line);background:var(--paper-2);overflow:hidden;cursor:crosshair} .type{font-family:Georgia,serif;font-size:clamp(4rem,12vw,9rem);line-height:.8;letter-spacing:-.08em;color:var(--ink);user-select:none} .lens{position:absolute;left:0;top:0;width:110px;height:110px;border:1px solid var(--ink);border-radius:50%;background:rgba(243,239,230,.18);backdrop-filter:blur(2px);transform:translate(var(--x),var(--y));pointer-events:none;mix-blend-mode:multiply} .lens:after{content:"";position:absolute;inset:9px;border:1px dashed rgba(21,19,15,.45);border-radius:50%} .status{margin:10px 0 0;color:var(--muted);font-size:12px} @media(pointer:coarse){.lens{display:none}} @media(prefers-reduced-motion:reduce){.lens{display:none}}`;
class MosaicCursorLens extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({mode:'open'});
    root.innerHTML = `<style>${CSS}</style><div class="stage" part="stage"><span class="type"></span><span class="lens" aria-hidden="true"></span></div><p class="status" role="status" aria-live="polite">Move across the specimen. The lens follows the pointer.</p>`;
    const stage = root.querySelector('.stage'), type = root.querySelector('.type'), lens = root.querySelector('.lens'), status = root.querySelector('.status');
    type.textContent = this.getAttribute('label') || 'Aa';
    const reset = () => { lens.style.setProperty('--x','50%'); lens.style.setProperty('--y','50%'); status.textContent = 'Move across the specimen. The lens follows the pointer.'; };
    stage.addEventListener('pointermove', e => {
      const r = stage.getBoundingClientRect();
      lens.style.setProperty('--x', `${e.clientX - r.left - 55}px`);
      lens.style.setProperty('--y', `${e.clientY - r.top - 55}px`);
      status.textContent = 'Reading through the lens.';
    });
    stage.addEventListener('pointerleave', reset);
    stage.addEventListener('click', () => this.dispatchEvent(new CustomEvent('mosaic-lens', {bubbles:true, composed:true, detail:{kind:'cursor-lens'}})));
  }
}
customElements.define('mosaic-cursor-lens', MosaicCursorLens);
