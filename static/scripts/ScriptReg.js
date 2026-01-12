const form = document.getElementById("formRegistro");
const historialLista = document.getElementById("listaHistorial");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const correo = document.getElementById("correo").value.trim();
    const usuario = document.getElementById("usuario").value.trim();
    const password = document.getElementById("password").value;

    const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
    if (!passwordRegex.test(password)) {
        Swal.fire({
            icon: "error",
            title: "Contraseña inválida",
            text: "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número."
        });
        return;
    }

    if (!correo || !usuario || !password) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Error, correo electronico o usuario invalido"
        });
        return;
    }

    if (!correo.includes("@")) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Error, correo electronico o usuario invalido"
        });
        return;
    }

    const emailValido = /\S+@\S+\.\S+/.test(correo);
    if (!emailValido) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Error, correo electronico o usuario invalido"
        });
        return;
    }

    const respuesta = await fetch("/registrar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, usuario, password }),
    });

    const data = await respuesta.json();

    if (data.error) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Error, correo electronico o usuario invalido"
        });
        return;
    }

    Swal.fire({
        icon: "success",
        title: "Registro completado",
        timer: 1500,
        showConfirmButton: false
    });

    // Redirigir después del registro
    setTimeout(() => {
        window.location.href = "/";
    }, 1500);

    actualizarHistorial(data.historial);
});

function actualizarHistorial(historial) {
    if (!historialLista) return; 
    historialLista.innerHTML = "";
    historial.forEach((r) => {
        let li = document.createElement("li");
        li.textContent = `${r.correo} — ${r.password}`;
        historialLista.appendChild(li);
    });
}

function mostrarHistorial() {
    const contenido = historialLista ? historialLista.innerHTML : "";
    Swal.fire({
        title: "Historial",
        html: contenido || "<i>No hay registros todavía</i>",
        width: 400
    });
}
