import cv2
import numpy as np
import paho.mqtt.client as mqtt
import json
from typing import Tuple

# MQTT Configurazione dei dati per il protocollo
BROKER_ADDRESS = "localhost"  # Cambia con l'IP del broker
BROKER_PORT = 1883
TOPIC_TO_UI = "iot/to_ui" #Parte riservata all'invio dei dati all'interfaccia
TOPIC_FROM_UI = "iot/from_ui" #Parte per il ricevimento e modifica dei dati

# MQTT Client setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connesso")
    client.subscribe(TOPIC_FROM_UI) #iscrizione per ricecevere i nuovi dati

def on_message(client, userdata, msg):
    print(f"Messaggi ricevuti: {msg.payload}")
    data = json.loads(msg.payload.decode())
    print(f"Dati ricevuti: {data}")

client.on_connect = on_connect
client.on_message = on_message

# Funzioni
def calculate_average_color(frame: np.ndarray) -> Tuple[float, float, float]:
    avg_b, avg_g, avg_r = np.mean(frame[:, :, 0]), np.mean(frame[:, :, 1]), np.mean(frame[:, :, 2])
    return avg_b, avg_g, avg_r

def main():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Webcam not found.")

        client.connect(BROKER_ADDRESS, BROKER_PORT)
        client.loop_start()

        while True:
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("Frame not captured.")

            avg_color = calculate_average_color(frame)
            data = {"average_color": {"r": avg_color[2], "g": avg_color[1], "b": avg_color[0]}}
            
            # Send data to the web interface
            client.publish(TOPIC_TO_UI, json.dumps(data))
            
            cv2.imshow("Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
