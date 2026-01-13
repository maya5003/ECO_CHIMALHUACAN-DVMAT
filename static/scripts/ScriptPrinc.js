document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.main-menu a, .user-profile-link');
    const contentDisplay = document.getElementById('content-display');

    let hideTimeout;

    // Contenido por sección (se usa para el popover; puede adaptarse).
    const content = {
        inicio: `
            <p> Regresa a la pagina de inicio </p>
        `,
        lecturas: `
            <ul>
                <li>"Ecologia y Educacion Ambiental"</li>
                <li>"Te Cuento mi Ambiente"</li>
                <li>"Medio Ambiente y Desarrollo"</li>
                <li>"Fundamentos De Ecologia y Ambiente"</li>
                <li>"El libro del reciclaje"</li>
            </ul>
        `,
        entrevistas: `
            <ul>
                <li>Contaminación de puebla — Dr. Ramón Ojeda Mestre</li>
                <li>Contaminación de la CDMX — Dr. Malaquías López</li>
                <li>Derecho al medio ambiente — Dr. Ramon Ojeda Mestre</li>
                <li>Que es la contingencia ambiental — Dr. Azándar Guzmán</li>
            </ul>
        `,
        videos: `
            <ul>
                <li>Que es la ecologia — Profe Sil</li>
                <li>¿Qué es la ecologia? — Bioasmobroso</li>
                <li>Fundamental Concepts of Ecology — BioScience</li>
                <li>What is Ecology? — Simply Science</li>
            </ul>
        `,
        juegos: `
            <ul>
                <li>Recicla y Gana</li>
                <li>ECOTrivia</li>
                <li>Aventura verde</li>
                <li>Guardianes del planeta</li>
            </ul>
        `,
        acciones: `
            <p> Descubre mas sobre DVMAT, el equipo detras del desarrollo de este sitio.</p>
        `,
        catalogo: `
            <p> Explora nuestro catalogo de materiales reciclables y aprende todo lo fundamental de ellos.</p>
        `,
        centros: `
            <p> Encuentra los centros de reciclaje mas cercanos a tu ubicacion y conoce sus horarios de atencion.</p>
        `,
        Perfil: `
            <p> Accede a tu perfil de usuario para ver y editar tu informacion personal.</p>
        `,
        manualidades: `
            <p> Aprende a crear manualidades ecologicas y sostenibles con nuestros instructivos paso a paso.</p>
        `
    };

    // Popover
    const popover = document.createElement('div');
    popover.className = 'tooltip-popover';
    popover.style.display = 'none';
    document.body.appendChild(popover);

    popover.addEventListener('mouseenter', () => clearTimeout(hideTimeout));
    popover.addEventListener('mouseleave', () => hidePopover(null));

    function positionPopover(target) {
        const rect = target.getBoundingClientRect();
        popover.style.left = '0px';
        popover.style.top = '0px';
        popover.style.display = 'block';
        const popWidth = popover.offsetWidth;
        const popHeight = popover.offsetHeight;
        const margin = 8;
        let left = rect.right + window.scrollX + margin; // Posicionar a la derecha del botón
        let top = rect.bottom + window.scrollY + margin;

        // Si no cabe a la derecha, posicionar a la izquierda
        if (left + popWidth > window.innerWidth + window.scrollX) {
            left = rect.left + window.scrollX - popWidth - margin;
        }
        // Si se sale por abajo de la ventana, mostrar encima del botón
        if (top + popHeight > window.innerHeight + window.scrollY) {
            top = rect.top + window.scrollY - popHeight - margin;
        }
        // Evitar salir a la izquierda
        if (left < window.scrollX + margin) left = window.scrollX + margin;

        // Extra margin for perfil-usuario
        if (target.classList.contains('user-profile-link')) {
            left += 200; // increased horizontal margin
            top += 150;  // increased vertical margin
        }

        popover.style.left = `${left}px`;
        popover.style.top = `${top}px`;
    }

    function showPopover(button) {
        clearTimeout(hideTimeout);
        const key = button.dataset.content;
        popover.innerHTML = `<div class="popover-title">${button.textContent}</div>${content[key] || '<p>No hay contenido.</p>'}`;
        popover.style.display = 'block';
        positionPopover(button);
        // Marcar atributo aria para accesibilidad
        button.setAttribute('aria-expanded', 'true');
        // Preparar elementos para efectos de visibilidad
        if (window.prepareObserveElements) {
            window.prepareObserveElements(popover);
        }
    }

    function hidePopover(button) {
        hideTimeout = setTimeout(() => {
            popover.style.display = 'none';
            if (button) button.setAttribute('aria-expanded', 'false');
        }, 150);
    }

    // eventos en los botones
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => showPopover(button));
        button.addEventListener('mouseleave', () => hidePopover(button));
        button.addEventListener('focus', () => showPopover(button));
        button.addEventListener('blur', () => hidePopover(button));

        // Touch para móviles: toggle en primer toque para mostrar, segundo toque deja seguir al href
        let touchShown = false;
        button.addEventListener('touchstart', (e) => {
            if (!touchShown) {
                // Mostrar la tooltip y evitar que el navegador siga el enlace en el primer toque
                e.preventDefault();
                showPopover(button);
                touchShown = true;
                // Al tocar fuera ocultamos
                const docClick = (ev) => {
                    if (!button.contains(ev.target) && !popover.contains(ev.target)) {
                        hidePopover(button);
                        touchShown = false;
                        document.removeEventListener('touchstart', docClick);
                    }
                };
                document.addEventListener('touchstart', docClick);
            } else {
                // Si ya estaba mostrado, permitimos la navegación con el siguiente toque
                touchShown = false;
            }
        });
    });

    // Ocultar popover en resize/scroll para mantenerlo en posición correcta
    window.addEventListener('resize', () => popover.style.display = 'none');
    window.addEventListener('scroll', () => popover.style.display = 'none');

    // Si quieres seguir mostrando detalles en la sección #content-display cuando no navegas,
    // puedes dejar extra lógica para rellenar contentDisplay en un click si detectas que el href es '#'.
});