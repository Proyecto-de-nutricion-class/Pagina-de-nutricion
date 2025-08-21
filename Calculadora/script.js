document.addEventListener('DOMContentLoaded', function() {
    const calculateBtn = document.getElementById('calculate-btn');
    calculateBtn.addEventListener('click', calculateBMI);
});

function calculateBMI() {
    const height = parseFloat(document.getElementById('height').value) / 100;
    const weight = parseFloat(document.getElementById('weight').value);
    
    if (isNaN(height) || isNaN(weight) || height <= 0 || weight <= 0) {
        alert('Por favor ingresa valores válidos para altura y peso');
        return;
    }
    
    const bmi = weight / (height * height);
    const roundedBMI = bmi.toFixed(1);
    
    let category, info;
    if (bmi < 18.5) {
        category = 'Bajo peso';
        info = 'Tu peso es inferior al normal. Considera consultar una dieta para personas con bajo peso';
    } else if (bmi < 25) {
        category = 'Peso normal';
        info = '¡Felicidades! Tu peso está dentro del rango considerado normal.';
    } else if (bmi < 30) {
        category = 'Sobrepeso';
        info = 'Tienes sobrepeso. Considera aumentar tu actividad física y mejorar tu alimentación.';
    } else {
        category = 'Obesidad';
        info = 'Tu IMC indica obesidad. Es recomendable consultar las dietas para Gente con obesidad.';
    }
    
    document.getElementById('bmi-value').textContent = roundedBMI;
    document.getElementById('bmi-category').textContent = category;
    document.getElementById('bmi-info').textContent = info;
    
    const indicatorPosition = Math.min(bmi / 40 * 100, 100);
    document.getElementById('indicator').style.left = `${indicatorPosition}%`;
    
    document.getElementById('result').style.display = 'block';
}



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