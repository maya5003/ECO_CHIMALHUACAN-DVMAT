document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.main-menu a');
    const contentDisplay = document.getElementById('content-display');

    // Contenido por sección (se usa para el popover; puede adaptarse).
    const content = {
        lecturas: `
            <ul>
                <li>"Introducción a la Ecología" — Dr. Carlos Rivas</li>
                <li>"Ecosistemas y sus componentes" — Mtra. Elena Martínez</li>
                <li>"El impacto Humano en el medio Ambiente" — Ing. Roberto García</li>
                <li>"Energías renovables y desarrollo sostenible" — Lic. Paula Jime</li>
            </ul>
        `,
        entrevistas: `
            <ul>
                <li>Educación ambiental — Dr. Ricardo Lopez</li>
                <li>Cuidado del planeta — Carlos Mendez</li>
                <li>Energías limpias — Sofia Ramirez</li>
                <li>Participación juvenil — Fernanda Cruz</li>
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
        `
    };

    // Popover
    const popover = document.createElement('div');
    popover.className = 'tooltip-popover';
    popover.style.display = 'none';
    document.body.appendChild(popover);

    function positionPopover(target) {
        const rect = target.getBoundingClientRect();
        popover.style.left = '0px';
        popover.style.top = '0px';
        popover.style.display = 'block';
        const popWidth = popover.offsetWidth;
        const popHeight = popover.offsetHeight;
        const margin = 8;
        let left = rect.left + window.scrollX;
        let top = rect.bottom + window.scrollY + margin;

        // Si se sale del borde derecho, empujar hacia la izquierda
        if (left + popWidth > window.innerWidth + window.scrollX) {
            left = window.innerWidth + window.scrollX - popWidth - margin;
        }
        // Si se sale por abajo de la ventana, mostrar encima del botón
        if (top + popHeight > window.innerHeight + window.scrollY) {
            top = rect.top + window.scrollY - popHeight - margin;
        }
        // Evitar salir a la izquierda
        if (left < window.scrollX + margin) left = window.scrollX + margin;

        popover.style.left = `${left}px`;
        popover.style.top = `${top}px`;
    }

    function showPopover(button) {
        const key = button.dataset.content;
        popover.innerHTML = `<div class="popover-title">${button.textContent}</div>${content[key] || '<p>No hay contenido.</p>'}`;
        popover.style.display = 'block';
        positionPopover(button);
        // Marcar atributo aria para accesibilidad
        button.setAttribute('aria-expanded', 'true');
    }

    function hidePopover(button) {
        popover.style.display = 'none';
        if (button) button.setAttribute('aria-expanded', 'false');
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