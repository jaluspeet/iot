# Lumo Pasos  
---

## Funzionalità Principali  

### 1. Modalità Manuale  
La modalità manuale consente all'utente di regolare direttamente i parametri attraverso un'interfaccia:  
- **Luminosità:**  
  - Regolabile con un cursore che varia da valori minimi a massimi.  
  - Ideale per controllare l'intensità della luce in base alle preferenze.  
- **Temperatura:**  
  - Controllo tramite un cursore per impostare tonalità calde o fredde.  

---

### 2. Modalità Automatica  
La modalità automatica utilizza una webcam per calibrare la luminosità e la temperatura in base alle condizioni ambientali:  
- **Analisi in tempo reale:**  
  - L'app cattura immagini dalla webcam e calcola il colore medio dell'ambiente.  
- **Compensazione cromatica:**  
  - La luce della stanza viene regolata per bilanciare la luminosità e migliorare il comfort visivo.  

---

## Caratteristiche Tecniche  

### Analisi dell'Ambiente  
L'applicazione analizza il colore medio dell'ambiente attraverso una webcam:  
- I valori medi di blu, verde e rosso vengono calcolati con precisione.  
- Questi dati vengono utilizzati per creare un'illuminazione compensata che armonizza l'ambiente.

### Compensazione del Colore  
Il colore della luce emessa dalla lampada viene compensato per bilanciare i toni ambientali:  
- **Formula:** `1.0 - valore_normalizzato` per ottenere il colore complementare.  

### Interfaccia Utente  
L'app presenta un'interfaccia responsiva:  
- **Slider** per il controllo manuale.  
- **Input numerici** per impostare valori specifici nella modalità automatica.  
- **Color Picker** per scegliere il colore preferito della luce.  

---

## Istruzioni per l'Uso  

1. **Modalità Manuale:**  
   - Attiva il controllo manuale con il checkbox "Manuale".  
   - Usa gli slider per regolare luminosità e temperatura.  

2. **Modalità Automatica:**  
   - Attiva il controllo automatico con il checkbox "Automatica".  
   - Imposta i valori desiderati per luminosità e temperatura.  
   - La webcam si occuperà del resto 

3. **Color Picker:**  
   - Seleziona un colore personalizzato per la luce utilizzando l'apposito selettore.

---

## Tecnologie Utilizzate  

- **HTML5 e CSS3:** Per creare un'interfaccia utente moderna e responsiva.  
- **Bootstrap:** Per velocizzare lo sviluppo.  
- **Python (OpenCV):** Per la gestione della webcam e il calcolo del colore medio.  
- **JavaScript:** Per il controllo dinamico delle modalità e dell'interazione utente.  

---

## Autori  
Lumo Pasos è stato sviluppato da:  
- Alessandro Dominici  
- Jacopo Spitaleri  
- Mactar Seck Ibrahima  
