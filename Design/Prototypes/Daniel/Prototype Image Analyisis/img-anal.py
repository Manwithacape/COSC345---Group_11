import sys
import cv2 as cv
import numpy as np


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


def detect_sharpness(image):
    """Detect the sharpness of an image as a proportion between 0 (blurry) and 1 (sharp)."""
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    laplacian_var = cv.Laplacian(gray_image, cv.CV_64F).var()
    # Define reasonable min and max values for normalization
    min_var = 10  # typical value for very blurry images
    max_var = 1000  # typical value for very sharp images
    sharpness = (laplacian_var - min_var) / (max_var - min_var)
    sharpness = max(0.0, min(1.0, sharpness))  # Clamp between 0 and 1
    return sharpness


def detect_exposure(image):
    """
    Detect the exposure of an image as a proportion:
    1 = well-exposed (not too dark or too bright),
    0 = underexposed or overexposed.
    """
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    mean_intensity = np.mean(gray_image)
    # Assume ideal exposure is around mid-gray (127.5)
    # The further from 127.5, the worse the exposure
    exposure = 1.0 - (abs(mean_intensity - 127.5) / 127.5)
    exposure = max(0.0, min(1.0, exposure))  # Clamp between 0 and 1
    return exposure


def detect_saturation(image):
    """Detect the saturation of an image as a proportion: 0 (grayscale), 1 (fully saturated)."""
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    saturation_channel = hsv_image[:, :, 1]
    mean_saturation = np.mean(saturation_channel)
    # Normalize mean saturation (0 = grayscale, 255 = fully saturated)
    saturation = mean_saturation / 255.0
    saturation = max(0.0, min(1.0, saturation))  # Clamp between 0 and 1
    return saturation


def detect_contrast(image):
    """Detect the contrast of an image as a proportion: 0 (low contrast), 1 (high contrast)."""
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    min_val, max_val = np.min(gray_image), np.max(gray_image)
    contrast = (max_val - min_val) / 255.0
    contrast = max(0.0, min(1.0, contrast))  # Clamp between 0 and 1
    return contrast


def detect_dominant_color(image):
    """Detect the dominant color of an image."""
    # Convert the image to the HSV color space
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    # Calculate the histogram for the hue channel
    hist = cv.calcHist([hsv_image], [0], None, [180], [0, 180])
    # Find the index of the maximum value in the histogram
    dominant_hue_index = np.argmax(hist)
    # Convert the hue index to a color in BGR format
    dominant_color = cv.cvtColor(
        np.uint8([[[dominant_hue_index, 255, 255]]]), cv.COLOR_HSV2BGR
    )[0][0]
    return dominant_color


def load_image(image_path):
    """Load an image from the specified path."""
    image = cv.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")
    return image


def display_image(image, window_name="Image"):
    """Display an image in a window."""
    cv.imshow(window_name, image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def main():
    ## use arguments to specify the image path
    if len(sys.argv) < 2:
        print("Usage: python img-anal.py <image_path>")
        return

    image_path = sys.argv[1]
    try:
        ## Where we will draw the results in a grid
        result_image = cv.Mat()

        image = load_image(image_path)
        image = rezize_image_preserve_aspect_ratio(image)

        # Resize the image while preserving aspect ratio

        # Apply focus mask to the image
        for focus_threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
            image_masked = focus_mask(image, focus_threshold)
            cv.imshow(
                f"Masked Image (Focus Threshold: {focus_threshold})", image_masked
            )
        image_masked = focus_mask(image)
        cv.waitKey(0)  # Wait for a key press to close the windows

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
