document.addEventListener("DOMContentLoaded", () => {
    console.log("Loaded");
});

// Script per abilitare/disabilitare gli slider
const lumosSlider = document.getElementById('lumos');
const temperatureSlider = document.getElementById('temperature');
const checkLumos = document.getElementById('checkLumos');
const checkTemperature = document.getElementById('checkTemperature');

// Funzione per resettare il valore dello slider e disabilitarlo
const toggleSlider = (checkbox, slider) => {
    if (checkbox.checked) {
        slider.disabled = false;
    } else {
        slider.disabled = true;
        slider.value = 50; // Valore di default centrale
    }
};

// Event listener per Luminosità
checkLumos.addEventListener('change', () => toggleSlider(checkLumos, lumosSlider));

// Event listener per Temperatura
checkTemperature.addEventListener('change', () => toggleSlider(checkTemperature, temperatureSlider));