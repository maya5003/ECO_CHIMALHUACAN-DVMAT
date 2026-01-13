const input = document.getElementById('NombreLect');
const suggestions = document.getElementById('suggestions');

input.addEventListener('input', function() {
    const searchTerm = this.value.trim().toLowerCase();
    if (searchTerm.length === 0) {
        suggestions.style.display = 'none';
        return;
    }
    const matches = window.libros.filter(libro => libro.nombre.toLowerCase().startsWith(searchTerm));
    if (matches.length > 0) {
        suggestions.innerHTML = matches.map(libro => `<div style="padding: 8px; cursor: pointer; border-bottom: 1px solid #eee;" onclick="selectSuggestion('${libro.nombre}')">${libro.nombre}</div>`).join('');
        suggestions.style.display = 'block';
    } else {
        suggestions.style.display = 'none';
    }
});

function selectSuggestion(name) {
    input.value = name;
    suggestions.style.display = 'none';
}

// Ocultar sugerencias al hacer clic fuera
document.addEventListener('click', function(e) {
    if (!input.contains(e.target) && !suggestions.contains(e.target)) {
        suggestions.style.display = 'none';
    }
});

document.getElementById('btnBuscarLect').addEventListener('click', function() {
    const searchTerm = input.value.trim().toLowerCase();
    const libro = window.libros.find(l => l.nombre.toLowerCase() === searchTerm);
    if (libro) {
        document.getElementById('modal-img').src = '/static/img/Libros/' + libro.imagen;
        document.getElementById('modal-sinopsis').textContent = 'Sinopsis: ' + libro.sinopsis;
        document.getElementById('modal-descarga').href = libro.descarga;
        document.getElementById('book-modal').style.display = 'flex';
    } else {
        Swal.fire({
            iconHtml: '😢',
            title: "upss",
            text: "Lo sentimos, no podemos encontrar el material de tu busqueda, revisa si el libro que buscas esta en nuestra pagina comprueba que este bien escrito el titulo"
        });
    }
    suggestions.style.display = 'none';
});

function closeModal() {
    document.getElementById('book-modal').style.display = 'none';
}