(() => {
  const root = document.documentElement;
  root.classList.remove('no-js');
  root.classList.add('js');

  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Reveal: observer plus a time safety net so a fast jump cannot leave a section hidden.
  const reveals = [...document.querySelectorAll('.reveal')];
  if (reveals.length) {
    if (reduced() || !('IntersectionObserver' in window)) {
      reveals.forEach((el) => el.classList.add('is-visible'));
    } else {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
      reveals.forEach((el, i) => {
        io.observe(el);
        setTimeout(() => el.classList.add('is-visible'), 1400 + i * 40);
      });
    }
  }

  // Hold to confirm. One state machine per control; pointer capture and keyboard share it.
  document.querySelectorAll('[data-hold]').forEach((button) => {
    const fill = button.querySelector('[data-hold-fill]');
    const label = button.querySelector('[data-hold-label]');
    const describedBy = button.getAttribute('aria-describedby');
    const status = describedBy ? document.getElementById(describedBy) : null;
    let started = 0;
    let raf = 0;
    let holding = false;
    let done = false;
    let progress = 0;

    const paint = (value) => {
      progress = Math.max(0, Math.min(1, value));
      if (fill) fill.style.transform = `scaleX(${progress})`;
      if (fill) fill.style.transition = 'none';
    };

    const reset = () => {
      holding = false;
      cancelAnimationFrame(raf);
      if (fill) {
        fill.style.transition = 'transform .3s cubic-bezier(.22,1,.36,1)';
        fill.style.transform = 'scaleX(0)';
      }
      if (label) label.textContent = 'Hold to delete';
      if (status) status.textContent = 'Released. Nothing was deleted.';
      button.classList.remove('is-done');
      button.removeAttribute('data-done');
    };

    const tick = (now) => {
      if (!holding) return;
      const value = Math.min(1, (now - started) / 1200);
      paint(value);
      if (value >= 1) {
        holding = false;
        done = true;
        button.classList.add('is-done');
        button.setAttribute('data-done', 'true');
        if (label) label.textContent = 'Deleted';
        if (status) status.textContent = 'Deleted. One action, confirmed.';
        return;
      }
      if (status) status.textContent = `Keep holding. ${Math.round(value * 100)}%.`;
      raf = requestAnimationFrame(tick);
    };

    const start = (event) => {
      if (done) return;
      if (event && event.type === 'pointerdown') {
        event.preventDefault();
        button.setPointerCapture?.(event.pointerId);
      }
      if (event && event.type === 'keydown') {
        if (event.repeat) return;
        event.preventDefault();
      }
      holding = true;
      started = performance.now() - progress * 1200;
      if (label) label.textContent = 'Keep holding';
      if (status) status.textContent = 'Keep holding.';
      paint(progress);
      raf = requestAnimationFrame(tick);
    };

    const stop = () => {
      if (!holding) return;
      holding = false;
      cancelAnimationFrame(raf);
      if (!done) reset();
    };

    button.addEventListener('pointerdown', start);
    button.addEventListener('pointerup', stop);
    button.addEventListener('pointercancel', reset);
    button.addEventListener('pointerleave', (event) => {
      if (event.pointerType === 'mouse' && holding) stop();
    });
    button.addEventListener('keydown', (event) => {
      if (event.key === ' ' || event.key === 'Enter') start(event);
    });
    button.addEventListener('keyup', (event) => {
      if (event.key === ' ' || event.key === 'Enter') stop();
    });
    button.addEventListener('blur', () => {
      if (!done) reset();
    });
    button.addEventListener('contextmenu', (event) => event.preventDefault());
  });

  // Segmented readout.
  const seg = document.querySelector('.seg');
  if (seg) {
    const buttons = [...seg.querySelectorAll('[data-seg]')];
    const readout = document.querySelector('[data-seg-readout]');
    const content = {
      day: ['Day', '24 hours · 1 lap'],
      week: ['Week', '7 days · 5 laps'],
      month: ['Month', '30 days · 12 laps'],
      year: ['Year', '12 months · 147 laps'],
    };
    const choose = (button) => {
      buttons.forEach((other) => {
        const active = other === button;
        other.setAttribute('aria-selected', String(active));
        other.tabIndex = active ? 0 : -1;
      });
      const item = content[button.dataset.seg];
      if (readout && item) {
        readout.replaceChildren();
        const strong = document.createElement('strong');
        strong.textContent = item[0];
        const span = document.createElement('span');
        span.textContent = item[1];
        readout.append(strong, span);
      }
    };
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => choose(button));
      button.addEventListener('keydown', (event) => {
        let next = null;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = buttons[(index + 1) % buttons.length];
        if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = buttons[(index - 1 + buttons.length) % buttons.length];
        if (event.key === 'Home') next = buttons[0];
        if (event.key === 'End') next = buttons[buttons.length - 1];
        if (next) {
          event.preventDefault();
          choose(next);
          next.focus();
        }
      });
    });
  }

  // Card tilt: a bonus, never required, never on touch or reduced motion.
  const tilt = document.querySelector('[data-tilt]');
  if (tilt) {
    const card = tilt.querySelector('.tilt-card');
    let enabled = !reduced();
    tilt.addEventListener('pointermove', (event) => {
      if (!enabled || event.pointerType === 'touch' || !card) return;
      const rect = tilt.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width;
      const y = (event.clientY - rect.top) / rect.height;
      card.style.transform = `rotateY(${((x - 0.5) * 7).toFixed(2)}deg) rotateX(${((0.5 - y) * 5).toFixed(2)}deg) translateY(-3px)`;
    });
    tilt.addEventListener('pointerleave', () => {
      if (card) card.style.transform = '';
    });
    tilt.addEventListener('pointerdown', (event) => {
      if (event.pointerType === 'touch') enabled = false;
    });
    window.addEventListener('resize', () => { enabled = !reduced(); });
  }

  // Thinking state: named steps, no invented percentage.
  document.querySelectorAll('[data-think]').forEach((button) => {
    const steps = [...document.querySelectorAll('[data-think-steps] [data-step]')];
    const status = document.querySelector('[data-think-status]');
    let running = false;
    const clear = () => steps.forEach((step) => step.classList.remove('is-done', 'is-now'));
    const run = () => {
      if (running || !steps.length) return;
      running = true;
      button.disabled = true;
      clear();
      let index = 0;
      const advance = () => {
        steps.forEach((step, i) => {
          step.classList.toggle('is-done', i < index);
          step.classList.toggle('is-now', i === index);
        });
        if (status) status.textContent = `${steps[index]?.textContent?.trim() || 'Working'}...`;
        index += 1;
        if (index < steps.length) {
          setTimeout(advance, reduced() ? 120 : 720);
        } else {
          setTimeout(() => {
            steps.forEach((step) => step.classList.add('is-done'));
            steps.forEach((step) => step.classList.remove('is-now'));
            if (status) status.textContent = 'Done. Four steps, no fake percentage.';
            running = false;
            button.disabled = false;
            button.textContent = 'Run again';
          }, reduced() ? 120 : 620);
        }
      };
      advance();
    };
    button.addEventListener('click', run);
  });

  // Copy install commands.
  document.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = document.querySelector(button.dataset.copy);
      if (!target) return;
      const text = target.textContent || '';
      try {
        await navigator.clipboard.writeText(text);
        const old = button.textContent;
        button.textContent = 'Copied';
        setTimeout(() => { button.textContent = old; }, 1500);
      } catch {
        button.textContent = 'Select it';
      }
    });
  });

  // Forge playground: real files and real code from the bundled samples.
  const forgeData = window.MOSAIC_FORGE;
  const stackSelect = document.querySelector('#forge-stack');
  const motionSelect = document.querySelector('#forge-motion');
  const fileList = document.querySelector('#forge-files');
  const codeEl = document.querySelector('#forge-code');
  const fileLabel = document.querySelector('#forge-file');
  const depsLabel = document.querySelector('#forge-deps');
  if (forgeData && stackSelect && motionSelect && fileList && codeEl) {
    forgeData.stacks.forEach((stack) => {
      const option = document.createElement('option');
      option.value = stack.id;
      option.textContent = stack.label;
      stackSelect.append(option);
    });
    stackSelect.value = 'react';
    let selectedPath = 'index.tsx';
    const renderCode = () => {
      const sample = forgeData.samples[stackSelect.value]?.[motionSelect.value];
      if (!sample) return;
      const files = sample.files || [];
      if (!files.some((file) => file.path === selectedPath)) {
        selectedPath = files.find((file) => file.path.startsWith('index.'))?.path || files[0]?.path || '';
      }
      fileList.replaceChildren();
      files.forEach((file) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = file.path;
        button.setAttribute('aria-pressed', String(file.path === selectedPath));
        button.addEventListener('click', () => {
          selectedPath = file.path;
          renderCode();
        });
        fileList.append(button);
      });
      const selected = files.find((file) => file.path === selectedPath);
      if (fileLabel) fileLabel.textContent = selected?.path || 'forge';
      const deps = sample.deps?.length ? sample.deps.join(', ') : 'none';
      if (depsLabel) depsLabel.textContent = `deps: ${deps}`;
      if (codeEl) codeEl.textContent = selected?.content || '';
    };
    stackSelect.addEventListener('change', () => { selectedPath = 'index.tsx'; renderCode(); });
    motionSelect.addEventListener('change', renderCode);
    renderCode();
  }

  // Download ring demo: every step is an explicit event, not a timer.
  const ring = document.querySelector('mosaic-download-ring');
  const advance = document.querySelector('[data-demo-download]');
  if (ring && advance) {
    let progress = 0;
    advance.addEventListener('click', () => {
      progress = Math.min(100, progress + 20);
      ring.progress = progress;
      advance.textContent = progress >= 100 ? 'Complete' : 'Advance event';
    });
  }

  // Taste lab: selected brief -> real mosaic_invent candidates.
  const tasteData = window.MOSAIC_INVENT;
  const tasteSelect = document.querySelector('#taste-brief');
  const tasteGrid = document.querySelector('#taste-grid');
  if (tasteData && tasteSelect && tasteGrid) {
    const add = (parent, tag, className, text) => {
      const node = document.createElement(tag);
      if (className) node.className = className;
      if (text !== undefined) node.textContent = text;
      parent.append(node);
      return node;
    };
    tasteData.briefs.forEach((group, index) => {
      const option = document.createElement('option');
      option.value = String(index);
      option.textContent = group.brief;
      tasteSelect.append(option);
    });
    const renderTaste = () => {
      const group = tasteData.briefs[Number(tasteSelect.value) || 0];
      tasteGrid.replaceChildren();
      group.candidates.forEach((c) => {
        const card = add(tasteGrid, 'article', 'taste-card');
        add(card, 'h3', '', c.name);
        add(card, 'p', 'thesis', c.thesis);
        const chips = add(card, 'div', 'taste-chips');
        [c.input, c.physics, c.feedback, c.forge_kind].forEach((value) => add(chips, 'span', '', value));
        const list = add(card, 'ol', 'taste-states');
        c.state_machine.slice(0, 3).forEach((state) => add(list, 'li', '', `${state.state}: ${state.event} → ${state.result}`));
        const scores = add(card, 'div', 'scores');
        Object.entries(c.scores).forEach(([key, value]) => {
          const row = add(scores, 'div', 'score-row');
          add(row, 'span', '', key);
          const bar = add(row, 'i');
          const fill = add(bar, 'b');
          fill.style.width = `${value * 10}%`;
          add(row, 'em', '', String(value));
        });
        const total = add(card, 'div', 'taste-total');
        add(total, 'span', '', 'overall');
        add(total, 'strong', '', c.overall.toFixed(1));
      });
    };
    tasteSelect.addEventListener('change', renderTaste);
    renderTaste();
  }

  // Component index: all public observations, with a small visual grammar.
  const gallery = window.MOSAIC_COMPONENTS;
  const galleryGrid = document.querySelector('#component-grid');
  if (gallery && galleryGrid) {
    const add = (parent, tag, className, text) => {
      const node = document.createElement(tag);
      if (className) node.className = className;
      if (text !== undefined) node.textContent = text;
      parent.append(node);
      return node;
    };
    gallery.forEach((component) => {
      const card = add(galleryGrid, 'article', 'specimen');
      const art = add(card, 'div', 'specimen-art');
      art.dataset.family = component.family;
      const body = add(card, 'div', 'specimen-body');
      add(body, 'b', '', component.name);
      add(body, 'span', '', component.family);
      add(body, 'p', '', component.state.length > 152 ? component.state.slice(0, 149) + '...' : component.state);
      add(body, 'small', '', component.use_when);
    });
  }
})();
