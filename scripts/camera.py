import cv2
import numpy as np


def main():
    # Open a connection to the webcam
    # Use 0 for the default camera, or change it to the index of your camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return

    print("Press 'q' to quit the application.")

    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture an image.")
            break

        # Convert the frame to a NumPy array (pixel values)
        pixel_values = np.array(frame)

        # Show the captured frame in a window
        cv2.imshow("Webcam Feed", frame)

        # Print the pixel values of the center of the frame as an example
        h, w, _ = frame.shape
        center_pixel = pixel_values[h // 2, w // 2]
        print(f"Center pixel values (BGR): {center_pixel}")

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
