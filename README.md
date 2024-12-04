# Lumo Pasos  

Lumo Pasos è un'applicazione per la gestione dell'illuminazione ambientale che consente di regolare luminosità e temperatura attraverso modalità manuali e automatiche.  

## Funzionalità Principali  

### 1. Modalità Manuale  
La modalità manuale consente all'utente di regolare i parametri tramite un'interfaccia web:  
- **Luminosità:** Regolabile con uno slider per scegliere l'intensità desiderata.  
- **Temperatura:** Slider per regolare la tonalità calda o fredda della luce.  

### 2. Modalità Automatica  
La modalità automatica sfrutta una webcam per calibrare in tempo reale luminosità e temperatura:  
- **Analisi ambientale:** La webcam cattura immagini per calcolare il colore medio dell'ambiente.  
- **Adattamento dinamico:** La luce viene regolata automaticamente per migliorare il comfort visivo.  

## Caratteristiche Tecniche  

### Server Web Flask  
- L'applicazione utilizza Flask per servire l'interfaccia web e gestire le richieste utente.  
- Comunicazione in tempo reale tra client e server per l'applicazione delle modifiche.  

### Analisi del Colore  
- Calcolo dei valori medi di rosso, verde e blu (RGB) tramite OpenCV.  
- Compensazione del colore con formule per creare un'illuminazione complementare.  

### Interfaccia Utente  
- **Modalità manuale:** Slider e input numerici per personalizzare luminosità e temperatura.  
- **Modalità automatica:** Regolazione automatica basata sui dati acquisiti dalla webcam.  
- **Color Picker:** Possibilità di scegliere un colore personalizzato per l'illuminazione.  

## Istruzioni per l'Uso  
### Modalità Manuale  
- Attivare il controllo manuale e usare gli slider per regolare luminosità e temperatura.  

### Modalità Automatica  
- Attivare il controllo automatico e lasciare che la webcam regoli i parametri.  

## Tecnologie Utilizzate  
- **Flask:** Framework per la gestione del server web.  
- **HTML5, CSS3, Bootstrap:** Per un'interfaccia moderna e responsiva.  
- **JavaScript:** Per l'interattività dell'interfaccia.  
- **OpenCV (Python):** Per l'elaborazione delle immagini catturate dalla webcam.  

## Autori  
Lumo Pasos è stato sviluppato da:  
- **Alessandro Dominici**  
- **Jacopo Spitaleri**  
- **Mactar Seck Ibrahima**  

