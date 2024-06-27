import cv2
import pytesseract
import json
import os
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Shubham.Luxkar\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Define the mapping of class IDs to descriptions
class_id_mapping = {
    0: "Order_Number",
    1: "Order_Date",
    2: "Delivery_Date",
    3: "Delivery_Address",
    4: "Product_Code"
}


def read_bounding_boxes_from_file(file_path):
    with open(file_path, 'r') as file:
        bounding_boxes_text = file.read()

    # Use regex to extract bounding box data
    pattern = re.compile(r'data: tensor\(\[\[(.*?)\]\]\)', re.DOTALL)
    match = pattern.search(bounding_boxes_text)
    if not match:
        raise ValueError("No bounding box data found in the file")

    # Extract the content inside the brackets
    bbox_data = match.group(1).strip()

    # Split the data into individual entries
    entries = bbox_data.split('],\n        [')
    bounding_boxes = []
    classes = []

    for entry in entries:
        values = list(map(float, entry.split(', ')))
        xmin, ymin, xmax, ymax, _, class_id = values
        bounding_boxes.append([xmin, ymin, xmax, ymax])
        classes.append(class_id)

    return bounding_boxes, classes


def extract_text_from_bounding_boxes(image_path, bounding_boxes, classes):
    # Load the image
    image = cv2.imread(image_path)

    extracted_data = {}

    for bbox, cls in zip(bounding_boxes, classes):
        xmin, ymin, xmax, ymax = bbox
        roi = image[int(ymin):int(ymax), int(xmin):int(xmax)]

        # Use Tesseract to extract text from the ROI
        text = pytesseract.image_to_string(roi).strip()

        # Map the class ID to the description
        class_name = class_id_mapping.get(int(cls), f"Class_{int(cls)}")
        if class_name not in extracted_data:
            extracted_data[class_name] = []

        extracted_data[class_name].append(text)

    return extracted_data


def save_data_as_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def get_json_filename(image_path):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    return f"{base_name}_extracted_text.json"


bounding_boxes_file = 'coordinates.txt'
# Example usage
image_path = 'result.jpg'

bounding_boxes, classes = read_bounding_boxes_from_file(bounding_boxes_file)
extracted_data = extract_text_from_bounding_boxes(image_path, bounding_boxes, classes)
json_filename = get_json_filename(image_path)
save_data_as_json(extracted_data, json_filename)

print(f"Extracted text saved to {json_filename}")
