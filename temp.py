from ultralytics import YOLO
import os

# Initialize the YOLO model
model = YOLO("runs/detect/train/weights/best.pt")

# List of images to perform inference on
image_paths = ["invoiceImages/invoiceImg_02.jpg"]  # Replace with your list of image paths

# Create Prediction directory if it doesn't exist
os.makedirs("Prediction", exist_ok=True)

# Perform batched inference on the list of images
results = model.predict(image_paths, stream=True)  # return a generator of Results objects
names = model.names

# Counter for naming coordinate files
file_counter = 1

# Process results generator
for image_path, result in zip(image_paths, results):
    # Generate filename for coordinates.txt based on image name
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    coordinates_filename = f"Prediction/{image_name}_coordinates_{file_counter}.txt"

    # Save the predicted image
    result.save(filename=f"Prediction/{image_name}_predicted.jpg")

    # Save information about 'boxes' to the specified file
    with open(coordinates_filename, "w") as file:
        file.write("Information about 'boxes' attribute:\n\n")
        file.write(f"boxes (Boxes, optional): Object containing detection bounding boxes.\n\n")

        # Write bounding box coordinates
        boxes = result.boxes  # Get the boxes object from the result
        if boxes is not None:
            for box in boxes:
                cls = box.cls.item() if box.cls is not None else 'N/A'
                conf = box.conf.item() if box.conf is not None else 'N/A'
                x1, y1, x2, y2 = box.xyxy if box.xyxy is not None else ('N/A', 'N/A', 'N/A', 'N/A')
                file.write(f"Class: {names[int(cls)]}, Confidence: {conf}, Coordinates: [{x1}, {y1}, {x2}, {y2}]\n")

    # Increment the file counter
    file_counter += 1

    # Display the result on screen (optional)
    result.show()

print("Prediction and coordinate files saved successfully.")
