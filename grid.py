import cv2
import numpy as np

def add_grid_to_image(image_path, rows=5, cols=5, output_path=None):
    """
    Adds a grid to the given image and displays/saves it.

    Parameters:
    - image_path (str): Path to the input image.
    - rows (int): Number of rows in the grid.
    - cols (int): Number of columns in the grid.
    - output_path (str or None): Path to save the output image with grid. If None, the image will not be saved.
    """
    # Load the image
    image = cv2.imread(r"C:\Users\abhir\OneDrive\Desktop\WhatsApp Image 2024-12-28 at 21.15.40_5d1a07e2.jpg")

    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Calculate the size of each grid cell
    cell_height = height // rows
    cell_width = width // cols

    # Draw horizontal grid lines
    for i in range(1, rows):
        y = i * cell_height
        cv2.line(image, (0, y), (width, y), (0, 255, 0), 2)  # Green horizontal lines

    # Draw vertical grid lines
    for i in range(1, cols):
        x = i * cell_width
        cv2.line(image, (x, 0), (x, height), (0, 255, 0), 2)  # Green vertical lines

    # Display the image with grid
    cv2.imshow('Image with Grid', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Optionally, save the image with grid lines
    if output_path:
        cv2.imwrite(output_path, image)
        print(f"Image with grid saved at {output_path}")

# Example usage:
image_path = 'Desktop\WhatsApp Image 2024-12-28 at 21.15.40_5d1a07e2.jpg'  # Path to your input image
output_path = 'image_with_grid.jpg'  # Path to save the output image with grid

add_grid_to_image(image_path, rows=5, cols=5, output_path=output_path)
