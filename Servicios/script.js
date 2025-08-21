// Obtener elementos del DOM
const contactLink = document.getElementById('contactLink');
const contactModal = document.getElementById('contactModal');
const modalOverlay = document.getElementById('modalOverlay');

// Función para abrir el modal
function openModal(e) {
    e.preventDefault(); // Prevenir el comportamiento por defecto del enlace
    contactModal.style.display = 'block';
    modalOverlay.style.display = 'block';
}

// Función para cerrar el modal
function closeModal() {
    contactModal.style.display = 'none';
    modalOverlay.style.display = 'none';
}

// Evento click en el enlace de contacto
contactLink.addEventListener('click', openModal);

// Evento click en el overlay para cerrar el modal
modalOverlay.addEventListener('click', closeModal);

// Cerrar el modal si se hace clic fuera de él
window.addEventListener('click', function(event) {
    if (event.target === modalOverlay) {
        closeModal();
    }
});