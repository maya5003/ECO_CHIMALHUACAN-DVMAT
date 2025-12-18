// -------------------
// GLOBAL
// -------------------

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let keys = {};
let enemies = [];

let score = 0;
let lives = 3;
let gameRunning = false;

// -------------------
// IMÁGENES
// -------------------

const playerImg = new Image();
playerImg.src = "../static/img/Juegos/player.png";

const sprites = [
    "../static/img/Juegos/botella.png",
    "../static/img/Juegos/lata.png",
    "../static/img/Juegos/papel.png",
    "../static/img/Juegos/plastico.png"
];

// -------------------
// OBJETOS
// -------------------

let player = {
    x: canvas.width / 2 - 20,
    y: canvas.height - 80,
    width: 40,
    height: 40,
    speed: 5
};

// -------------------
// EVENTOS
// -------------------

document.addEventListener("keydown", e => keys[e.code] = true);
document.addEventListener("keyup", e => keys[e.code] = false);

// -------------------
// INICIAR JUEGO
// -------------------

document.getElementById("startBtn").addEventListener("click", () => {
    document.getElementById("menu").style.display = "none";
    canvas.style.display = "block";

    score = 0;
    lives = 3;
    enemies = [];

    gameRunning = true;
    gameLoop();
});

// -------------------
// REINICIAR
// -------------------

document.getElementById("restartBtn").addEventListener("click", () => {
    document.getElementById("gameOver").style.display = "none";
    canvas.style.display = "block";

    score = 0;
    lives = 3;
    enemies = [];

    gameRunning = true;
    gameLoop();
});

// -------------------
// COLISIONES
// -------------------

function collide(a, b) {
    return (
        a.x < b.x + b.width &&
        a.x + a.width > b.x &&
        a.y < b.y + b.height &&
        a.y + a.height > b.y
    );
}

// -------------------
// CREACIÓN DE ENEMIGOS
// -------------------

setInterval(() => {
    if (!gameRunning) return;

    let img = new Image();
    img.src = sprites[Math.floor(Math.random() * sprites.length)];

    enemies.push({
        x: Math.random() * (canvas.width - 40),
        y: -40,
        width: 40,
        height: 40,
        speed: 2,
        zigzag: Math.random() < 0.5 ? -1 : 1,
        img: img
    });
}, 900);

// -------------------
// UPDATE
// -------------------

function update() {
    if (!gameRunning) return;

    if (keys["ArrowLeft"]) player.x -= player.speed;
    if (keys["ArrowRight"]) player.x += player.speed;

    player.x = Math.max(0, Math.min(player.x, canvas.width - player.width));

    enemies.forEach(e => {
        e.y += e.speed;
        e.x += e.zigzag * 2;

        if (e.x <= 0 || e.x >= canvas.width - e.width) {
            e.zigzag *= -1;
        }
    });

    enemies.forEach((e, ei) => {
        if (collide(e, player)) {
            enemies.splice(ei, 1);
            score++;
        }
    });

    enemies.forEach((e, ei) => {
        if (e.y > canvas.height) {
            enemies.splice(ei, 1);
            lives--;

            if (lives <= 0) endGame();
        }
    });
}

// -------------------
// DRAW
// -------------------

function draw() {
    if (!gameRunning) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.drawImage(playerImg, player.x, player.y, player.width, player.height);

    enemies.forEach(e => {
        ctx.drawImage(e.img, e.x, e.y, e.width, e.height);
    });

    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.fillText("Score: " + score, 10, 30);
    ctx.fillText("Vidas: " + lives, 10, 55);
}

// -------------------
// LOOP PRINCIPAL
// -------------------

function gameLoop() {
    if (!gameRunning) return;

    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// -------------------
// GAME OVER
// -------------------

function endGame() {
    gameRunning = false;
    canvas.style.display = "none";
    document.getElementById("gameOver").style.display = "block";
    document.getElementById("finalScore").innerText = "Puntaje: " + score;
}
