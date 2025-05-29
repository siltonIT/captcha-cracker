import cv2
from config import CAPTCHA_DIR

def preprocess_image(image_path, session_id):
    """Preprocesses a CAPTCHA image for better OCR recognition.
    
    Processing steps:
    1. Loads the image
    2. Converts to grayscale
    3. Applies binary thresholding
    4. Enhances edges using Canny algorithm
    5. Combines binary and edge images
    6. Saves the processed image

    Args:
        image_path (str): Path to the original CAPTCHA image
        session_id (str): Unique session identifier for naming output file

    Returns:
        tuple: (processed_image, output_path) where:
            - processed_image: Preprocessed numpy array
            - output_path: Path to saved processed image

    Raises:
        Exception: If the input image cannot be loaded
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Failed to load image for preprocessing: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding to isolate text
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Enhance contours using edge detection
    edges = cv2.Canny(binary, 100, 200) 
    result = cv2.bitwise_or(binary, edges)

    # Save processed image
    processed_path = f"{CAPTCHA_DIR}/processed_{session_id}.png"
    cv2.imwrite(processed_path, result)

    return result, processed_path
