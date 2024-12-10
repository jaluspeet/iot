from __future__ import annotations
import cv2
import json
import paho.mqtt.client as mqtt
import numpy as np

BROKER = "localhost"
TOPIC = "paso"
PORT = 1883

# COLOR
class Color:
    def __init__(self, r: float, g: float, b: float, normalize=False) -> None:
        self.r = r / 255.0 if normalize else r
        self.g = g / 255.0 if normalize else g
        self.b = b / 255.0 if normalize else b

    def __str__(self) -> str:
        r_hex: str = f"{int(self.r * 255):02X}"
        g_hex: str = f"{int(self.g * 255):02X}"
        b_hex: str = f"{int(self.b * 255):02X}"
        return f"#{r_hex}{g_hex}{b_hex}"

    def reverse(self, normalize: bool = False) -> Color:
        return Color(1.0 - self.r, 1.0 - self.g, 1.0 - self.b, normalize)

    @staticmethod
    def from_frame(frame: np.ndarray, normalize: bool = True) -> Color:
        avg_b: float = np.mean(frame[:, :, 0])
        avg_g: float = np.mean(frame[:, :, 1])
        avg_r: float = np.mean(frame[:, :, 2])
        return Color(avg_r, avg_g, avg_b, normalize)

    @staticmethod
    def mix_colors(color1: Color, color2: Color, normalize: bool = False) -> Color:
        mixed_r = min(1.0, color1.r + color2.r)
        mixed_g = min(1.0, color1.g + color2.g)
        mixed_b = min(1.0, color1.b + color2.b)
        return Color(mixed_r, mixed_g, mixed_b, normalize)


# CAMERA
class Camera:
    def __init__(self, cap: cv2.VideoCapture, auto_processing: bool = False) -> None:
        self.cap = cap
        if not auto_processing:
            self.disable_auto_processing()

    def disable_auto_processing(self) -> None:
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, -4)
        self.cap.set(cv2.CAP_PROP_GAIN, 0)

    def get_frame(self) -> np.ndarray:
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame from the webcam.")
        return frame


# LAMP
class Lamp:
    def __init__(self, name, height, width) -> None:
        self.height = height
        self.width = width
        self.name = name

    def turn_on(self) -> None:
        self.window: np.ndarray = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        cv2.imshow(self.name, self.window)

    def turn_off(self) -> None:
        cv2.destroyWindow(self.name)

    def set_color(self, color: Color) -> None:
        self.window[:] = (
            int(color.b * 255),
            int(color.g * 255),
            int(color.r * 255),
        )
        cv2.imshow(self.name, self.window)

    @staticmethod
    def decide_lamp_color(settings: dict, room_color: Color) -> Color:
        mode = settings.get("mode", "manual")
        temperature = settings.get("temperature", 127.5)
        brightness = settings.get("brightness", 255)

        red = temperature / 255.0
        blue = 1.0 - red

        green = 0.3 + (temperature / 255.0) * 0.4

        red *= brightness / 255.0
        green *= brightness / 255.0
        blue *= brightness / 255.0

        target_color = Color(red, green, blue, normalize=False)

        if mode == "manual":
            return target_color

        elif mode == "automatic":
            offset_r = target_color.r - room_color.r
            offset_g = target_color.g - room_color.g
            offset_b = target_color.b - room_color.b

            comp_r = min(1.0, max(0.0, room_color.r + offset_r))
            comp_g = min(1.0, max(0.0, room_color.g + offset_g))
            comp_b = min(1.0, max(0.0, room_color.b + offset_b))

            return Color(comp_r, comp_g, comp_b, normalize=False)

        else:
            raise ValueError(f"Unknown mode: {mode}")


# CLIENT
class MQTTClient:
    def __init__(self, broker: str = BROKER, port: int = PORT, topic: str = TOPIC) -> None:
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.inbox: dict = None

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc) -> None:
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg) -> None:
        try:
            self.inbox: dict = json.loads(msg.payload.decode('utf-8').replace("'", '"'))
            print(self.inbox)
        except json.JSONDecodeError:
            print("Error decoding MQTT message payload.")

    def start(self) -> None:
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()


if __name__ == "__main__":

    try:
        # CLIENT - setup
        client = MQTTClient(BROKER, PORT, TOPIC)
        client.start()

        # CAMERA - setup
        camera: Camera = Camera(cv2.VideoCapture(0))
        if not camera.cap.isOpened():
            raise RuntimeError("Webcam not found.")

        # LAMP - setup
        lamp1: Lamp = Lamp("lampada1", 200, 400)
        lamp1.turn_on()

        # MAIN LOOP
        while True:
            frame: np.ndarray = camera.get_frame()
            frame_color: Color = Color.from_frame(frame)

            if client.inbox:
                lamp_color: Color = Lamp.decide_lamp_color(client.inbox, frame_color)
                print(f"LAMP:\t{lamp_color}\tROOM:\t{frame_color}")
                lamp1.set_color(lamp_color)

    except RuntimeError as init_error:
        print(f"INIT ERROR: {init_error}")

    finally:
        camera.cap.release()
        client.stop()
