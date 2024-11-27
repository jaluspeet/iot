import cv2
import numpy as np
from typing import Tuple

MAX_TEMP: int = 6500
MIN_TEMP: int = 2000


def calculate_brightness(frame: np.ndarray) -> float:
    """
    Calculate the average brightness of a frame.
    :param frame: frame (BGR format).
    :return: average brightness.
    """
    gray: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return float(np.mean(gray))


def calculate_color_temperature(frame: np.ndarray) -> float:
    """
    Calculate the color temperature of a frame (Kelvin).
    :param frame: frame (BGR format).
    :return: color temperature (Kelvin).
    """
    frame_rgb: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    avg_r: float = float(np.mean(frame_rgb[:, :, 0]))
    avg_g: float = float(np.mean(frame_rgb[:, :, 1]))
    avg_b: float = float(np.mean(frame_rgb[:, :, 2]))

    # Normalize
    r_norm: float = avg_r / (avg_r + avg_g + avg_b)
    g_norm: float = avg_g / (avg_r + avg_g + avg_b)
    b_norm: float = avg_b / (avg_r + avg_g + avg_b)

    # Chromaticity coordinates
    x: float = 0.4124 * r_norm + 0.3576 * g_norm + 0.1805 * b_norm
    y: float = 0.2126 * r_norm + 0.7152 * g_norm + 0.0722 * b_norm

    # CCT to Kelvin
    n: float = (x - 0.3320) / (0.1858 - y)
    cct: float = 449 * n**3 + 3525 * n**2 + 6823.3 * n + 5520.33

    return cct


def map_compensation_color(brightness: float, temperature: float) -> Tuple[int, int, int]:
    """
    Calculate the compensating RGB color for given brightness and temperature.
    :param brightness: brightness.
    :param temperature: temperature (Kelvin).
    :return: compensating color Tuple(R,G,B).
    """
    # Invert brightness
    brightness_factor: float = np.clip(1.2 - (brightness / 255), 0.2, 1.0)

    # Invert temperature
    temperature = np.clip(temperature, MIN_TEMP, MAX_TEMP)
    red: int = int(np.interp(temperature, [MIN_TEMP, MAX_TEMP], [50, 255]))
    blue: int = int(np.interp(temperature, [MIN_TEMP, MAX_TEMP], [255, 50]))
    green: int = int((red + blue) / 3)

    # Scale by inverted brightness
    red = int(red * brightness_factor)
    green = int(green * brightness_factor)
    blue = int(blue * brightness_factor)

    return (blue, green, red)


def disable_auto_processing(cap: cv2.VideoCapture) -> None:
    """
    Disable auto-exposure, auto-white balance, and other automatic camera processing.
    :param cap: OpenCV VideoCapture object.
    """
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    cap.set(cv2.CAP_PROP_EXPOSURE, -4)
    cap.set(cv2.CAP_PROP_GAIN, 0)


def main() -> None:
    # Select source
    cap: cv2.VideoCapture = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return

    # Disable auto-processing features
    disable_auto_processing(cap)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture an image.")
            break

        brightness: float = calculate_brightness(frame)
        temp: float = calculate_color_temperature(frame)
        lamp: Tuple[int, int, int] = map_compensation_color(brightness, temp)

        # Fake lamp
        color_frame: np.ndarray = np.zeros((200, 400, 3), dtype=np.uint8)
        color_frame[:] = lamp

        # Show webcam feed and fake lamp
        cv2.imshow("Webcam Feed", frame)
        cv2.imshow("Compensating Solid Color", color_frame)

        # Log
        print(f"BRT: {brightness:.2f}, TMP: {temp:.2f}K, LMP: {lamp}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
