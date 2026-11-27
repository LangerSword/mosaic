const CSS = `:host{--paper:#f3efe6;--paper-2:#e9e2d5;--ink:#15130f;--muted:#6c655a;--line:#d4ccbd;--clay:#c64a2e;--cobalt:#0d2340;--ease:cubic-bezier(.22,1,.36,1);display:block;color:var(--ink);font-family:ui-sans-serif,system-ui,sans-serif;line-height:1.4}*{box-sizing:border-box}button{font:inherit;color:inherit}button:focus-visible{outline:2px solid var(--cobalt);outline-offset:3px}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
:host{--ascii-bg:#0b1424;--ascii-fg:#f1eee6;--ascii-dim:#7083a6;display:block;background:var(--ascii-bg);color:var(--ascii-fg);overflow:hidden}
.field{position:relative;min-height:210px;padding:14px;background:radial-gradient(120% 120% at 18% 0%,#183451 0%,transparent 58%),var(--ascii-bg);overflow:hidden}
pre{margin:0;font:11px/1.04 ui-monospace,SFMono-Regular,monospace;letter-spacing:.08em;white-space:pre;color:var(--ascii-fg);opacity:.92}
.toolbar{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:8px;padding-top:9px;border-top:1px solid rgba(241,238,230,.2);font:8px/1.3 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ascii-dim)}
.toolbar strong{color:var(--ascii-fg);font-weight:400}
button{min-height:28px;padding:5px 8px;border:1px solid rgba(241,238,230,.35);background:transparent;color:var(--ascii-fg);font:8px/1 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}
button:hover{background:var(--ascii-fg);color:var(--ascii-bg)}
.status{margin:0;padding:0 14px 12px;color:var(--ascii-dim);font:9px/1.4 ui-monospace,monospace}`;
class MosaicAsciiField extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({mode:'open'});
    root.innerHTML = `<style>${CSS}</style><div class="field"><pre aria-hidden="true" data-field></pre><div class="toolbar"><span>field / <strong data-mode>sky</strong></span><button type="button" data-shift>Shift ramp</button></div></div><p class="status" role="status" aria-live="polite">A monospace field. Pointer changes the lens; the button changes the ramp.</p>`;
    const field = root.querySelector('.field'), pre = root.querySelector('[data-field]');
    const modeEl = root.querySelector('[data-mode]'), button = root.querySelector('[data-shift]');
    const status = root.querySelector('.status');
    const ramps = [' .:-=+*#%@', ' ·░▒▓█'];
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let mode = 0, pointerX = .5, pointerY = .5, raf = 0, visible = true, last = 0;
    const render = (time) => {
      const width = Math.max(280, this.clientWidth || 480);
      const cols = Math.max(34, Math.min(72, Math.floor(width / 9)));
      const rows = 18;
      const ramp = ramps[mode];
      const phase = time * .00035;
      const lines = [];
      for (let y = 0; y < rows; y += 1) {
        let line = '';
        for (let x = 0; x < cols; x += 1) {
          const nx = x / Math.max(1, cols - 1), ny = y / Math.max(1, rows - 1);
          const lens = Math.max(0, 1 - Math.hypot(nx - pointerX, ny - pointerY) * 2.2);
          const value = (Math.sin(nx * 12 + phase) + Math.cos(ny * 9 - phase * .7) + lens * 1.7) / 3;
          const index = Math.max(0, Math.min(ramp.length - 1, Math.floor((value * .5 + .5) * ramp.length)));
          line += ramp[index];
        }
        lines.push(line);
      }
      pre.textContent = lines.join('\n');
    };
    const loop = (time) => {
      if (!visible || document.hidden) return;
      if (time - last > 33) { render(time); last = time; }
      raf = requestAnimationFrame(loop);
    };
    const kick = () => { if (!reduced && visible && !raf) { last = 0; raf = requestAnimationFrame(loop); } };
    field.addEventListener('pointermove', (event) => {
      const rect = field.getBoundingClientRect();
      pointerX = Math.max(0, Math.min(1, (event.clientX - rect.left) / Math.max(1, rect.width)));
      pointerY = Math.max(0, Math.min(1, (event.clientY - rect.top) / Math.max(1, rect.height)));
      if (reduced) render(0);
    });
    field.addEventListener('pointerleave', () => { pointerX = .5; pointerY = .5; if (reduced) render(0); });
    button.addEventListener('click', () => {
      mode = (mode + 1) % ramps.length;
      modeEl.textContent = mode === 0 ? 'sky' : 'dense';
      status.textContent = mode === 0 ? 'Sky ramp. Pointer changes the lens.' : 'Dense ramp. Same field, different density.';
      this.dispatchEvent(new CustomEvent('mosaic-ascii-change', {bubbles:true, composed:true, detail:{ramp: mode === 0 ? 'sky' : 'dense'}}));
      if (reduced) render(0); else kick();
    });
    if (reduced) { render(0); return; }
    const io = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      if (visible) kick(); else { cancelAnimationFrame(raf); raf = 0; }
    }, {threshold: .05});
    io.observe(this);
    document.addEventListener('visibilitychange', () => { if (document.hidden) { cancelAnimationFrame(raf); raf = 0; } else kick(); });
    kick();
  }
}
customElements.define('mosaic-ascii-field', MosaicAsciiField);
