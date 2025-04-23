import os
import sys
import subprocess
import time
import shutil
import cv2
import numpy as np
from PIL import ImageGrab

# Function to capture a screenshot
def capture_screenshot(save_path, index):
    img = ImageGrab.grab()
    filename = f"screenshot_{index:04}.png"
    img.save(os.path.join(save_path, filename))
    return filename

# Function to compare images using OpenCV
def are_images_similar(img1_path, img2_path, threshold=0.85):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1.shape != img2.shape:
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    non_zero_count = np.count_nonzero(gray)
    total_pixels = gray.size
    similarity = 1 - (non_zero_count / total_pixels)

    print(similarity, end=" ")
    return similarity >= threshold

# Function to identify and copy unique screenshots based on sequence comparison
"""
    similarity threshold determines how similar images are to marked as similar
        - higher means more similarity to be marked
        - lower means less similarity to be marked
"""
def identify_duplicates(folder, similarity_threshold=0.85):
    unique_folder = os.path.join(folder, "unique")
    os.makedirs(unique_folder, exist_ok=True)

    screenshots = [f for f in sorted(os.listdir(folder)) if f.endswith('.png')]

    if not screenshots:
        return unique_folder

    current_unique = os.path.join(folder, screenshots[0])
    shutil.copy(current_unique, os.path.join(unique_folder, screenshots[0]))

    for filename in screenshots[1:]:
        filepath = os.path.join(folder, filename)

        if not are_images_similar(filepath, current_unique, threshold=similarity_threshold):
            shutil.copy(filepath, os.path.join(unique_folder, filename))
            current_unique = filepath

    return unique_folder

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 screenshotter.py <interval_in_seconds> <starting_delay_in_seconds>")
        sys.exit(1)

    interval = int(sys.argv[1])
    delay = int(sys.argv[2])
    screenshot_folder = "screenshots"
    os.makedirs(screenshot_folder, exist_ok=True)

    print("Starting in...")
    while 0 <= delay:
        time.sleep(1)
        print(f"{delay}")
        delay -= 1

    print("\nStarting screenshot capture. Press Ctrl+C to stop.")
    index = 0
    try:
        while True:
            capture_screenshot(screenshot_folder, index)
            index += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nScreenshot capture stopped.")

    print("Identifying unique screenshots...")
    unique_folder = identify_duplicates(screenshot_folder)
    print(f"Unique screenshots saved in: {unique_folder}")

    print("Now processing screenshots...")
    subprocess.run(["python3", "music_processor.py"])
    print("""Music processed. Ready to construct sheets.
    Check that the first and last processed images are correct then run
    python3 construct_pages.py <music_name>
    """)


if __name__ == "__main__":
    main()
