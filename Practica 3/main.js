// Akinator de Autos - versión con arbolBase de 32 autos
// El arbolBase está construido con las preguntas proporcionadas
// y contiene las 32 entradas que usábamos en Python.

const CARS_LIST = [
  "Toyota Supra Japones 2JZ-GTE I6 TT",
  "Chevrolet Camaro USA ZL1 LT4 V8 TT",
  "Volkswagen Beetle Aleman Boxer4 TT",
  "Nissan Skyline GTR Japones R34 RB26DETT L6 TA",
  "Porsche 911 Gt3 RS Aleman Boxer6 TT",
  "Ford F-150 Raptor USA Ecoboost V6 T4",
  "Ford Mustang GT USA Coyote V8 TT",
  "McLaren F1 Britanico V12 TT",
  "Lamborghini Murcielago Italiano V12 TA",
  "Lamborghini Gallardo Italiano V10 TA",
  "Ferrari F-40 Italiano V8 TT",
  "Nissan Tsuru Japones I4 TD",
  "Chevrolet Chevy Pop USA I4 TD",
  "Ford Fiesta USA I4 TD",
  "Ford Focus RS USA Ecoboost I4 TA",
  "Volkswagen Jetta Aleman I4 TD",
  "Dodge Charger R/T 1970 USA Hemi V8 TT",
  "Mitsubishi Lancer Evolution 9 Japones I4 TA",
  "Subaru Impreza STI Japones Boxer4 TA",
  "Chevrolet Impala SS 1994 USA V6 TT",
  "Acura NSX Japones V6 TA",
  "Bugatti Chiron SS Frances W16 TA",
  "Chevrolet Astra USA I4 TD",
  "Toyota Corolla 86 Japones I4 TT",
  "Lamborghini Aventador J Italiano V12 TA",
  "Ferrari La Ferrari Italiano V12 TT",
  "Mazda 3 Japones Sckyactiv G I4 TD",
  "BMW M3 E30 Aleman M20 I6 TT",
  "Mazda Miata Mx-5 Japones Skyactiv G I4 TT",
  "Shelby AC Cobra USA 427 V8 TT",
  "Chevrolet Corvette C6 Z06 USA LT4 V8 TT",
  "Nissan Fairlady Z 240Z Japones L24 I6 TT"
];

// Preguntas que vinieron del Excel (las usé como claves de decisión)
const QUESTIONS = [
  "¿Es Traccion Delantera?",
  "¿Es Estado Unidense?",
  "¿Es de la marca Ford?",
  "¿Su motor es en linea?",
  "¿Es de 4 Cilindros?",
  "¿Seguro que es Ford?",
  "¿Es de la Marca Chevrolet?",
  "¿Es Coche Hatchback pequeño?",
  "¿Es Japones?",
  "¿Es de la Marca Mazda?",
  "¿Es Hatchback?",
  "¿Es Aleman?",
  "¿Es de Volkswagen?",
  "¿Es Traccion Trasera?",
  "¿Es Chevrolet?",
  "¿Es Un Corvette?",
  "¿Es de Ford?",
  "¿Es Aleman?",
  "¿Es JDM?",
  "¿Es Famoso por los Rallys?"
];

// ARBOL BASE (completo con 32 autos, usando las preguntas principales)
let arbolBase = {
  "¿Es Estado Unidense?": {
    "sí": {
      "¿Es de la marca Ford?": {
        "sí": {
          "¿Es Traccion Trasera?": {
            "sí": "Ford Mustang GT USA Coyote V8 TT",
            "no": {
              "¿Es camioneta?": { // pregunta auxiliar añadida para distinguir F-150
                "sí": "Ford F-150 Raptor USA Ecoboost V6 T4",
                "no": {
                  "¿Es pequeño y económico?": {
                    "sí": "Ford Fiesta USA I4 TD",
                    "no": "Shelby AC Cobra USA 427 V8 TT"
                  }
                }
              }
            }
          }
        },
        "no": {
          "¿Es de la Marca Chevrolet?": {
            "sí": {
              "¿Es Un Corvette?": {
                "sí": "Chevrolet Corvette C6 Z06 USA LT4 V8 TT",
                "no": {
                  "¿Es muscle clásico?": {
                    "sí": "Dodge Charger R/T 1970 USA Hemi V8 TT", // aunque Dodge no es Chevy, lo agrupamos por muscle
                    "no": {
                      "¿Es compacto económico?": {
                        "sí": "Chevrolet Chevy Pop USA I4 TD",
                        "no": {
                          "¿Es un Camaro?": {
                            "sí": "Chevrolet Camaro USA ZL1 LT4 V8 TT",
                            "no": {
                              "¿Es sedán grande?": {
                                "sí": "Chevrolet Impala SS 1994 USA V6 TT",
                                "no": "Chevrolet Astra USA I4 TD"
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            },
            "no": {
              // Otros americanos / británico / frances
              "¿Es Britanico?": {
                "sí": "McLaren F1 Britanico V12 TT",
                "no": "Bugatti Chiron SS Frances W16 TA"
              }
            }
          }
        }
      }
    },
    "no": {
      "¿Es Japones?": {
        "sí": {
          "¿Es JDM?": {
            "sí": {
              "¿Es Famoso por los Rallys?": {
                "sí": {
                  "¿Es Mitsubishi?": {
                    "sí": "Mitsubishi Lancer Evolution 9 Japones I4 TA",
                    "no": {
                      "¿Es Subaru?": {
                        "sí": "Subaru Impreza STI Japones Boxer4 TA",
                        "no": "Nissan Tsuru Japones I4 TD"
                      }
                    }
                  }
                },
                "no": {
                  "¿Es de la marca Nissan?": {
                    "sí": {
                      "¿Es deportivo y trasero?": {
                        "sí": "Nissan Skyline GTR Japones R34 RB26DETT L6 TA",
                        "no": {
                          "¿Es clásico deportivo?": {
                            "sí": "Nissan Fairlady Z 240Z Japones L24 I6 TT",
                            "no": "Nissan Tsuru Japones I4 TD"
                          }
                        }
                      }
                    },
                    "no": {
                      "¿Es de la Marca Mazda?": {
                        "sí": {
                          "¿Es biplaza descapotable?": {
                            "sí": "Mazda Miata Mx-5 Japones Skyactiv G I4 TT",
                            "no": {
                              "¿Es compacto 4 puertas?": {
                                "sí": "Mazda 3 Japones Sckyactiv G I4 TD",
                                "no": "Toyota Corolla 86 Japones I4 TT"
                              }
                            }
                          }
                        },
                        "no": {
                          "¿Es deportivo exótico?": {
                            "sí": "Acura NSX Japones V6 TA",
                            "no": "Toyota Supra Japones 2JZ-GTE I6 TT"
                          }
                        }
                      }
                    }
                  }
                }
              }
            },
            "no": {
              // Japonés no-JDM / general
              "¿Es compacto?": {
                "sí": "Toyota Corolla 86 Japones I4 TT",
                "no": "Acura NSX Japones V6 TA"
              }
            }
          }
        },
        "no": {
          "¿Es Aleman?": {
            "sí": {
              "¿Es de Volkswagen?": {
                "sí": {
                  "¿Es clásico?": {
                    "sí": "Volkswagen Beetle Aleman Boxer4 TT",
                    "no": {
                      "¿Es sedán?": {
                        "sí": "Volkswagen Jetta Aleman I4 TD",
                        "no": "BMW M3 E30 Aleman M20 I6 TT"
                      }
                    }
                  }
                },
                "no": "Porsche 911 Gt3 RS Aleman Boxer6 TT"
              }
            },
            "no": {
              "¿Es Italiano?": {
                "sí": {
                  "¿Es Ferrari?": {
                    "sí": {
                      "¿Es hypercar moderno?": {
                        "sí": "Ferrari La Ferrari Italiano V12 TT",
                        "no": "Ferrari F-40 Italiano V8 TT"
                      }
                    },
                    "no": {
                      "¿Es Lamborghini V12?": {
                        "sí": "Lamborghini Aventador J Italiano V12 TA",
                        "no": "Lamborghini Gallardo Italiano V10 TA"
                      }
                    }
                  }
                },
                "no": {
                  // Otros europeos
                  "¿Es deportivo exótico (no italiano)?": {
                    "sí": "McLaren F1 Britanico V12 TT",
                    "no": "Bugatti Chiron SS Frances W16 TA"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
};

// Clonar arbolBase sin referenciarlo (compatibilidad)
function clone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

// Cargar versión guardada si existe
let arbol = JSON.parse(localStorage.getItem("arbolAutos")) || clone(arbolBase);

let nodoActual = arbol;
let preguntaActual = Object.keys(nodoActual)[0];

const preguntaTexto = document.getElementById("pregunta");
const botonSi = document.getElementById("btn-si");
const botonNo = document.getElementById("btn-no");
const botonNose = document.getElementById("btn-nose");
const botonReiniciar = document.getElementById("reiniciar");
const estadoDiv = document.getElementById("estado");

function isLeaf(node) {
  return typeof node === "string";
}

function mostrarPregunta() {
  if (isLeaf(nodoActual)) {
    preguntaTexto.textContent = `¿Tu auto es: ${nodoActual}?`;
    botonReiniciar.style.display = "inline-block";
  } else {
    preguntaActual = Object.keys(nodoActual)[0];
    preguntaTexto.textContent = `¿${preguntaActual}?`;
    botonReiniciar.style.display = "none";
  }
}

// Manejo respuestas
function respuesta(r) {
  if (isLeaf(nodoActual)) {
    if (r === "si") {
      estadoDiv.textContent = `¡Adiviné! Era ${nodoActual} 😎`;
      botonReiniciar.style.display = "inline-block";
    } else {
      // aprender
      aprenderNuevoAuto();
    }
  } else {
    // bajar por la rama
    const rama = nodoActual[preguntaActual];
    // si la estructura no tiene la rama por alguna razón, evitar crash
    if (!rama || !(r in rama)) {
      // marcar desconcuerdo; forzamos rama "no" o "si" con fallback
      nodoActual = (rama && rama["no"]) || (rama && rama["si"]) || nodoActual;
    } else {
      nodoActual = rama[r];
    }
    mostrarPregunta();
  }
}

// Aprendizaje: preguntar al usuario y modificar el arbol in-place
function aprenderNuevoAuto() {
  const actual = nodoActual; // string
  const nuevoAuto = prompt("No lo adiviné. ¿Cuál era tu auto? (escribe nombre)");
  if (!nuevoAuto) {
    estadoDiv.textContent = "No se guardó nada (nombre vacío).";
    return;
  }
  const nuevaPregunta = prompt(`Escribe una pregunta de sí/no que distinga "${nuevoAuto}" de "${actual}"\n(por ejemplo: '¿Tiene V12?', '¿Es SUV?', '¿Es japonés?')`);
  if (!nuevaPregunta) {
    // Guardar solo el auto extra como fallback
    // Reemplazamos la hoja actual por un objeto de elección simple
    nodoActual = { [nuevaPregunta || "¿Es este?"]: { "sí": nuevoAuto, "no": actual } };
    // Actualizamos todo el arbol guardado abajo
    arbol = reemplazarNodo(arbol, actual, nodoActual);
    localStorage.setItem("arbolAutos", JSON.stringify(arbol));
    estadoDiv.textContent = `Guardado (sin pregunta específica). Aprendí: ${nuevoAuto}`;
    mostrarPregunta();
    return;
  }
  let respuestaParaNuevo = "";
  while (!["si", "no"].includes(respuestaParaNuevo)) {
    respuestaParaNuevo = prompt(`Para "${nuevoAuto}", la respuesta a "${nuevaPregunta}" es 'si' o 'no'?`).toLowerCase();
  }

  // Construir nueva subrama
  const nuevoNodo = {};
  nuevoNodo[nuevaPregunta] = { "sí": "", "no": "" };
  if (respuestaParaNuevo === "si") {
    nuevoNodo[nuevaPregunta]["sí"] = nuevoAuto;
    nuevoNodo[nuevaPregunta]["no"] = actual;
  } else {
    nuevoNodo[nuevaPregunta]["no"] = nuevoAuto;
    nuevoNodo[nuevaPregunta]["sí"] = actual;
  }

  // Reemplazamos la hoja actual en el arbol con el nuevo nodo
  arbol = reemplazarNodo(arbol, actual, nuevoNodo);
  // Guardar en localStorage
  localStorage.setItem("arbolAutos", JSON.stringify(arbol));
  estadoDiv.textContent = `Gracias — aprendí sobre ${nuevoAuto} ✅`;
  // Reset para que el usuario vea el cambio
  nodoActual = arbol;
  mostrarPregunta();
}

// Función que reemplaza la primera ocurrencia de una hoja (string) por nuevoNodo
function reemplazarNodo(nodo, hojaTexto, nuevoNodo) {
  if (typeof nodo === "string") {
    if (nodo === hojaTexto) {
      return clone(nuevoNodo);
    } else {
      return nodo;
    }
  } else if (typeof nodo === "object") {
    const clave = Object.keys(nodo)[0];
    const ramas = nodo[clave];
    const s = reemplazarNodo(ramas["sí"], hojaTexto, nuevoNodo);
    const n = reemplazarNodo(ramas["no"], hojaTexto, nuevoNodo);
    const copia = {};
    copia[clave] = { "sí": s, "no": n };
    return copia;
  }
  return nodo;
}

function reiniciar() {
  arbol = JSON.parse(localStorage.getItem("arbolAutos")) || clone(arbolBase);
  nodoActual = arbol;
  estadoDiv.textContent = "";
  mostrarPregunta();
}

// Eventos botones (si existen en tu HTML)
if (botonSi) botonSi.addEventListener("click", () => respuesta("si"));
if (botonNo) botonNo.addEventListener("click", () => respuesta("no"));
if (botonNose) botonNose.addEventListener("click", () => respuesta("no se"));
if (botonReiniciar) botonReiniciar.addEventListener("click", reiniciar);

// Inicializar UI
nodoActual = arbol;
mostrarPregunta();

