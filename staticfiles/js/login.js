(function(){
  document.querySelectorAll('.togglePassBtn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var inp = this.previousElementSibling;
      var icon = this.querySelector('.eyeIcon');
      if(inp.type === 'password'){
        inp.type = 'text';
        icon.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';
      } else {
        inp.type = 'password';
        icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
      }
    });
  });

  var loginForm = document.getElementById('loginForm');
  var loginBtn = document.getElementById('loginBtn');
  var loginError = document.getElementById('loginError');

  if (loginForm && loginBtn) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      var oldText = loginBtn.innerHTML;
      loginBtn.innerHTML = 'Ingresando...';
      loginBtn.classList.add('loading');
      if (loginError) loginError.classList.remove('show');

      var formData = new FormData(loginForm);
      fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(function(res) {
        if (res.ok) return res.json();
        throw res;
      })
      .then(function(data) {
        if (data.status === 'success') {
          window.location.href = data.redirect_url;
        }
      })
      .catch(function(err) {
        loginBtn.innerHTML = oldText;
        loginBtn.classList.remove('loading');
        if (loginError) loginError.classList.add('show');
        
        // Trigger abrupt closing animation
        if (window.triggerErrorAnim) window.triggerErrorAnim();
      });
    });
  }
})();

// Animación progresiva de la flor SVG (por caracteres / simple jumps)
(function() {
  var FRAMES = window.FLOWER_FRAMES || [];
  var N = FRAMES.length;
  var stage = document.getElementById('flowerStage');
  var glow = document.getElementById('bloomGlow');
  
  var userInp = document.getElementById('emailInput');
  var passInp = document.getElementById('passInput');
  
  var els = []; var cur = 0; var animTimer = null;
  for (var i = 0; i < N; i++) {
    var d = document.createElement('div'); d.className = 'flower-frame';
    d.innerHTML = FRAMES[i]; stage.appendChild(d); els.push(d);
  }
  if (els[0]) els[0].classList.add('active');

  function updateGlow(idx) {
    if (idx < 0) { glow.style.opacity = 0; return; }
    glow.style.opacity = 1;
    var pct = idx / (N - 1);
    var op = 0.1 + (pct * 0.2);
    glow.style.background = 'radial-gradient(ellipse, rgba(245,198,198,'+ op +') 0%, transparent 65%)';
  }

  function goToFrame(target) {
    if (cur === target) return;
    if (animTimer) clearInterval(animTimer);
    var step = cur < target ? 1 : -1;
    animTimer = setInterval(function() {
      if (cur === target) { clearInterval(animTimer); animTimer = null; return; }
      if (els[cur]) els[cur].classList.remove('active');
      cur += step;
      if (els[cur]) {
        els[cur].classList.add('active');
      }
      updateGlow(cur);
    }, 45);
  }

  // Lógica simplificada preferida por la usuaria
  function updateAnim() {
    var target = 0;
    if (userInp && userInp.value.trim().length > 0) target = 12;
    if (passInp && passInp.value.length > 0) target = 24;
    goToFrame(target);
  }

  window.triggerErrorAnim = function() {
    // Snap shut logic
    if (animTimer) clearInterval(animTimer);
    if (els[cur]) els[cur].classList.remove('active');
    cur = 0;
    if (els[cur]) els[cur].classList.add('active');
    updateGlow(cur);
  };

  [userInp, passInp].forEach(function(inp) {
    if(inp) {
      inp.addEventListener('input', updateAnim);
      inp.addEventListener('focus', updateAnim);
      inp.addEventListener('blur', updateAnim);
    }
  });

  updateAnim();
})();