from utils.preprocess import preprocess_image
from utils.ocr import recognize_text
from session import get_session_id, download_captcha, verify_captcha
import logging
import os
from display import show_image

def main():
    """Automatically recognizes and verifies a CAPTCHA in a loop until successful.

    Process:
    1. Downloads the CAPTCHA image
    2. Preprocesses the image (binarization, enhancement)
    3. Recognizes text using OCR (PSM 10)
    4. Verifies the result with the server
    5. Repeats if unsuccessful

    Returns:
        str | None: Path to the CAPTCHA image if successful, otherwise None after all attempts.
    """
    random_image_path = None
    while True:
        try:
            # Get session ID and session object
            session_id, session = get_session_id()
            if session_id:
                # Download CAPTCHA image
                image_path = download_captcha(session_id, session)
            
                # Image preprocessing
                processed_image, processed_path = preprocess_image(image_path, session_id)
                logging.info(f"Processed image saved: {processed_path}")
            
                # Text recognition
                for psm in [10]:  # Using PSM 10 for single character recognition
                    recognized_text = recognize_text(processed_image, psm=psm)
                
                    # Limit to 6 characters
                    EXPECTED_LENGTH = 6
                    recognized_text = (recognized_text[:EXPECTED_LENGTH] + ' ' * EXPECTED_LENGTH)[:EXPECTED_LENGTH]
                    logging.info(f"Session ID: {session_id}, Recognized Text (PSM={psm}): {recognized_text}")
                
                    # Verify recognized text
                    if recognized_text and any(c.isalnum() for c in recognized_text):
                        success, random_image_path = verify_captcha(session_id, recognized_text, session)
                        if success:
                            break
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
        
        if random_image_path:
            break

        logging.error("Failed to recognize or verify CAPTCHA.")

    return random_image_path

if __name__ == "__main__":
    # Get the solved CAPTCHA image path
    image_path = main()
    
    if image_path and os.path.exists(image_path):
        try:
            # Display and then delete the CAPTCHA image
            show_image(image_path)
            os.remove(image_path)
        except Exception as e:
            print(f"Error processing image: {e}")
    else:
        print("CAPTCHA wasn't solved, no image was downloaded.")
