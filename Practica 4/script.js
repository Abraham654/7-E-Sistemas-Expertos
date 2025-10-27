
// Flood Among Us - Itch.io HTML prototype (UNSC Emblem + immersive audio)
// Data
const characters = [
  "Jefe Maestro John-117",
  "Sargento Johnson",
  "Emile-A239",
  "Inquisidor Thel 'Vadam",
  "Comandante Lazky"
];
const locations = [
  "Puente de mando",
  "Armería",
  "Hangar de Pelicans",
  "Centro de mando táctico (Combat Deck / CIC)",
  "Bahía de mantenimiento (Maintenance Bay)"
];
const weapons = ["Escopeta","Espada de energía","Rifle de asalto","Magnum","Rifle de plasma"];

const narratives = {
  "Jefe Maestro John-117": "Mientras la Infinity navegaba por un cúmulo de remanentes Forerunner, el Jefe Maestro se encontró en el {location} revisando coordenadas. Una explosión de violencia: un enfrentamiento directo. Las marcas en la escena indican que el responsable usó un(a) {weapon} de corto alcance y precisión. ¿Por qué Master Chief? La evidencia sugiere un intento de contener una infección, pero algo salió mal...",
  "Sargento Johnson": "El Sargento Johnson, siempre con bromas en su boca, quedó contra las cuerdas en el {location}. Testigos escucharon gritos y el sonido rítmico de recargas: el arma era un(a) {weapon}. ¿Había decidido eliminar a un infectado a la fuerza o fue traicionado? El polvo de pólvora y restos de armadura cuentan la historia...",
  "Emile-A239": "Emile-A239 operaba en silencio en la {location}, sus tácticas letales son conocidas. El arma encontrada es un(a) {weapon}, con rastros que coinciden con técnicas de combate cuerpo a cuerpo. Alguien intentó entrar sigilosamente para neutralizar la amenaza; sin embargo, las huellas muestran que la situación escaló demasiado rápido...",
  "Inquisidor Thel 'Vadam": "Thel 'Vadam fue visto cerca del {location} minutos antes del incidente. Como inquisidor, su propósito es purgar la disidencia; el arma hallada, un(a) {weapon}, sugiere una ejecución ritual más que un duelo. ¿Protegía Covenant la seguridad o buscaba un objetivo propio?",
  "Comandante Lazky": "El Comandante Lazky manejaba la logística en la {location}. Entre chispas y herramientas, apareció el(a) {weapon}. El área de mantenimiento alberga secretos: filtros contaminados y sistemas alterados. ¿Fue Lazky un saboteador o un sabio que intentó detener la propagación a cualquier costo?"
};

// Preset deterministic cases (one per character)
const presetCases = [
  {culprit: characters[0], weapon: weapons[0], location: locations[0]},
  {culprit: characters[1], weapon: weapons[3], location: locations[1]},
  {culprit: characters[2], weapon: weapons[2], location: locations[2]},
  {culprit: characters[3], weapon: weapons[4], location: locations[3]},
  {culprit: characters[4], weapon: weapons[1], location: locations[4]}
];

// UI refs
const boot = document.getElementById('boot-screen');
const game = document.getElementById('game');
const audioAmbient = document.getElementById('audioAmbient');
const audioBeep = document.getElementById('audioBeep');
const audioClick = document.getElementById('audioClick');
const audioError = document.getElementById('audioError');

const selPerson = document.getElementById('selPerson');
const selWeapon = document.getElementById('selWeapon');
const selLocation = document.getElementById('selLocation');
const narrativeEl = document.getElementById('narrative');
const btnStart = document.getElementById('btnStart');
const btnAccuse = document.getElementById('btnAccuse');
const btnReveal = document.getElementById('btnReveal');
const btnReset = document.getElementById('btnReset');
const attemptsEl = document.getElementById('attempts');
const gameState = document.getElementById('gameState');
const feedbackArea = document.getElementById('feedbackArea');
const audioToggle = document.getElementById('audioToggle');

// Populate selects
function populateSelects(){
  selPerson.innerHTML = '<option value="">-- Selecciona --</option>' + characters.map(c => '<option>'+c+'</option>').join('');
  selWeapon.innerHTML = '<option value="">-- Selecciona --</option>' + weapons.map(w => '<option>'+w+'</option>').join('');
  selLocation.innerHTML = '<option value="">-- Selecciona --</option>' + locations.map(l => '<option>'+l+'</option>').join('');
}
populateSelects();

let currentCase = null;
let attempts = 3;
let audioEnabled = false;

// Boot sequence: wait for any key press
setTimeout(function(){
  boot.classList.add('boot-show');
}, 300);

function endBoot(){
  audioBeep.play().catch(function(){});
  boot.classList.add('hidden');
  game.classList.remove('hidden');
  gameState.textContent = 'Sistema activo - listo para análisis';
  if(audioEnabled){ audioAmbient.play().catch(function(){}); }
}

document.addEventListener('keydown', function(e){
  if(!boot.classList.contains('hidden')){
    endBoot();
  }
});

audioToggle.addEventListener('click', function(){
  audioEnabled = !audioEnabled;
  audioToggle.textContent = audioEnabled? 'Audio: ON' : 'Activar audio';
  if(audioEnabled){ audioAmbient.play().catch(function(){}); audioBeep.play().catch(function(){}); } else { audioAmbient.pause(); audioAmbient.currentTime = 0; }
});

function generateRandomCase(){
  var culprit = characters[Math.floor(Math.random()*characters.length)];
  var weapon = weapons[Math.floor(Math.random()*weapons.length)];
  var location = locations[Math.floor(Math.random()*locations.length)];
  renderCase({culprit:culprit,weapon:weapon,location:location});
}

function renderCase(c){
  currentCase = c;
  attempts = 3;
  attemptsEl.textContent = attempts;
  gameState.textContent = 'Caso cargado - acceso a análisis';
  feedbackArea.innerHTML = '';
  var base = narratives[c.culprit];
  var text = base.replace('{location}', c.location).replace('{weapon}', c.weapon);
  narrativeEl.textContent = text;
}

document.querySelectorAll('.preset-list [data-case]').forEach(function(btn){
  btn.addEventListener('click', function(){
    var idx = parseInt(btn.getAttribute('data-case'));
    renderCase(presetCases[idx]);
    audioClick.play().catch(function(){});
  });
});

btnStart.addEventListener('click', function(){
  generateRandomCase();
  audioClick.play().catch(function(){});
});

btnReset.addEventListener('click', function(){
  currentCase = null;
  narrativeEl.textContent = 'Presiona Iniciar análisis para generar un caso.';
  attemptsEl.textContent = '—';
  gameState.textContent = 'Esperando...';
  feedbackArea.innerHTML = '';
  audioClick.play().catch(function(){});
});

btnAccuse.addEventListener('click', function(){
  if(!currentCase){ alert('Genera o carga un caso primero.'); return; }
  var guessPerson = selPerson.value;
  var guessWeapon = selWeapon.value;
  var guessLocation = selLocation.value;
  if(!guessPerson || !guessWeapon || !guessLocation){ alert('Debes seleccionar personaje, arma y ubicación.'); return; }

  var correctPerson = guessPerson === currentCase.culprit;
  var correctWeapon = guessWeapon === currentCase.weapon;
  var correctLocation = guessLocation === currentCase.location;

  if(correctPerson && correctWeapon && correctLocation){
    feedbackArea.innerHTML = '<div class="panel-card" style="border:1px solid rgba(0,200,255,0.08);box-shadow:0 12px 40px rgba(0,214,255,0.06)"><strong>¡Acusación correcta!</strong><div class="muted">Infección contenida. Buen trabajo, Spartan.</div></div>';
    gameState.textContent = 'Caso resuelto - victoria';
    if(audioEnabled){ audioClick.play().catch(function(){}); }
    return;
  }

  var fb = '<div class="panel-card"><div><strong>Feedback parcial:</strong></div><ul style="margin:8px 0 0 16px">';
  fb += (correctPerson? '<li><strong>Personaje: ✅</strong></li>' : '<li>Personaje: ❌</li>');
  fb += (correctWeapon? '<li><strong>Arma: ✅</strong></li>' : '<li>Arma: ❌</li>');
  fb += (correctLocation? '<li><strong>Ubicación: ✅</strong></li>' : '<li>Ubicación: ❌</li>');
  fb += '</ul></div>';
  feedbackArea.innerHTML = fb;
  attempts -= 1;
  attemptsEl.textContent = attempts;
  gameState.textContent = 'Análisis en curso - intentos restantes: ' + attempts;
  if(audioEnabled){ audioError.play().catch(function(){}); }
  if(attempts <= 0){
    feedbackArea.innerHTML += '<div class="panel-card" style="margin-top:8px"><strong>Se agotaron los intentos.</strong><div class="muted">Pulsa Revelar solución para conocer la verdad.</div></div>';
  }
});

btnReveal.addEventListener('click', function(){
  if(!currentCase){ alert('Genera o carga un caso primero.'); return; }
  feedbackArea.innerHTML = '<div class="panel-card"><strong>Solución</strong><div class="muted">Culpable: ' + currentCase.culprit + ' — Arma: ' + currentCase.weapon + ' — Ubicación: ' + currentCase.location + '</div></div>';
  if(audioEnabled){ audioBeep.play().catch(function(){}); }
});
