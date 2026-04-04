/**
 * Lightweight magical sparkle layer (canvas).
 */
(function () {
  var canvas = document.getElementById('sparkle-canvas');
  if (!canvas || !canvas.getContext) return;

  var ctx = canvas.getContext('2d');
  var w = 0;
  var h = 0;
  var particles = [];
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var colors = ['#c4b5fd', '#a5f3fc', '#fbcfe8', '#fde68a', '#bbf7d0', '#e9d5ff'];

  function resize() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.width = Math.floor(window.innerWidth * dpr);
    h = canvas.height = Math.floor(window.innerHeight * dpr);
    canvas.style.width = window.innerWidth + 'px';
    canvas.style.height = window.innerHeight + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function Sparkle() {
    this.reset(true);
  }

  Sparkle.prototype.reset = function (initial) {
    this.x = Math.random() * window.innerWidth;
    this.y = Math.random() * window.innerHeight;
    this.r = Math.random() * 2.2 + 0.4;
    this.vx = (Math.random() - 0.5) * 0.35;
    this.vy = (Math.random() - 0.5) * 0.35;
    this.twinkle = Math.random() * Math.PI * 2;
    this.speed = 0.06 + Math.random() * 0.06;
    this.c = colors[(Math.random() * colors.length) | 0];
    if (initial) this.twinkle = Math.random() * Math.PI * 2;
  };

  Sparkle.prototype.step = function () {
    this.x += this.vx;
    this.y += this.vy;
    this.twinkle += this.speed;
    var W = window.innerWidth;
    var H = window.innerHeight;
    if (this.x < -20 || this.x > W + 20 || this.y < -20 || this.y > H + 20) {
      this.reset(false);
    }
  };

  Sparkle.prototype.draw = function () {
    var a = 0.25 + Math.sin(this.twinkle) * 0.45;
    ctx.beginPath();
    ctx.fillStyle = this.c;
    ctx.globalAlpha = Math.max(0.08, Math.min(0.85, a));
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
    ctx.fill();

    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.twinkle * 0.8);
    ctx.strokeStyle = this.c;
    ctx.globalAlpha = a * 0.75;
    ctx.lineWidth = 0.6;
    var s = this.r * 4;
    ctx.beginPath();
    ctx.moveTo(-s, 0);
    ctx.lineTo(s, 0);
    ctx.moveTo(0, -s);
    ctx.lineTo(0, s);
    ctx.stroke();
    ctx.restore();
    ctx.globalAlpha = 1;
  };

  function countParticles() {
    var area = window.innerWidth * window.innerHeight;
    var n = Math.floor(area / 14000);
    return Math.max(40, Math.min(140, n));
  }

  function initParticles() {
    particles = [];
    var n = countParticles();
    for (var i = 0; i < n; i++) particles.push(new Sparkle());
  }

  function loop() {
    if (reducedMotion) return;
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
    for (var i = 0; i < particles.length; i++) {
      particles[i].step();
      particles[i].draw();
    }
    requestAnimationFrame(loop);
  }

  window.addEventListener('resize', function () {
    resize();
    initParticles();
  });

  resize();
  initParticles();

  if (!reducedMotion) {
    requestAnimationFrame(loop);
  }
})();
