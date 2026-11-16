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

  // Mappa Google caricata solo dopo il clic, per non attivare cookie di terze parti
  var map = document.getElementById('map');
  var load = document.getElementById('map-load');
  if (map && load) {
    var types = document.querySelectorAll('.map-tools button');
    var address = 'Via Cesare Battisti 12, 21055 Gorla Minore VA';
    var show = function (type) {
      var src = 'https://maps.google.com/maps?q=' + encodeURIComponent(address) + '&t=' + type + '&z=18&output=embed';
      var frame = map.querySelector('iframe');
      if (!frame) {
        map.innerHTML = '';
        frame = document.createElement('iframe');
        frame.title = 'Mappa dello studio del Dott. Croci';
        frame.loading = 'lazy';
        frame.referrerPolicy = 'no-referrer-when-downgrade';
        map.appendChild(frame);
      }
      frame.src = src;
      types.forEach(function (b) {
        b.disabled = false;
        b.setAttribute('aria-pressed', b.dataset.type === type);
      });
    };
    load.addEventListener('click', function () { show('m'); });
    types.forEach(function (b) {
      b.addEventListener('click', function () { show(b.dataset.type); });
    });
  }
})();
