import json
import os


def labelme2yolo(labelme_json, output_dir):
    # Load JSON data
    with open(labelme_json) as f:
        data = json.load(f)

    image_width = data['imageWidth']
    image_height = data['imageHeight']
    shapes = data['shapes']

    # Create YOLO annotation file
    yolo_annotations = []
    for shape in shapes:
        label = shape['labels']
        points = shape['points']

        if shape['shape_type'] != 'rectangle':
            continue

        x_min = min(points[0][0], points[1][0])
        y_min = min(points[0][1], points[1][1])
        x_max = max(points[0][0], points[1][0])
        y_max = max(points[0][1], points[1][1])

        box_width = x_max - x_min
        box_height = y_max - y_min
        center_x = x_min + box_width / 2
        center_y = y_min + box_height / 2

        # Normalize
        center_x /= image_width
        center_y /= image_height
        box_width /= image_width
        box_height /= image_height

        # Assuming labels mapping is needed, define a class list
        # You may need to adjust the class list based on your labels
        class_list = ["Order_Number", "Order_Date", "Delivery_Date", "Delivery_Address", "Product_Code"]  # Example class list
        class_id = class_list.index(label)

        yolo_annotation = f"{class_id} {center_x} {center_y} {box_width} {box_height}"
        yolo_annotations.append(yolo_annotation)

    # Define output file path
    image_filename = os.path.splitext(os.path.basename(data['imagePath']))[0]
    output_path = os.path.join(output_dir, f"{image_filename}.txt")

    # Save YOLO annotations to file
    with open(output_path, 'w') as f:
        for ann in yolo_annotations:
            f.write(ann + '\n')


def process_directory(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each JSON file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(input_dir, filename)
            labelme2yolo(json_path, output_dir)
            print(f"Processed {filename}")


# Usage example
input_directory = 'json_data'  # Path to your input directory containing Labelme JSON files
output_directory = 'yolo_data'  # Path to save YOLO annotation files
process_directory(input_directory, output_directory)
