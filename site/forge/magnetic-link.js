const CSS = `:host{--paper:#f3efe6;--paper-2:#e9e2d5;--ink:#15130f;--muted:#6c655a;--line:#d4ccbd;--clay:#c64a2e;--cobalt:#0d2340;--ease:cubic-bezier(.22,1,.36,1);display:block;color:var(--ink);font-family:ui-sans-serif,system-ui,sans-serif;line-height:1.4}*{box-sizing:border-box}button{font:inherit;color:inherit}button:focus-visible{outline:2px solid var(--cobalt);outline-offset:3px}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
:host{display:inline-block;--mx:0px;--my:0px} button{position:relative;display:inline-flex;align-items:center;gap:12px;min-height:52px;padding:0 18px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);font:700 11px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;transform:translate(var(--mx),var(--my));transition:transform .18s var(--ease),background .18s} button:hover,button:focus-visible{background:var(--clay);border-color:var(--clay)} .arrow{display:inline-grid;place-items:center;width:28px;height:28px;border:1px solid currentColor;border-radius:50%;font-size:16px;transition:transform .18s} button:hover .arrow{transform:rotate(45deg)} .status{display:block;margin:10px 0 0;color:var(--muted);font-size:12px} @media(prefers-reduced-motion:reduce){button{transform:none}}`;
class MosaicMagneticLink extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({mode:'open'});
    root.innerHTML = `<style>${CSS}</style><button type="button" part="control"><span class="label"></span><span class="arrow" aria-hidden="true">↗</span></button><p class="status" role="status" aria-live="polite">Move across the button. It follows, then settles.</p>`;
    const button = root.querySelector('button'), label = root.querySelector('.label'), status = root.querySelector('.status');
    label.textContent = this.getAttribute('label') || 'Follow the signal';
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const reset = () => { button.style.setProperty('--mx','0px'); button.style.setProperty('--my','0px'); };
    button.addEventListener('pointermove', e => {
      if (reduced) return;
      const r = button.getBoundingClientRect();
      button.style.setProperty('--mx', `${((e.clientX - (r.left + r.width / 2)) * .12).toFixed(1)}px`);
      button.style.setProperty('--my', `${((e.clientY - (r.top + r.height / 2)) * .18).toFixed(1)}px`);
    });
    button.addEventListener('pointerleave', reset);
    button.addEventListener('blur', reset);
    button.addEventListener('click', () => {
      status.textContent = 'Signal received. The link holds.';
      this.dispatchEvent(new CustomEvent('mosaic-follow', {bubbles:true, composed:true, detail:{kind:'magnetic-link'}}));
      setTimeout(() => { status.textContent = 'Move across the button. It follows, then settles.'; }, 1600);
    });
  }
}
customElements.define('mosaic-magnetic-link', MosaicMagneticLink);
