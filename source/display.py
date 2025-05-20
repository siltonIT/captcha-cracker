import cv2

def show_images(original_path, processed_path):
    # Загрузка изображений
    original = cv2.imread(original_path)
    processed = cv2.imread(processed_path)
    
    # Получение размеров оригинального изображения
    height, width = original.shape[:2]
    
    # Отображение изображений в отдельных окнах
    cv2.imshow("Original Captcha", original)
    cv2.imshow("Processed Captcha", processed)
    
    # Перемещение окон: "Original Captcha" слева, "Processed Captcha" справа
    cv2.moveWindow("Original Captcha", 0, 0)
    cv2.moveWindow("Processed Captcha", width + 250, height)
    
    print("Нажмите любую клавишу, чтобы закрыть окна с изображениями...")
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()
