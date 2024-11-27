import cv2
import numpy as np
from typing import Tuple

MAX_TEMP: int = 6500
MIN_TEMP: int = 2000


def calculate_brightness(frame: np.ndarray) -> float:
    gray: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return float(np.mean(gray))


def calculate_color_temperature(frame: np.ndarray) -> float:
    frame_rgb: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    avg_r: float = float(np.mean(frame_rgb[:, :, 0]))
    avg_g: float = float(np.mean(frame_rgb[:, :, 1]))
    avg_b: float = float(np.mean(frame_rgb[:, :, 2]))

    # normalizza
    r_norm: float = avg_r / (avg_r + avg_g + avg_b)
    g_norm: float = avg_g / (avg_r + avg_g + avg_b)
    b_norm: float = avg_b / (avg_r + avg_g + avg_b)

    # coordinate cromaticità
    x: float = 0.4124 * r_norm + 0.3576 * g_norm + 0.1805 * b_norm
    y: float = 0.2126 * r_norm + 0.7152 * g_norm + 0.0722 * b_norm

    # CCT to Kelvin
    n: float = (x - 0.3320) / (0.1858 - y)
    cct: float = 449 * n**3 + 3525 * n**2 + 6823.3 * n + 5520.33

    return cct


def map_compensation_color(brightness: float, temperature: float) -> Tuple[int, int, int]:
    brightness_factor: float = np.clip(1.2 - (brightness / 255), 0.2, 1.0)
    temperature = np.clip(temperature, MIN_TEMP, MAX_TEMP)

    red: int = int(np.interp(temperature, [MIN_TEMP, MAX_TEMP], [50, 255]))
    blue: int = int(np.interp(temperature, [MIN_TEMP, MAX_TEMP], [255, 50]))
    green: int = int((red + blue) / 3)

    red = int(red * brightness_factor)
    green = int(green * brightness_factor)
    blue = int(blue * brightness_factor)

    return (blue, green, red)


def disable_auto_processing(cap: cv2.VideoCapture) -> None:
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    cap.set(cv2.CAP_PROP_EXPOSURE, -4)
    cap.set(cv2.CAP_PROP_GAIN, 0)


def main() -> None:
    try:
        cap: cv2.VideoCapture = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise RuntimeError("ERRORE: webcam non trovata.")

        disable_auto_processing(cap)

        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    raise RuntimeError("ERRORE: frame non catturato.")

                brightness: float = calculate_brightness(frame)
                temp: float = calculate_color_temperature(frame)
                lamp: Tuple[int, int, int] = map_compensation_color(
                    brightness, temp)

                color_frame: np.ndarray = np.zeros(
                    (200, 400, 3), dtype=np.uint8)
                color_frame[:] = lamp

                cv2.imshow("webcam", frame)
                cv2.imshow("lampada", color_frame)

                print(f"BRT: {brightness:.2f}, TMP: {temp:.2f}K, LMP: {lamp}")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except RuntimeError as frame_error:
                print(
                    f"ERRORE CATTURA FRAME/PROCESSING: {frame_error}")
                break
    except RuntimeError as init_error:
        print(f"ERRORE INIZIALIZIAZIONE: {init_error}")
    finally:
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
