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
    sendMessage("iot/from_ui", { mode: "manual" }); // Invio del messaggio via MQTT
};

// Funzione per attivare la modalità automatica
const enableAutoMode = () => {
    manualLumos.disabled = true;
    manualTemp.disabled = true;
    autoLumos.disabled = false;
    autoTemp.disabled = false;
    sendMessage("iot/from_ui", { mode: "auto" }); // Invio del messaggio via MQTT
};

// Event listener per la checkbox "Manuale"
manualCheck.addEventListener('change', () => {
    if (manualCheck.checked) {
        autoCheck.checked = false; // Deseleziona "Automatica" se "Manuale" è selezionata
        enableManualMode();
    } else {
        manualLumos.disabled = true;
        manualTemp.disabled = true;
        sendMessage("iot/from_ui", { mode: "auto" }); // invio quando deselezioni
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
        sendMessage("iot/from_ui", { mode: "manual" }); // invio quando deselezioni
    }
});

// Funzione per inviare messaggi MQTT
const sendMessage = (topic, payload) => {
    const message = new Paho.MQTT.Message(JSON.stringify(payload));
    message.destinationName = topic;
    client.send(message);
    console.log("Messaggio inviato:", payload);
};

//--------------------------------------Parte di comunicazione

// MQTT Configurazione
const clientId = "web_client_" + Math.floor(Math.random() * 1000); // ID unico per il client
const client = new Paho.MQTT.Client("localhost", 9001, clientId); // Cambia 'localhost' con l'IP del Raspberry Pi

// Eventi MQTT
client.onConnectionLost = (responseObject) => {
    console.error("Connessione persa: " + responseObject.errorMessage);
};
client.onMessageArrived = (message) => {
    console.log("Messaggio ricevuto: " + message.payloadString);

    // Aggiorna interfaccia web con i dati ricevuti
    const data = JSON.parse(message.payloadString);
    if (data.average_color) {
        const { r, g, b } = data.average_color;
        document.body.style.backgroundColor = `rgb(${r}, ${g}, ${b})`; // Cambia colore sfondo
    }
};

// Connetti al broker
client.connect({
    onSuccess: () => {
        console.log("Connesso al broker MQTT");
        client.subscribe("iot/to_ui"); // Topic per ricevere i dati dal Raspberry
    },
});

// Event listener per il controllo manuale
document.getElementById("manualLumos").addEventListener("input", (e) => {
    const brightness = e.target.value;
    sendMessage("iot/from_ui", { brightness });
});

document.getElementById("manualTemp").addEventListener("input", (e) => {
    const temperature = e.target.value;
    sendMessage("iot/from_ui", { temperature });
});

document.getElementById("autoLumos").addEventListener("input", (e) => {
    const brightness = e.target.value;
    sendMessage("iot/from_ui", { auto_brightness: brightness });
});

document.getElementById("autoTemp").addEventListener("input", (e) => {
    const temperature = e.target.value;
    sendMessage("iot/from_ui", { auto_temperature: temperature });
});
