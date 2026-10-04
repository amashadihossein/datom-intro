// Motion starts when its slide does, and a beat's motion when its fragment does.
//
// Off-screen SVG timelines are paused; the slide being shown is rewound and
// played. Inside a slide, a fragment can hold triggers -- SMIL elements with
// class "on-reveal" and begin="indefinite" -- which fire when that fragment is
// shown; the beat's animations begin relative to its trigger.
(function () {
  function fire(fragment) {
    var found = fragment.querySelectorAll ? fragment.querySelectorAll('.on-reveal') : [];
    Array.prototype.forEach.call(found, function (t) {
      // only this fragment's own triggers, not those of fragments nested inside it
      if (t.closest('.fragment') === fragment && t.beginElement) t.beginElement();
    });
  }
  function sync(current) {
    document.querySelectorAll('.reveal .slides section svg').forEach(function (svg) {
      if (!svg.pauseAnimations) return;
      if (current && current.contains(svg)) {
        svg.setCurrentTime(0);
        svg.unpauseAnimations();
      } else {
        svg.pauseAnimations();
      }
    });
    if (!current) return;
    // Arriving with fragments already shown (navigating back): replay their
    // one-shot motion, then jump past it so the scene shows its end state.
    var shown = current.querySelectorAll('.fragment.visible');
    if (!shown.length) return;
    shown.forEach(fire);
    current.querySelectorAll('svg').forEach(function (svg) {
      if (svg.setCurrentTime) svg.setCurrentTime(svg.getCurrentTime() + 30);
    });
  }
  function hook() {
    if (!window.Reveal || !Reveal.on) return setTimeout(hook, 50);
    Reveal.on('slidechanged', function (e) { sync(e.currentSlide); });
    Reveal.on('fragmentshown', function (e) { (e.fragments || [e.fragment]).forEach(fire); });
    if (Reveal.isReady()) sync(Reveal.getCurrentSlide());
    else Reveal.on('ready', function (e) { sync(e.currentSlide); });
  }
  hook();
})();
