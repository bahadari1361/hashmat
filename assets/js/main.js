(function () {
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('animateMotion').forEach(function (el) { el.remove(); });
  }
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
(function () {
  var f = document.getElementById('enquiry');
  if (!f) return;
  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var v = function (n) { return (f.elements[n] && f.elements[n].value || '').trim(); };
    var body = v('message') + '\n\n--\n' + v('name') + (v('company') ? '\n' + v('company') : '') + '\n' + v('email');
    var subject = f.dataset.subject + ': ' + v('topic');
    window.location.href = 'mailto:' + f.dataset.to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });
})();
