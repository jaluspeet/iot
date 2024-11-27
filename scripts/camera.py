import cv2
import numpy as np
from typing import Tuple


def calculate_average_color(frame: np.ndarray) -> Tuple[float, float, float]:
    avg_b: float = np.mean(frame[:, :, 0])
    avg_g: float = np.mean(frame[:, :, 1])
    avg_r: float = np.mean(frame[:, :, 2])
    return avg_b, avg_g, avg_r


def map_compensation_color(avg_color: Tuple[float, float, float]) -> Tuple[int, int, int]:
    norm_color = [c / 255.0 for c in avg_color]
    comp_color = [1.0 - c for c in norm_color]
    return tuple(int(c * 255) for c in comp_color)


def mix_colors(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> Tuple[int, int, int]:
    norm1 = [c / 255.0 for c in color1]
    norm2 = [c / 255.0 for c in color2]
    mixed = [min(1.0, norm1[i] + norm2[i]) for i in range(3)]
    return tuple(int(c * 255) for c in mixed)


def disable_auto_processing(cap: cv2.VideoCapture) -> None:
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    cap.set(cv2.CAP_PROP_EXPOSURE, -4)
    cap.set(cv2.CAP_PROP_GAIN, 0)


def main() -> None:
    try:
        cap: cv2.VideoCapture = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise RuntimeError("Error: Webcam not found.")

        disable_auto_processing(cap)

        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    raise RuntimeError("Error: Frame not captured.")

                avg_color: Tuple[float, float, float] = calculate_average_color(frame)
                
                room_color = avg_color
                lamp_color: Tuple[int, int, int] = map_compensation_color(avg_color)
                combined_color: Tuple[int, int, int] = mix_colors(room_color, lamp_color)

                room_frame: np.ndarray = np.zeros((200, 400, 3), dtype=np.uint8)
                room_frame[:] = room_color
                lamp_frame: np.ndarray = np.zeros((200, 400, 3), dtype=np.uint8)
                lamp_frame[:] = lamp_color
                combined_frame: np.ndarray = np.zeros((200, 400, 3), dtype=np.uint8)
                combined_frame[:] = combined_color

                cv2.imshow("webcam", frame)
                cv2.imshow("room", room_frame)
                cv2.imshow("lamp", lamp_frame)
                cv2.imshow("combined", combined_frame)

                print(f"ROOM:\t({round(avg_color[0])},{round(avg_color[1])},{round(avg_color[2])})\tLAMP:\t({round(lamp_color[0])},{round(lamp_color[1])},{round(lamp_color[2])})\tCOMBINED:\t{combined_color}")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except RuntimeError as frame_error:
                print(f"Frame Capture/Processing Error: {frame_error}")
                break
    except RuntimeError as init_error:
        print(f"Initialization Error: {init_error}")
    finally:
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

