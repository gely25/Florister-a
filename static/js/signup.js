(function(){
  // Password Visibility
  document.querySelectorAll('.togglePassBtn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var inp = this.parentElement.querySelector('input');
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

  // Form Loading
  var signupForm = document.getElementById('signupForm');
  var regBtn = document.getElementById('registerBtn');
  var errMsg = document.getElementById('errMsg');

  signupForm.addEventListener('submit', function(e){
    var p1 = document.getElementById('passInput').value;
    var p2 = document.getElementById('passConfirmInput').value;
    if(p1 !== p2){
      e.preventDefault();
      errMsg.textContent = 'Las contraseñas no coinciden.';
      errMsg.classList.add('show');
      return;
    }
    regBtn.innerHTML = 'Procesando...';
    regBtn.style.opacity = '0.7';
  });

  // Flower logic
  var FRAMES = window.FLOWER_FRAMES || [];
  var N = FRAMES.length;
  var RANGES = [
    {start:0, end:4}, {start:5, end:8}, {start:9, end:12}, {start:13, end:16}, {start:17, end:20}, {start:21, end:24}
  ];
  var LABELS = ['Nombre','Apellido','Usuario','Correo','Contraseña','Confirmación'];
  var stage = document.getElementById('flowerStage');
  var glow = document.getElementById('bloomGlow');
  var stageLabel = document.getElementById('stageLabel');
  
  var inps = [
    document.getElementById('nameInput'), document.getElementById('lastNameInput'),
    document.getElementById('userInput'), document.getElementById('emailInput'),
    document.getElementById('passInput'), document.getElementById('passConfirmInput')
  ];
  
  var els = []; var cur = 0; var animTimer = null;
  for (var i = 0; i < N; i++) {
    var d = document.createElement('div'); d.className = 'flower-frame';
    d.innerHTML = FRAMES[i]; stage.appendChild(d); els.push(d);
  }
  if (els[0]) els[0].classList.add('active');

  function updateGlow(idx) {
    if (idx < 0) { glow.style.opacity = 0; return; }
    glow.style.opacity = 0.6;
    var pct = idx / (N - 1);
    var op = 0.1 + (pct * 0.25);
    glow.style.background = 'radial-gradient(ellipse, rgba(245,198,198,'+ op +') 0%, transparent 70%)';
  }

  function goToFrame(target) {
    if (animTimer) clearInterval(animTimer);
    target = Math.max(0, Math.min(N - 1, target));
    if (cur === target) return;
    var step = cur < target ? 1 : -1;
    animTimer = setInterval(function() {
      if (cur === target) { clearInterval(animTimer); animTimer = null; return; }
      if (els[cur]) els[cur].classList.remove('active');
      cur += step;
      if (els[cur]) {
        els[cur].classList.add('active');
        var fieldIdx = -1;
        for(var i=0; i<RANGES.length; i++) {
          if(cur >= RANGES[i].start && cur <= RANGES[i].end) { fieldIdx = i; break; }
        }
        if(fieldIdx !== -1) stageLabel.textContent = LABELS[fieldIdx];
      }
      updateGlow(cur);
    }, 40);
  }

  function updateAnim() {
    var lastFilled = -1;
    for (var i = 0; i < inps.length; i++) {
      if (inps[i] && inps[i].value.trim().length > 0) lastFilled = i;
    }
    var target = lastFilled === -1 ? 0 : RANGES[lastFilled].end;
    goToFrame(target);
  }

  inps.forEach(function(inp) {
    if(inp) {
      inp.addEventListener('input', updateAnim);
      inp.addEventListener('focus', updateAnim);
    }
  });

  // Initial update
  updateAnim();

  // AJAX & Sync validations
  function setValid(inp, isValid, msgEl, msgText) {
    var iw = inp.closest('.iw');
    if (isValid) {
      iw.classList.remove('is-invalid');
      iw.classList.add('is-valid');
      if (msgEl) { msgEl.textContent = ''; msgEl.classList.remove('show'); }
    } else {
      iw.classList.remove('is-valid');
      iw.classList.add('is-invalid');
      if (msgEl) { msgEl.textContent = msgText; msgEl.classList.add('show'); }
    }
  }

  function clearState(inp, msgEl) {
    var iw = inp.closest('.iw');
    iw.classList.remove('is-valid', 'is-invalid');
    if (msgEl) { msgEl.textContent = ''; msgEl.classList.remove('show'); }
  }

  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  let timerMap = {};

  const userInp = document.getElementById('userInput');
  const msgUser = document.getElementById('msgUser');
  if(userInp){
    userInp.addEventListener('input', function() {
      clearTimeout(timerMap['user']);
      let val = this.value.trim();
      if (!val) { clearState(this, msgUser); return; }
      timerMap['user'] = setTimeout(() => {
        const url = (window.SISART_CONFIG && window.SISART_CONFIG.checkUsernameUrl) ? window.SISART_CONFIG.checkUsernameUrl : '/accounts/check-username/';
        fetch(url + '?username=' + encodeURIComponent(val))
          .then(r => r.json())
          .then(data => {
            if (data.is_taken) setValid(userInp, false, msgUser, 'Usuario ya existe.');
            else setValid(userInp, true, msgUser);
          })
          .catch(err => console.error('Error checking username:', err));
      }, 400);
    });
  }

  const emailInp = document.getElementById('emailInput');
  const msgEmail = document.getElementById('msgEmail');
  if(emailInp){
    emailInp.addEventListener('input', function() {
      clearTimeout(timerMap['email']);
      let val = this.value.trim();
      if (!val) { clearState(this, msgEmail); return; }
      if (!emailRegex.test(val)) { setValid(this, false, msgEmail, 'Correo inválido.'); return; }
      timerMap['email'] = setTimeout(() => {
        const url = (window.SISART_CONFIG && window.SISART_CONFIG.checkEmailUrl) ? window.SISART_CONFIG.checkEmailUrl : '/accounts/check-email/';
        fetch(url + '?email=' + encodeURIComponent(val))
          .then(r => r.json())
          .then(data => {
            if (data.is_taken) setValid(emailInp, false, msgEmail, 'Este correo ya está registrado.');
            else setValid(emailInp, true, msgEmail);
          })
          .catch(err => console.error('Error checking email:', err));
      }, 400);
    });
  }

  const passInp = document.getElementById('passInput');
  const confirmInp = document.getElementById('passConfirmInput');
  const msgPass = document.getElementById('msgPass');
  const msgConfirm = document.getElementById('msgConfirm');

  if(passInp){
    passInp.addEventListener('input', function() {
      let val = this.value;
      if (!val) { clearState(this, msgPass); return; }
      
      if (val.length < 8) {
          setValid(this, false, msgPass, 'Mínimo 8 caracteres.');
      } else if (!/[A-Z]/.test(val)) {
          setValid(this, false, msgPass, 'Falta una mayúscula.');
      } else if (!/[a-z]/.test(val)) {
          setValid(this, false, msgPass, 'Falta una minúscula.');
      } else if (!/[0-9]/.test(val)) {
          setValid(this, false, msgPass, 'Falta un número.');
      } else if (!/[^a-zA-Z0-9]/.test(val)) {
          setValid(this, false, msgPass, 'Falta un símbolo.');
      } else {
          setValid(this, true, msgPass);
      }
      
      if (confirmInp.value) confirmInp.dispatchEvent(new Event('input'));
    });
  }

  if(confirmInp){
    confirmInp.addEventListener('input', function() {
      let val = this.value;
      if (!val) { clearState(this, msgConfirm); return; }
      if (val !== passInp.value) setValid(this, false, msgConfirm, 'No coinciden.');
      else if(val.length >= 8) setValid(this, true, msgConfirm);
    });
  }

  const nInp = document.getElementById('nameInput');
  const lInp = document.getElementById('lastNameInput');
  [nInp, lInp].forEach(el => {
    if(el){ el.addEventListener('input', function() {
      if(this.value.trim().length > 1) setValid(this, true, null);
      else clearState(this, null);
    });}
  });
})();