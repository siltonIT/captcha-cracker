from PIL import Image
import pytesseract

def recognize_text(image, psm=6):
    """Recognizes text from an image using OCR with configurable parameters.

    Processes the input image using Tesseract OCR with:
    - Custom character whitelist (alphanumeric only)
    - Configurable page segmentation mode
    - Optimal OCR engine mode

    Args:
        image: Input image as numpy array
        psm: Page segmentation mode for Tesseract (default: 6)

    Returns:
        str: Recognized text with whitespace stripped

    Example:
        >>> recognized = recognize_text(image_array, psm=10)
        'ABC123'
    """
    # Convert numpy array to PIL Image
    pil_image = Image.fromarray(image)
    
    # Character whitelist: only a-z, A-Z, 0-9
    whitelist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    # Tesseract configuration
    custom_config = f'--oem 3 --psm {psm} -c tessedit_char_whitelist={whitelist}'
    
    # Perform text recognition
    text = pytesseract.image_to_string(pil_image, config=custom_config)
    return text.strip()
