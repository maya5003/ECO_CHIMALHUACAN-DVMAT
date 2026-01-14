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
                const commentsList = document.getElementById('commentsList');
                commentsList.innerHTML = '<div class="no-comments-message">Inicia sesión para ver los comentarios publicados.</div>';
                return;
            }
            return response.json();
        })
        .then(comments => {
            if (comments) {
                displayComments(comments);
            }
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
        commentCard.setAttribute('data-comment-id', comment.id);
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
                <button class="reply-btn" data-comment-id="${comment.id}">Responder</button>
                <div class="reply-form" id="reply-form-${comment.id}" style="display: none;">
                    <textarea class="reply-text" placeholder="Escribe tu respuesta..." rows="2"></textarea>
                    <button class="btn-submit-reply" data-comment-id="${comment.id}">Publicar Respuesta</button>
                    <button class="btn-cancel-reply" data-comment-id="${comment.id}">Cancelar</button>
                </div>
                <div class="replies-container" id="replies-${comment.id}">
                    <!-- Las respuestas se cargarán aquí -->
                </div>
            </div>
        `;
        commentsList.appendChild(commentCard);

        // Cargar respuestas para este comentario
        loadReplies(comment.id);
    });

    // Agregar event listeners para botones de respuesta
    document.querySelectorAll('.reply-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            toggleReplyForm(commentId);
        });
    });

    document.querySelectorAll('.btn-submit-reply').forEach(btn => {
        btn.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            submitReply(commentId);
        });
    });

    document.querySelectorAll('.btn-cancel-reply').forEach(btn => {
        btn.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            cancelReply(commentId);
        });
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

// Función para cargar respuestas
function loadReplies(commentId) {
    fetch(`/obtener-respuestas-blog/${commentId}`)
        .then(response => {
            if (response.status === 401) {
                return [];
            }
            return response.json();
        })
        .then(replies => {
            displayReplies(commentId, replies);
        })
        .catch(error => {
            console.error('Error al cargar respuestas:', error);
        });
}

// Función para mostrar respuestas
function displayReplies(commentId, replies) {
    const repliesContainer = document.getElementById(`replies-${commentId}`);
    repliesContainer.innerHTML = '';

    if (replies.length > 0) {
        replies.forEach(reply => {
            const replyCard = document.createElement('div');
            replyCard.className = 'reply-card';
            replyCard.innerHTML = `
                <div class="reply-avatar">
                    <img src="${reply.foto_perfil}" alt="${reply.nombre_usuario}">
                </div>
                <div class="reply-content">
                    <div class="reply-header">
                        <p class="reply-username">${escapeHtml(reply.nombre_usuario)}</p>
                        <span class="reply-date">${formatDate(reply.fecha)}</span>
                    </div>
                    <p class="reply-text">${escapeHtml(reply.respuesta)}</p>
                </div>
            `;
            repliesContainer.appendChild(replyCard);
        });
    }
}

// Función para mostrar/ocultar formulario de respuesta
function toggleReplyForm(commentId) {
    const form = document.getElementById(`reply-form-${commentId}`);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// Función para enviar respuesta
function submitReply(commentId) {
    const replyText = document.querySelector(`#reply-form-${commentId} .reply-text`).value;

    if (!replyText.trim()) {
        Swal.fire({
            icon: 'warning',
            title: 'Campo vacío',
            text: 'Por favor, escribe una respuesta.',
            confirmButtonColor: '#4CAF50'
        });
        return;
    }

    fetch('/agregar-respuesta-blog', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            comentario_id: commentId,
            respuesta: replyText
        })
    })
    .then(response => {
        if (response.status === 401) {
            showLoginMessage();
            return;
        }
        if (!response.ok) {
            throw new Error('Error al enviar respuesta');
        }
        return response.json();
    })
    .then(data => {
        if (data && data.success) {
            document.querySelector(`#reply-form-${commentId} .reply-text`).value = '';
            toggleReplyForm(commentId);
            loadReplies(commentId);
            Swal.fire({
                icon: 'success',
                title: '¡Excelente!',
                text: 'Respuesta publicada exitosamente.',
                confirmButtonColor: '#4CAF50'
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Ocurrió un error al publicar la respuesta.',
            confirmButtonColor: '#4CAF50'
        });
    });
}

// Función para cancelar respuesta
function cancelReply(commentId) {
    document.querySelector(`#reply-form-${commentId} .reply-text`).value = '';
    toggleReplyForm(commentId);
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