import cv2

def show_image(path):
    """Displays an image in a window using OpenCV.
    
    Args:
        path (str): Path to the image file to be displayed.
        
    Behavior:
        - Loads the image from specified path
        - Displays it in a titled window
        - Waits for any key press to close
        - Cleans up all OpenCV windows afterwards
        
    Note:
        The function will block execution until a key is pressed.
    """
    # Load the image from file
    image = cv2.imread(path)
    
    # Display the image in a titled window
    cv2.imshow("Image", image)
    
    print("Press any key to close the image window...")
    cv2.waitKey(0)
    
    # Clean up all OpenCV windows
    cv2.destroyAllWindows()
