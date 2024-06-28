import os
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

# model.train(data="config.yaml", epochs=30)

image_paths = ["invoiceImages/invoiceImg_02.jpg"]  # Replace with your list of image paths

# Perform batched inference on the list of images
results = model.predict(image_paths, stream=True)  # return a generator of Results objects

for image_path in image_paths:
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    info_filename = f"Prediction/{image_name}_information.txt"

    # Save information about 'boxes' to the specified file
    with open(info_filename, "w") as file:
        for result in results:
            file.write(str(result.boxes))
    print(f"Information about 'boxes' attribute written to {info_filename}")

print("Information files saved successfully.")

