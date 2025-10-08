import cv2 as cv
import numpy as np
import sys


def load_image(image_path):
    """Load an image from the specified path."""
    image = cv.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")
    return image


def focus_mask(image, focus_threshold=0.5):
    """
    Creates a mask that removes unfocused areas of the image.
    The mask will keep the areas that are focused based on a sharpness threshold.
    """
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    laplacian = cv.Laplacian(gray, cv.CV_64F)
    sharpness_map = np.abs(laplacian)
    norm_sharpness = cv.normalize(sharpness_map, None, 0, 1, cv.NORM_MINMAX)
    mask = (norm_sharpness > focus_threshold).astype(np.uint8) * 255
    mask = cv.GaussianBlur(mask, (11, 11), 0)
    mask = cv.threshold(mask, 127, 255, cv.THRESH_BINARY)[1]
    masked_image = cv.bitwise_and(image, image, mask=mask)
    return masked_image


def rezize_image_preserve_aspect_ratio(image, target_width=960):
    """Resize an image while preserving its aspect ratio."""
    height, width = image.shape[:2]
    aspect_ratio = width / height
    target_height = int(target_width / aspect_ratio)
    resized_image = cv.resize(
        image, (int(target_width), target_height), interpolation=cv.INTER_AREA
    )
    return resized_image


def grid_of_images(images, max_width=2560, max_height=1440, max_columns=5):
    image_width = images[0].shape[1]
    image_height = images[0].shape[0]

    cell_width = min(image_width, max_width // max_columns)
    cell_height = int(cell_width * (image_height / image_width))

    grid_of_images = np.zeros(
        (
            cell_height * ((len(images) + max_columns - 1) // max_columns),
            cell_width * max_columns,
            3,
        ),
        dtype=np.uint8,
    )

    for i, img in enumerate(images):
        row = i // max_columns
        col = i % max_columns
        resized_img = cv.resize(
            img, (cell_width, cell_height), interpolation=cv.INTER_AREA
        )
        grid_of_images[
            row * cell_height : (row + 1) * cell_height,
            col * cell_width : (col + 1) * cell_width,
        ] = resized_img
    return grid_of_images


def main():
    ## get the file path from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python subject_detection.py <image_path>")
        sys.exit(1)
    image_path = sys.argv[1]

    try:
        images = []

        original = rezize_image_preserve_aspect_ratio(load_image(image_path))
        images.append(original)

        start = 0.0
        end = 0.1
        steps = 20
        step_size = (end - start) / steps
        variable_name = "focus_threshold"
        for focus_threshold in np.arange(start, end, step_size):
            image = focus_mask(original, focus_threshold)

            ## draw the focus threshold on the top left corner
            cv.putText(
                image,
                f"Focus Threshold: {focus_threshold:.2f}",
                (10, 30),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 255),
                2,
            )
            images.append(image)

        grid = grid_of_images(images)
        ## save the grid image
        cv.imwrite(f"{image_path}_{variable_name}_{start}-{end}_{step_size}.png", grid)

        cv.imshow("Image Analysis", grid)
        cv.waitKey(0)  # Wait for a key press to close the window

    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
