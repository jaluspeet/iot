from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

BROKER = "iot_server"
TOPIC = "paso"
PORT = 1883
CLIENT_ID = 60


app = Flask(__name__)

mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER, PORT, CLIENT_ID)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    print(data)
    mqtt_client.publish(TOPIC, payload=str(data), qos=0, retain=False)
    message = jsonify({"status": "success", "message": "Dati ricevuti correttamente"})
    return message


if __name__ == '__main__':
    app.run(debug=True)
