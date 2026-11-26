import os
import cv2
import numpy as np

# Arrow key codes returned by cv2.waitKeyEx() across Windows, macOS, and Linux
UP_ARROW_KEYS = {2490368, 65362, 63232}
DOWN_ARROW_KEYS = {2621440, 65364, 63233}


def apply_color_filter(image, filter_type, intensity=30):
    """Apply a color tint or channel intensity adjustment to the given image."""
    filtered_image = image.copy()

    # OpenCV uses BGR channel order: 0 = Blue, 1 = Green, 2 = Red
    if filter_type == "red_tint":
        filtered_image[:, :, 0] = 0  # Blue to 0
        filtered_image[:, :, 1] = 0  # Green to 0
    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0  # Blue to 0
        filtered_image[:, :, 2] = 0  # Red to 0
    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0  # Green to 0
        filtered_image[:, :, 2] = 0  # Red to 0
    elif filter_type == "increase_red":
        filtered_image[:, :, 2] = cv2.add(filtered_image[:, :, 2], intensity)
    elif filter_type == "decrease_red":
        filtered_image[:, :, 2] = cv2.subtract(filtered_image[:, :, 2], intensity)
    elif filter_type == "increase_green":
        filtered_image[:, :, 1] = cv2.add(filtered_image[:, :, 1], intensity)
    elif filter_type == "decrease_blue":
        filtered_image[:, :, 0] = cv2.subtract(filtered_image[:, :, 0], intensity)

    return filtered_image


def save_image(image, images_dir):
    """Prompt for a custom filename, sanitize invalid characters, and save to images/."""
    raw_name = input("Enter a custom filename (without extension): ").strip()
    sanitized_name = "".join(
        c for c in raw_name if c.isalnum() or c in ("_", "-")
    )

    if not sanitized_name:
        sanitized_name = "filtered_image"

    os.makedirs(images_dir, exist_ok=True)
    output_path = os.path.join(images_dir, f"{sanitized_name}.png")
    cv2.imwrite(output_path, image)
    print(f"Saved modified image to '{output_path}'.")


def interactive_color_filter(image_path, images_dir):
    """Run the real-time interactive color filter and channel adjustment loop."""
    original_image = cv2.imread(image_path)
    if original_image is None:
        print(f"Error: Could not load image at '{image_path}'.")
        return

    current_image = original_image.copy()
    window_name = "Real-Time Color Filter Application"

    print("Controls (click the image window first):")
    print("  'r'          - Apply Red Tint")
    print("  'g'          - Apply Green Tint")
    print("  'b'          - Apply Blue Tint")
    print("  'i'          - Increase Red Intensity")
    print("  'd'          - Decrease Blue Intensity")
    print("  'Up Arrow'   - Increase Green Intensity")
    print("  'Down Arrow' - Decrease Red Intensity")
    print("  'o'          - Reset to Original Image")
    print("  's'          - Save Current Image")
    print("  'q'          - Quit")

    while True:
        cv2.imshow(window_name, current_image)
        key = cv2.waitKeyEx(0)

        # Extract standard ASCII code if a normal character key was pressed
        char_key = key & 0xFF if key != -1 else -1

        if char_key == ord("r"):
            current_image = apply_color_filter(current_image, "red_tint")
            print("Applied: Red Tint")
        elif char_key == ord("g"):
            current_image = apply_color_filter(current_image, "green_tint")
            print("Applied: Green Tint")
        elif char_key == ord("b"):
            current_image = apply_color_filter(current_image)