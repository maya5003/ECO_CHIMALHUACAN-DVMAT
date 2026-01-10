// Funciones para mostrar alertas con SweetAlert

function showSuccessAlert(message) {
    Swal.fire({
        icon: "success",
        title: "Éxito",
        text: message,
        timer: 1500,
        showConfirmButton: false
    });
}

function showErrorAlert(message) {
    Swal.fire({
        icon: "error",
        title: "Error",
        text: message
    });
}

function showInfoAlert(message) {
    Swal.fire({
        icon: "info",
        title: "Información",
        text: message
    });
}