let objetoActual = null;
let puntaje = 0;
let tiempo = 10;
let intervalo = null;
const PUNTAJE_GANAR = 10;

function cargarObjeto() {
    fetch("/objeto")
        .then(response => response.json())
        .then(data => {
            objetoActual = data;
            document.getElementById("objeto").innerText = data.nombre;
            document.getElementById("mensaje").innerText = "";
            reiniciarTiempo();
        });
}

function responder(respuestaJugador) {
    if (!objetoActual) return;

    if (respuestaJugador === objetoActual.recicla) {
        puntaje++;
        document.getElementById("mensaje").innerText = "✅ Correcto";
    } else {
        puntaje--;
        document.getElementById("mensaje").innerText = "❌ Incorrecto";
    }

    document.getElementById("puntaje").innerText = puntaje;

    if (puntaje >= PUNTAJE_GANAR) {
        ganar();
        return;
    }

    cargarObjeto();
}

function reiniciarTiempo() {
    clearInterval(intervalo);
    tiempo = 10;
    document.getElementById("tiempo").innerText = tiempo;

    intervalo = setInterval(() => {
        tiempo--;
        document.getElementById("tiempo").innerText = tiempo;

        if (tiempo <= 0) {
            clearInterval(intervalo);
            puntaje--;
            document.getElementById("puntaje").innerText = puntaje;
            document.getElementById("mensaje").innerText = "⏰ Tiempo agotado";
            cargarObjeto();
        }
    }, 1000);
}

function ganar() {
    clearInterval(intervalo);
    document.getElementById("pantalla-juego").style.display = "none";
    document.getElementById("pantalla-ganar").style.display = "block";
    document.getElementById("puntaje-final").innerText = puntaje;
}

function reiniciar() {
    puntaje = 0;
    document.getElementById("puntaje").innerText = puntaje;
    document.getElementById("pantalla-ganar").style.display = "none";
    document.getElementById("pantalla-juego").style.display = "block";
    cargarObjeto();
}

cargarObjeto();
