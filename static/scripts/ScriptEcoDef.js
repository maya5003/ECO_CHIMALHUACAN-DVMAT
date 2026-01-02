// 🎮 --- CONFIGURACIÓN BÁSICA ---
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const scoreEl = document.getElementById('score');
const vidasEl = document.getElementById('vidas');
const nivelEl = document.getElementById('nivel');

// --- VARIABLES GLOBALES ---
let score = 0;
let vidas = 3;
let nivel = 1;
let direccion = 1;
let velocidadEnemigos = 2;
let enBonus = false;
let bonusTimer = 0;
let juegoTerminado = false;
let intervaloBonus = null; // nuevo: control del temporizador del bonus

// Control del disparo
let puedeDisparar = true;
const tiempoEntreDisparos = 150; // milisegundos

// --- IMÁGENES ---
const naveImg = new Image();
naveImg.src = "../static/img/Juegos/Eco_Defensor/nave.png";

const enemigoImg = new Image(); // botella
enemigoImg.src = "../static/img/Juegos/Eco_Defensor/enemigo.png";

const explosionImg = new Image();
explosionImg.src = "../static/img/Juegos/Eco_Defensor/explosion.png";

let naveCargada = false;
let enemigoCargado = false;
let explosionCargada = false;

naveImg.onload = () => naveCargada = true;
enemigoImg.onload = () => enemigoCargado = true;
explosionImg.onload = () => explosionCargada = true;

// --- NAVE ---
const nave = {
    x: canvas.width / 2 - 20,
    y: canvas.height - 60,
    width: 40,
    height: 40,
    speed: 7
};

// --- ARRAYS ---
const balas = [];
const enemigos = [];
const explosiones = [];

const filas = 3;
const columnas = 6;
const enemigoWidth = 40;
const enemigoHeight = 40;

// --- CONTROLES ---
let izquierda = false;
let derecha = false;

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') izquierda = true;
    if (e.key === 'ArrowRight') derecha = true;

    // Limitador de disparo
    if (e.key === ' ' && !juegoTerminado && puedeDisparar) {
        puedeDisparar = false;
        balas.push({ x: nave.x + nave.width / 2 - 2, y: nave.y, width: 4, height: 10 });
        setTimeout(() => puedeDisparar = true, tiempoEntreDisparos);
    }
});

document.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowLeft') izquierda = false;
    if (e.key === 'ArrowRight') derecha = false;
});

// --- FUNCIÓN PRINCIPAL ---
function gameLoop() {
    if (juegoTerminado) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Mover nave
    if (izquierda && nave.x > 0) nave.x -= nave.speed;
    if (derecha && nave.x + nave.width < canvas.width) nave.x += nave.speed;

    // Dibujar nave
    ctx.drawImage(naveImg, nave.x, nave.y, nave.width, nave.height);

    // Mover y dibujar balas
    for (let i = 0; i < balas.length; i++) {
        balas[i].y -= 7;
        ctx.fillStyle = 'white';
        ctx.fillRect(balas[i].x, balas[i].y, balas[i].width, balas[i].height);

        // Colisión con enemigos
        for (let j = 0; j < enemigos.length; j++) {
            const e = enemigos[j];
            if (!e.hits) e.hits = 1;

            if (
                balas[i].x < e.x + e.width &&
                balas[i].x + balas[i].width > e.x &&
                balas[i].y < e.y + e.height &&
                balas[i].y + balas[i].height > e.y
            ) {
                e.hits--;
                balas.splice(i, 1);
                i--;

                if (e.hits <= 0) {
                    // 💥 Crear explosión
                    explosiones.push({
                        x: e.x - e.width * 0.25,
                        y: e.y - e.height * 0.25,
                        width: e.width * 1.5,
                        height: e.height * 1.5,
                        timer: 15
                    });

                    enemigos.splice(j, 1);
                    score += 10;

                    // Si estamos en el bonus, reponer enemigo
                    if (enBonus) {
                        enemigos.push(crearEnemigoAleatorio());
                    }
                }
                break;
            }
        }
    }

    // Mover enemigos
    let cambiarDireccion = false;
    enemigos.forEach(e => {
        e.x += velocidadEnemigos * direccion;
        if (e.x + e.width >= canvas.width || e.x <= 0) cambiarDireccion = true;
    });

    if (cambiarDireccion) {
        direccion *= -1;
        enemigos.forEach(e => e.y += 20);
    }

    // Dibujar enemigos
    enemigos.forEach(e => ctx.drawImage(enemigoImg, e.x, e.y, e.width, e.height));

    // Dibujar explosiones 💥
    for (let i = 0; i < explosiones.length; i++) {
        const ex = explosiones[i];
        if (explosionCargada) {
            ctx.drawImage(explosionImg, ex.x, ex.y, ex.width, ex.height);
        }
        ex.timer--;
        if (ex.timer <= 0) {
            explosiones.splice(i, 1);
            i--;
        }
    }

    // Verificar si algún enemigo llega a la nave o al fondo
    enemigos.forEach(e => {
        if (e.y + e.height >= nave.y && !enBonus) {
            vidas--;
            resetEnemies();
        }

        // 🧩 BONUS: si una botella llega al fondo, termina el bonus antes de tiempo
        if (enBonus && e.y + e.height >= canvas.height) {
            enBonus = false;
            clearInterval(intervaloBonus);
            juegoTerminado = true; // 🛑 detiene el loop
            mostrarMensaje("🌍 ¡Bonus terminado por contaminación!");
            setTimeout(() => mostrarPantallaFinal(), 2000);
            return; // 🚫 corta el frame actual
        }
    });

    // Actualizar panel
    scoreEl.textContent = score;
    vidasEl.textContent = vidas;
    nivelEl.textContent = enBonus ? `BONUS (${bonusTimer}s)` : nivel;

    // Fin de nivel normal
    if (!enBonus && enemigos.length === 0) {
        nivel++;
        if (nivel === 3) {
            iniciarBonus();
            return;
        }
        if (nivel > 3) {
            mostrarPantallaFinal();
            return;
        }
        mostrarMensaje(`¡Nivel ${nivel}!`);
        setTimeout(() => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            resetEnemies();
        }, 2000);
        return;
    }

    if (vidas > 0) {
        requestAnimationFrame(gameLoop);
    } else {
        mostrarJuegoTerminado();
    }
}

// --- FUNCIONES AUXILIARES ---
function crearEnemigoAleatorio() {
    return {
        x: Math.random() * (canvas.width - 40),
        y: Math.random() * (canvas.height / 2),
        width: enemigoWidth,
        height: enemigoHeight,
        hits: 1
    };
}

function resetEnemies() {
    enemigos.length = 0;
    if (enBonus) return;

    for (let row = 0; row < filas; row++) {
        for (let col = 0; col < columnas; col++) {
            let vidaEnemigo = nivel === 2 ? 3 : 1;
            enemigos.push({
                x: 60 + col * 80,
                y: 50 + row * 60,
                width: enemigoWidth,
                height: enemigoHeight,
                hits: vidaEnemigo
            });
        }
    }

    direccion = (nivel === 2) ? -1 : 1;
    velocidadEnemigos = 1 + (nivel - 1) * 1.2;
    nave.x = canvas.width / 2 - 20;
    requestAnimationFrame(gameLoop);
}

// --- BONUS ---
function iniciarBonus() {
    enBonus = true;
    bonusTimer = 30;
    mostrarMensaje("🌟 Nivel Bonus 🌟");

    setTimeout(() => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        enemigos.length = 0;
        for (let i = 0; i < 8; i++) {
            enemigos.push(crearEnemigoAleatorio());
        }
        iniciarTemporizadorBonus();
        requestAnimationFrame(gameLoop);
    }, 2000);
}

function iniciarTemporizadorBonus() {
    clearInterval(intervaloBonus); // asegura que no haya uno previo
    intervaloBonus = setInterval(() => {
        if (!enBonus) {
            clearInterval(intervaloBonus);
            return;
        }

        bonusTimer--;
        nivelEl.textContent = `BONUS (${bonusTimer}s)`;

        if (bonusTimer <= 0 && enBonus) {
            clearInterval(intervaloBonus);
            enBonus = false;
            nivel++;
            mostrarPantallaFinal();
        }
    }, 1000);
}

// --- PANTALLA FINAL ---
function mostrarPantallaFinal() {
    juegoTerminado = true;
    clearInterval(intervaloBonus); // asegura que el temporizador pare
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#0b1c2d';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = 'yellow';
    ctx.font = '48px Arial';
    ctx.fillText('¡Felicidades Guardián! 🌎', canvas.width / 2, canvas.height / 2 - 80);

    ctx.fillStyle = 'white';
    ctx.font = '30px Arial';
    ctx.fillText('Has completado la misión.', canvas.width / 2, canvas.height / 2 - 20);
    ctx.fillText(`Puntuación final: ${score}`, canvas.width / 2, canvas.height / 2 + 30);
    ctx.fillText('Gracias por jugar 💚', canvas.width / 2, canvas.height / 2 + 80);

    const restartButton = document.createElement("button");
    restartButton.textContent = "🔄 Reiniciar";
    restartButton.style.position = "absolute";
    restartButton.style.left = "50%";
    restartButton.style.top = "70%";
    restartButton.style.transform = "translate(-50%, -50%)";
    restartButton.style.padding = "10px 20px";
    restartButton.style.fontSize = "18px";
    restartButton.style.borderRadius = "10px";
    restartButton.style.cursor = "pointer";
    restartButton.style.background = "#1e90ff";
    restartButton.style.color = "white";
    restartButton.style.border = "none";
    restartButton.onclick = reiniciarJuego;
    document.body.appendChild(restartButton);
}

// --- REINICIAR JUEGO ---
function reiniciarJuego() {
    score = 0;
    vidas = 3;
    nivel = 1;
    direccion = 1;
    velocidadEnemigos = 2;
    enBonus = false;
    bonusTimer = 0;
    juegoTerminado = false;

    const button = document.querySelector("button");
    if (button) button.remove();

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    resetEnemies();
}

// --- MENSAJES ---
function mostrarMensaje(texto) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'yellow';
    ctx.font = '40px Arial';
    ctx.textAlign = "center";
    ctx.fillText(texto, canvas.width / 2, canvas.height / 2);
}

function mostrarJuegoTerminado() {
    juegoTerminado = true;
    ctx.fillStyle = 'green';
    ctx.font = '40px Arial';
    ctx.textAlign = "center";
    ctx.fillText('¡Juego Terminado!', canvas.width / 2, canvas.height / 2);
}

// --- INICIO ---
function esperarImagenes() {
    if (naveCargada && enemigoCargado && explosionCargada) {
        resetEnemies();
    } else {
        requestAnimationFrame(esperarImagenes);
    }
}

esperarImagenes();