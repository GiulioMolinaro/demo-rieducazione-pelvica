(function () {
  // Menu su telefono
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') nav.classList.remove('open');
    });
  }

  // Mappa di Google: si carica solo dopo il clic, così prima nessun dato va a Google.
  // Senza JavaScript resta il link "Apri in Google Maps".
  var box = document.getElementById('map');
  var load = document.getElementById('map-load');
  if (box && load) {
    load.hidden = false;
    load.addEventListener('click', function () {
      var frame = document.createElement('iframe');
      frame.title = 'Mappa dello studio del Dott. Croci, Via Cesare Battisti 12, Gorla Minore';
      frame.referrerPolicy = 'no-referrer-when-downgrade';
      frame.src = 'https://maps.google.com/maps?q=' + encodeURIComponent('Via Cesare Battisti 12, 21055 Gorla Minore VA') + '&t=m&z=16&output=embed';
      box.innerHTML = '';
      box.classList.add('is-loaded');
      box.appendChild(frame);
    });
  }
})();
