import cv2
import pytesseract
import os

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # converts to a grayscale img
    return gray

# performing ocr in a region of interest
def perform_ocr(image, roi):
    x, y, w, h = roi
    roi_image = image[y:y+h, x:x+w]
    # assumes its in a single column format
    custom_config = r'--oem 3 --psm 6'  
    text = pytesseract.image_to_string(roi_image, config=custom_config)
    return text

def extract_title(image, roi):
    title_text = perform_ocr(image, roi)
    return title_text.strip()

def detect_title(image_path):
    processed_image = preprocess_image(image_path)
    # assumes its in the top-20% of the img
    height, width = processed_image.shape[:2]
    roi = (0, 0, width, height // 5) 
    title = extract_title(processed_image, roi)
    title = title.replace('\n', ' ')
    return title

def process_images(file_paths):
    for path in file_paths:
        if not os.path.isfile(path):
            print(f"File not found: {path}")
            continue
        title = detect_title(path)
        if title:
            print(f"Detected Title for {path}:\n{title}")
        else:
            print(f"Title is not detected for {path}")

def process_images_in_folder(folder_path):
    file_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            file_paths.append(os.path.join(folder_path, filename))
    
    if not file_paths:
        print("No image files found in the folder:", folder_path)
        return
    process_images(file_paths)

# prompt
user_input = input("[1] Select a file or multiple separated by commas\n[2] Select a folder\n")
if user_input == '1':
    file_paths_input = input("Enter the path of the file, if theres multiple separate them with commas\n")
    file_paths = [path.strip() for path in file_paths_input.split(',')]
    process_images(file_paths)
elif user_input == '2':
    folder_path = input("Enter the path of the folder containing the image files\n")
    if os.path.isdir(folder_path):
        process_images_in_folder(folder_path)
    else:
        print("Invalid folder path entered.")
else:
    print("Please enter either 1 or 2.")

