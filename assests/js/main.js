function smoothScroll(target, duration) {
  
  var targetPosition = target.getBoundingClientRect().top;
  var startPosition = window.pageYOffset || window.scrollY;
  var startTime = null;

  function loop(currentTime) {
    if (startTime === null) startTime = currentTime;
    var timeElapsed = currentTime - startTime;
    var run = ease(timeElapsed, startPosition, targetPosition, duration);
    window.scrollTo(0, run);
    if (timeElapsed < duration) requestAnimationFrame(loop);
  }
  function ease(t, b, c, d) {
    t /= d / 2;
    if (t < 1) return (c / 2) * t * t + b;
    t--;
    return (-c / 2) * (t * (t - 2) - 1) + b;
  }
  requestAnimationFrame(loop);
}

//Animating
document.querySelector(".work-nav").addEventListener("click", function (e) {
  e.preventDefault();
  console.log(e.target);
  var target = document.querySelector("#work");
  smoothScroll(target, 500);
});

//Animating Second Link
document.querySelector(".start").addEventListener("click", function (e) {
  e.preventDefault();
  var target = document.querySelector("#_start");
  smoothScroll(target, 500);
});
