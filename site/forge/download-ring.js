const CSS = `:host{--paper:#f3efe6;--paper-2:#e9e2d5;--ink:#15130f;--muted:#6c655a;--line:#d4ccbd;--clay:#c64a2e;--cobalt:#0d2340;--ease:cubic-bezier(.22,1,.36,1);display:block;color:var(--ink);font-family:ui-sans-serif,system-ui,sans-serif;line-height:1.4}*{box-sizing:border-box}button{font:inherit;color:inherit}button:focus-visible{outline:2px solid var(--cobalt);outline-offset:3px}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
:host{--p:0;--ring:var(--clay)} .ring{--deg:calc(var(--p) * 360deg);width:132px;height:132px;border-radius:50%;display:grid;place-items:center;background:conic-gradient(var(--ring) var(--deg), var(--line) 0);position:relative} .ring:before{content:"";position:absolute;inset:10px;border-radius:50%;background:var(--paper)} .inner{position:relative;z-index:1;text-align:center} strong{display:block;font-size:25px;line-height:1} span,p{font:10px/1.4 ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)} p{margin:10px 0 0;font-size:12px;text-transform:none;letter-spacing:0}`;
class MosaicDownloadRing extends HTMLElement {
  static get observedAttributes(){ return ['value','label']; }
  connectedCallback() {
    if (this.shadowRoot) return;
    const root=this.attachShadow({mode:'open'});
    root.innerHTML=`<style>${CSS}</style><div class="ring" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="inner"><strong>0%</strong><span data-label>Download</span></div></div><p role="status" aria-live="polite">Progress comes from real bytes, not a timer.</p>`;
    this._ring=root.querySelector('.ring'); this._strong=root.querySelector('strong'); this._status=root.querySelector('p');
    this._render();
  }
  attributeChangedCallback(){ if(this.shadowRoot) this._render(); }
  set progress(value) { this.setAttribute('value', String(Math.max(0, Math.min(100, Number(value)||0)))); }
  get progress() { return Number(this.getAttribute('value')||0); }
  _render() {
    const value=this.progress; this._ring.style.setProperty('--p', String(value/100)); this._ring.setAttribute('aria-valuenow', String(Math.round(value))); this._strong.textContent=`${Math.round(value)}%`; const label=this.getAttribute('label')||'Download'; this._ring.querySelector('[data-label]').textContent=label;
    this._status.textContent=value>=100?'Complete. The file is ready.':'Progress comes from real bytes, not a timer.';
    if(value>=100 && !this._done){ this._done=true; this.dispatchEvent(new CustomEvent('mosaic-complete',{bubbles:true,composed:true,detail:{value}})); }
  }
}
customElements.define('mosaic-download-ring', MosaicDownloadRing);
