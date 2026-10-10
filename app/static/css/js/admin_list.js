(function () {
  // ── live search ──
  var input   = document.getElementById('pg-search');
  var rows    = document.querySelectorAll('.pg-row');
  var shown   = document.querySelector('[data-shown]');
  var label   = document.querySelector('[data-label]');
  var nomatch = document.getElementById('pg-nomatch');

  if (input) {
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      var visible = 0;
      rows.forEach(function (row) {
        var match = !q || row.getAttribute('data-search').indexOf(q) !== -1;
        row.hidden = !match;
        if (match) visible++;
      });
      if (shown) shown.textContent = visible;
      if (label) label.textContent = q ? label.getAttribute('data-match') : label.getAttribute('data-total');
      if (nomatch) nomatch.hidden = visible !== 0;
    });
  }

  // ── delete confirm ──
  var buttons = document.querySelectorAll('.pg-del');
  if (!buttons.length) return;

  var dialog  = document.getElementById('pg-dialog');
  var hasDlg  = dialog && typeof dialog.showModal === 'function';
  var nameEl  = dialog ? dialog.querySelector('[data-name]') : null;
  var okBtn   = dialog ? dialog.querySelector('[data-confirm]') : null;
  var noBtn   = dialog ? dialog.querySelector('[data-cancel]') : null;
  var target  = null;

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var form = btn.closest('form');
      if (!hasDlg) {
        if (window.confirm('Delete ' + btn.getAttribute('data-name') + '? This can\'t be undone.')) form.submit();
        return;
      }
      target = form;
      nameEl.textContent = btn.getAttribute('data-name');
      dialog.showModal();
    });
  });

  if (hasDlg) {
    okBtn.addEventListener('click', function () { if (target) target.submit(); });
    noBtn.addEventListener('click', function () { dialog.close(); });
    dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  }
})();