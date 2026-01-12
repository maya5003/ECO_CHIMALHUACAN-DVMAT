const form = document.getElementById("formComentarios");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Recopilar todos los inputs del formulario
    const correoElectronico = document.getElementById("correoElectronico").value.trim();
    
    // Validar que el correo no esté vacío
    if (!correoElectronico) {
        showErrorAlert("Error, el correo electrónico es requerido");
        return;
    }

    // Validar formato de correo
    const emailValido = /\S+@\S+\.\S+/.test(correoElectronico);
    if (!emailValido) {
        showErrorAlert("Error, correo electrónico inválido");
        return;
    }

    // Recopilar todos los campos del formulario dinámicamente
    const inputs = form.querySelectorAll("input[type='text']");
    const comentarios = {};
    let camposVacios = false;

    inputs.forEach(input => {
        const valor = input.value.trim();
        if (!valor) {
            camposVacios = true;
        }
        comentarios[input.id] = valor;
    });

    // Incluir calificación si existe
    const calificacion = document.querySelector("input[name='Calificacion']:checked");
    if (calificacion) {
        comentarios['Calificacion'] = calificacion.value;
    }

    if (camposVacios) {
        showErrorAlert("Error, todos los campos son requeridos");
        return;
    }

    // Enviar comentario al servidor
    try {
        const respuesta = await fetch("/enviar-comentario", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                correoElectronico: correoElectronico,
                comentarios: comentarios 
            }),
        });

        const data = await respuesta.json();

        if (data.error) {
            showErrorAlert(data.error);
            return;
        }

        showSuccessAlert("Comentario enviado exitosamente");
        
        // Limpiar el formulario
        form.reset();

    } catch (error) {
        console.error("Error:", error);
        showErrorAlert("Error al enviar el comentario");
    }
});
