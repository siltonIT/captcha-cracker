import cv2

def show_image(original_path):
    # Загрузка изображений
    original = cv2.imread(original_path)
    
    # Получение размеров оригинального изображения
    height, width = original.shape[:2]
    
    # Отображение изображений в отдельных окнах
    cv2.imshow("Image", original)
    
    print("Нажмите любую клавишу, чтобы закрыть окна с изображениями...")
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()
