/* ============================================================
   AI Assistant Floating Widget — Behaviour
   Calls POST /ask/message and renders chat bubbles in-panel.
   ============================================================ */

(function () {
  'use strict';

  const fab      = document.getElementById('ai-fab');
  const panel    = document.getElementById('ai-panel');
  const messages = document.getElementById('ai-messages');
  const welcome  = document.getElementById('ai-welcome');
  const input    = document.getElementById('ai-input');
  const sendBtn  = document.getElementById('ai-send');

  /* ---- Panel toggle ---- */
  function togglePanel() {
    const isOpen = fab.classList.toggle('open');
    panel.classList.toggle('visible', isOpen);
    panel.setAttribute('aria-hidden', String(!isOpen));
    if (isOpen) input.focus();
  }

  fab.addEventListener('click', togglePanel);

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && fab.classList.contains('open')) togglePanel();
  });

  /* ---- Textarea auto-resize ---- */
  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 90) + 'px';
  });

  // Enter = send, Shift+Enter = newline
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  sendBtn.addEventListener('click', sendMessage);

  /* ---- DOM helpers ---- */
  function appendBubble(role, text) {
    if (welcome) welcome.style.display = 'none';

    const wrap   = document.createElement('div');
    wrap.className = 'ai-msg ' + role;

    const bubble = document.createElement('div');
    bubble.className = 'ai-bubble';
    bubble.textContent = text;

    wrap.appendChild(bubble);
    messages.appendChild(wrap);
    messages.scrollTop = messages.scrollHeight;
    return bubble;
  }

  function showTyping() {
    if (welcome) welcome.style.display = 'none';

    const wrap   = document.createElement('div');
    wrap.className = 'ai-msg bot';
    wrap.id = 'ai-typing-indicator';

    const bubble = document.createElement('div');
    bubble.className = 'ai-bubble';
    bubble.innerHTML =
      '<div class="ai-typing-dots"><span></span><span></span><span></span></div>';

    wrap.appendChild(bubble);
    messages.appendChild(wrap);
    messages.scrollTop = messages.scrollHeight;
  }

  function removeTyping() {
    const el = document.getElementById('ai-typing-indicator');
    if (el) el.remove();
  }

  /* ---- Send a message ---- */
  async function sendMessage() {
    const text = input.value.trim();
    if (!text || sendBtn.disabled) return;

    appendBubble('user', text);
    input.value = '';
    input.style.height = 'auto';
    sendBtn.disabled = true;
    showTyping();

    try {
      const res  = await fetch('/ask/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      removeTyping();

      if (!res.ok) {
        appendBubble('bot', '⚠️ ' + (data.error || 'Something went wrong. Please try again.'));
      } else {
        appendBubble('bot', data.reply);
      }
    } catch (_) {
      removeTyping();
      appendBubble('bot', '⚠️ Could not reach the assistant. Check your connection.');
    } finally {
      sendBtn.disabled = false;
      input.focus();
    }
  }
})();
