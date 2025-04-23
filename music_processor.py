import os
import cv2
import numpy as np

input_dir = "screenshots/unique"
output_dir = "screenshots/processed"
os.makedirs(output_dir, exist_ok=True)

def extract_music_area(input_path, output_path):
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = [cv2.boundingRect(c) for c in contours]

    if not bounding_boxes:
        print(f"No white area found in {input_path}")
        return

    # Use the largest white rectangle
    x, y, w, h = max(bounding_boxes, key=lambda b: b[2] * b[3])
    cropped = image[y:y+h, x:x+w]
    cv2.imwrite(output_path, cropped)

# Process all PNG images in the unique directory
for filename in sorted(os.listdir(input_dir)):
    if filename.lower().endswith(".png"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        extract_music_area(input_path, output_path)
        print(f"Processed {filename}")
