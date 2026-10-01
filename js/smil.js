// Motion starts when its slide does: pause every SVG timeline off-screen,
// and rewind + play the ones on the slide being shown.
(function () {
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
  }
  function hook() {
    if (!window.Reveal || !Reveal.on) return setTimeout(hook, 50);
    Reveal.on('slidechanged', function (e) { sync(e.currentSlide); });
    if (Reveal.isReady()) sync(Reveal.getCurrentSlide());
    else Reveal.on('ready', function (e) { sync(e.currentSlide); });
  }
  hook();
})();
