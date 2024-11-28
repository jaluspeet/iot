document.addEventListener("DOMContentLoaded", () => { 
    console.log("Loaded");
});

// Elementi del DOM
const manualCheck = document.getElementById('manualCheck');
const autoCheck = document.getElementById('autoCheck');
const manualLumos = document.getElementById('manualLumos');
const manualTemp = document.getElementById('manualTemp');
const autoLumos = document.getElementById('autoLumos');
const autoTemp = document.getElementById('autoTemp');

// Funzione per attivare la modalità manuale
const enableManualMode = () => {
    manualLumos.disabled = false;
    manualTemp.disabled = false;
    autoLumos.disabled = true;
    autoTemp.disabled = true;
};

// Funzione per attivare la modalità automatica
const enableAutoMode = () => {
    manualLumos.disabled = true;
    manualTemp.disabled = true;
    autoLumos.disabled = false;
    autoTemp.disabled = false;
};

// Event listener per la checkbox "Manuale"
manualCheck.addEventListener('change', () => {
    if (manualCheck.checked) {
        autoCheck.checked = false; // Deseleziona "Automatica" se "Manuale" è selezionata
        enableManualMode();
    } else {
        manualLumos.disabled = true;
        manualTemp.disabled = true;
        
    }
});

// Event listener per la checkbox "Automatica"
autoCheck.addEventListener('change', () => {
    if (autoCheck.checked) {
        manualCheck.checked = false; // Deseleziona "Manuale" se "Automatica" è selezionata
        enableAutoMode();
    } else {
        autoLumos.disabled = true;
        autoTemp.disabled = true;
    }
});

const toggleSlider = (checkbox, slider) => {
    if (checkbox.checked) {
        slider.disabled = false;
    } else {
        slider.disabled = true;
        slider.value = 50; // Valore di default centrale
    }
};
