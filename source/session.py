import requests
import logging
from config import CAPTCHA_DIR, BASE_URL, logging
import os

def get_session_id():
    """Retrieves session ID from server cookies.
    
    Returns:
        tuple: (session_id, session_object) if successful
        
    Raises:
        Exception: If session_id cookie not found or network error occurs
    """
    session = requests.Session()  # Create session to maintain cookies
    try:
        response = session.get(f"{BASE_URL}")  # Removed timeout
        if response.status_code == 200:
            # Extract session_id from cookies
            session_id = session.cookies.get("session_id")
            if not session_id:
                logging.error("session_id cookie not found in server response")
                raise Exception("session_id cookie not found in server response")
            logging.info(f"Retrieved session_id from cookies: {session_id}")
            return session_id, session
        else:
            logging.error(f"Error getting session_id: {response.status_code}, Response: {response.text[:500]}")
            raise Exception(f"Error getting session_id: {response.status_code}, Response: {response.text[:500]}")
    except requests.RequestException as e:
        logging.error(f"Network error while getting session_id: {str(e)}")
        raise Exception(f"Network error while getting session_id: {str(e)}")

def download_captcha(session_id, session):
    """Downloads CAPTCHA image for given session ID.
    
    Args:
        session_id: Current session identifier
        session: Active requests session
        
    Returns:
        str: Path to saved CAPTCHA image
        
    Raises:
        Exception: If download fails or HTTP error occurs
    """
    url = f"{BASE_URL}/captcha-image?session_id={session_id}"
    try:
        response = session.get(url, stream=True)  # Removed timeout
        response.raise_for_status()  # Raises HTTPError for bad responses
        filename = f"{CAPTCHA_DIR}/captcha_{session_id}.png"
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
        logging.info(f"CAPTCHA image saved as: {filename}")
        return filename
    except requests.RequestException as e:
        logging.error(f"Error downloading CAPTCHA from {url}: {str(e)}, Response: {getattr(e.response, 'text', 'No data')[:500]}")
        raise Exception(f"Error downloading CAPTCHA: {str(e)}")

def download_random_image(session_id, session):
    """Downloads random image after successful CAPTCHA verification.
    
    Args:
        session_id: Current session identifier
        session: Active requests session
        
    Returns:
        str: Path to saved random image or None if failed
    """
    url = f"{BASE_URL}/random-image?session_id={session_id}"
    try:
        response = session.get(url, stream=True)  # Removed timeout
        response.raise_for_status()
        filename = f"{CAPTCHA_DIR}/random_{session_id}.png"
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
        logging.info(f"Random image saved as: {filename}")
        return filename
    except requests.RequestException as e:
        logging.error(f"Error downloading random image from {url}: {str(e)}, Response: {getattr(e.response, 'text', 'No data')[:500]}")
        return None

def verify_captcha(session_id, captcha_text, session):
    """Verifies CAPTCHA solution with the server.
    
    Args:
        session_id: Current session identifier
        captcha_text: Recognized CAPTCHA text
        session: Active requests session
        
    Returns:
        tuple: (success_status, random_image_path)
        
    Raises:
        Exception: If verification fails or network error occurs
    """
    url = f"{BASE_URL}/captcha"  # Correct POST endpoint
    payload = {'captcha': captcha_text, 'attempts': '0'}  # Added attempts
    cookies = {'session_id': session_id}  # Pass session_id in cookies
    
    try:
        # Send request allowing redirects
        response = session.post(url, data=payload, 
                              headers={'Content-Type': 'application/x-www-form-urlencoded'}, 
                              cookies=cookies, 
                              allow_redirects=True)  # Removed timeout
        logging.info(f"Sent POST request: URL={url}, Payload={payload}, Cookies={cookies}")
        logging.info(f"Server response (raw): {response.text[:500]}")
        
        # Check final URL after redirects
        final_url = response.url
        logging.info(f"Final URL after redirects: {final_url}")
        
        # Check if final URL is success page
        if "/success" in final_url and response.status_code == 200:
            # Download random image
            random_image_path = download_random_image(session_id, session)
            if random_image_path:
                logging.info(f"Random image downloaded: {random_image_path}")
            else:
                logging.warning("Failed to download random image")
            
            logging.info(f"CAPTCHA verified successfully. Session ID: {session_id}, Text: {captcha_text}")
            return True, random_image_path
        elif response.status_code == 200:
            if response.text.strip():  # Check for empty response
                try:
                    data = response.json()
                    if data.get("success"):
                        logging.info(f"CAPTCHA verified successfully. Session ID: {session_id}, Text: {captcha_text}")
                        return True, None  # No image since no redirect
                    else:
                        logging.warning(f"Wrong CAPTCHA text. Session ID: {session_id}, Text: {captcha_text}, Message: {data.get('message')}")
                        return False, None
                except ValueError:
                    logging.error(f"Failed to parse JSON response: {response.text[:500]}")
                    raise Exception(f"Failed to parse JSON response: {response.text[:500]}")
            else:
                logging.error(f"Empty server response with status 200 for session_id: {session_id}")
                raise Exception("Empty server response with status 200")
        else:
            logging.error(f"CAPTCHA verification error: {response.status_code}, Response: {response.text[:500]}")
            raise Exception(f"CAPTCHA verification error: {response.status_code}, Response: {response.text[:500]}")
    except requests.RequestException as e:
        logging.error(f"Network error during CAPTCHA verification: {str(e)}, Response: {getattr(e.response, 'text', 'No data')[:500]}")
        raise Exception(f"Network error during CAPTCHA verification: {str(e)}")
