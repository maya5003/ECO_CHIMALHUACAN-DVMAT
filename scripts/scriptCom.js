const form = document.getElementById("formRegistro");
const historialLista = document.getElementById("listaHistorial");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const correo = document.getElementById("correo").value.trim();
    const usuario = document.getElementById("usuario").value.trim();
    const password = document.getElementById("password").value;

    if (!correo || !usuario || !password) {
        showErrorAlert("Error, correo electrónico o usuario inválido");
        return;
    }

    if (!correo.includes("@")) {
        showErrorAlert("Error, correo electrónico o usuario inválido");
        return;
    }


    const emailValido = /\S+@\S+\.\S+/.test(correo);
    if (!emailValido) {
        showErrorAlert("Error, correo electrónico o usuario inválido");
        return;
    }

    const respuesta = await fetch("/registrar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, usuario, password }),
    });

    const data = await respuesta.json();

    if (data.error) {
        showErrorAlert("Error, correo electrónico o usuario inválido");
        return;
    }

    showSuccessAlert("Envío completado");

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
    showInfoAlert(contenido || "No hay registros todavía");
}
