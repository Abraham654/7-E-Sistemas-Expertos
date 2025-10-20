const arbol = {
  "es eléctrico": {
    "sí": "Tesla Model 3",
    "no": {
      "es deportivo": {
        "sí": "Ferrari 488",
        "no": "Toyota Corolla"
      }
    }
  }
};

let nodoActual = arbol;
let preguntaActual = Object.keys(nodoActual)[0];
const preguntaTexto = document.getElementById("pregunta");
const botonReiniciar = document.getElementById("reiniciar");

function mostrarPregunta() {
  if (typeof nodoActual === "string") {
    preguntaTexto.textContent = `¿Tu auto es un ${nodoActual}?`;
    botonReiniciar.style.display = "block";
  } else {
    preguntaActual = Object.keys(nodoActual)[0];
    preguntaTexto.textContent = `¿Tu auto ${preguntaActual}?`;
  }
}

function respuesta(r) {
  if (typeof nodoActual === "string") {
    preguntaTexto.textContent = "¡Ya terminé! 😄";
  } else {
    nodoActual = nodoActual[preguntaActual][r];
    mostrarPregunta();
  }
}

function reiniciar() {
  nodoActual = arbol;
  botonReiniciar.style.display = "none";
  mostrarPregunta();
}

mostrarPregunta();
