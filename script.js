(function () {
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');
  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') nav.classList.remove('open');
  });

  var tabs = document.querySelectorAll('.tabs button');
  var panels = document.querySelectorAll('.panel');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (b) { b.setAttribute('aria-selected', b === t); });
      panels.forEach(function (p) { p.classList.toggle('on', p.id === t.getAttribute('aria-controls')); });
    });
  });
})();
