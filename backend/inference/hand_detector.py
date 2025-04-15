import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

mp_hands = mp.solutions.hands

def detect_and_crop_hand(pil_image: Image.Image) -> Image.Image:
    image = np.array(pil_image.convert("RGB"))
    image.flags.writeable = False

    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.3)
    results = hands.process(image)
    hands.close()

    if not results.multi_hand_landmarks:
        print("🛑 No hand detected.")
        # Save fallback image for visual check
        pil_image.save("debug_hand_detection__no_hand.jpg")
        return pil_image

    h, w, _ = image.shape
    landmarks = results.multi_hand_landmarks[0].landmark
    x_coords = [lm.x * w for lm in landmarks]
    y_coords = [lm.y * h for lm in landmarks]

    x_min, x_max = int(min(x_coords)), int(max(x_coords))
    y_min, y_max = int(min(y_coords)), int(max(y_coords))

    padding = 20
    x_min = max(x_min - padding, 0)
    y_min = max(y_min - padding, 0)
    x_max = min(x_max + padding, w)
    y_max = min(y_max + padding, h)

    # Draw bounding box on original image for debugging
    debug_image = image.copy()
    cv2.rectangle(debug_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    debug_pil = Image.fromarray(debug_image)
    debug_pil.save("debug_hand_detection__bbox.jpg")  # <-- Save visual box

    # Save cropped image
    cropped = image[y_min:y_max, x_min:x_max]
    cropped_pil = Image.fromarray(cropped)
    cropped_pil.save("debug_hand_detection__cropped.jpg")  # <-- Save cropped hand

    print("✂️ Cropped hand from image (and saved).")
    return cropped_pil
