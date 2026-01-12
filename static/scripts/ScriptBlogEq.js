// ScriptBlogEq.js - JavaScript for BlogEq.html

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to navigation links
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Placeholder for image loading or other interactions
    const images = document.querySelectorAll('img[id^="img"]');
    images.forEach(img => {
        if (!img.src || img.src === '') {
            img.src = 'https://via.placeholder.com/400x200?text=Imagen+no+disponible';
            img.alt = 'Imagen no disponible';
        }
    });

    // Add click event to blog post titles for expansion/collapse if needed
    // For now, just log clicks
    const titles = document.querySelectorAll('.titulo1, .titulo2, .titulo3, .titulo4');
    titles.forEach(title => {
        title.addEventListener('click', function() {
            console.log('Title clicked:', this.textContent);
            // Could add toggle visibility of content here
        });
    });

    // Cargar comentarios
    loadComments();

    // Manejar el envío del formulario de comentarios
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitComment();
        });
    }
});

// Función para cargar comentarios
function loadComments() {
    fetch('/obtener-comentarios-blog')
        .then(response => {
            if (response.status === 401) {
                // Usuario no autenticado
                showLoginMessage();
                return [];
            }
            return response.json();
        })
        .then(comments => {
            displayComments(comments);
        })
        .catch(error => {
            console.error('Error al cargar comentarios:', error);
        });
}

// Función para mostrar comentarios
function displayComments(comments) {
    const commentsList = document.getElementById('commentsList');
    commentsList.innerHTML = '';

    if (comments.length === 0) {
        commentsList.innerHTML = '<div class="no-comments-message">Aún no hay comentarios. ¡Sé el primero en comentar!</div>';
        return;
    }

    comments.forEach(comment => {
        const commentCard = document.createElement('div');
        commentCard.className = 'comment-card';
        commentCard.innerHTML = `
            <div class="comment-avatar">
                <img src="${comment.foto_perfil}" alt="${comment.nombre_usuario}">
            </div>
            <div class="comment-content">
                <div class="comment-header">
                    <p class="comment-username">${escapeHtml(comment.nombre_usuario)}</p>
                    <span class="comment-date">${formatDate(comment.fecha)}</span>
                </div>
                <p class="comment-text">${escapeHtml(comment.comentario)}</p>
            </div>
        `;
        commentsList.appendChild(commentCard);
    });
}

// Función para enviar un comentario
function submitComment() {
    const commentText = document.getElementById('commentText').value;

    if (!commentText.trim()) {
        Swal.fire({
            icon: 'warning',
            title: 'Campo vacío',
            text: 'Por favor, escribe un comentario.',
            confirmButtonColor: '#4CAF50'
        });
        return;
    }

    fetch('/agregar-comentario-blog', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            comentario: commentText
        })
    })
    .then(response => {
        if (response.status === 401) {
            showLoginMessage();
            return;
        }
        if (!response.ok) {
            throw new Error('Error al enviar comentario');
        }
        return response.json();
    })
    .then(data => {
        if (data && data.success) {
            document.getElementById('commentText').value = '';
            loadComments();
            Swal.fire({
                icon: 'success',
                title: '¡Excelente!',
                text: 'Comentario publicado exitosamente.',
                confirmButtonColor: '#4CAF50'
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Ocurrió un error al publicar el comentario.',
            confirmButtonColor: '#4CAF50'
        });
    });
}

// Función para mostrar mensaje de login
function showLoginMessage() {
    const commentForm = document.getElementById('commentForm');
    const loginMessage = document.getElementById('loginMessage');
    const textarea = document.getElementById('commentText');
    const button = document.querySelector('.btn-submit-comment');

    if (commentForm) {
        textarea.disabled = true;
        button.disabled = true;
        loginMessage.style.display = 'block';
    }
}

// Función para escapar HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Función para formatear fecha
function formatDate(dateString) {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
        return 'Hoy a las ' + date.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
    } else if (date.toDateString() === yesterday.toDateString()) {
        return 'Ayer a las ' + date.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
    } else {
        return date.toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' });
    }
}