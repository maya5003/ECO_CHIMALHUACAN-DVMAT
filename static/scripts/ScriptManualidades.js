const btnAnterior = document.getElementById('btnAnterior');
const btnSiguiente = document.getElementById('btnSiguiente');
const contenedores = document.querySelectorAll('.contenedor');
let currentIndex = 0;
const totalContenedores = contenedores.length;

function mostrarContenedor() {
    // Ocultar todos los contenedores
    contenedores.forEach((contenedor) => {
        contenedor.style.display = 'none';
    });
    
    // Mostrar solo el contenedor actual
    contenedores[currentIndex].style.display = 'block';
}

function siguiente() {
    currentIndex = (currentIndex + 1) % totalContenedores;
    mostrarContenedor();
}

function anterior() {
    currentIndex = (currentIndex - 1 + totalContenedores) % totalContenedores;
    mostrarContenedor();
}

btnSiguiente.addEventListener('click', siguiente);
btnAnterior.addEventListener('click', anterior);

// Inicializar - mostrar solo el primer contenedor
mostrarContenedor();
