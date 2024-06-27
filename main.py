from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

# model.train(data="config.yaml", epochs=30)

# Run batched inference on a list of images
results = model(["invoiceImages/invoiceImg_02.jpg"], stream=True, )  # return a generator of Results objects
names = model.names
# Process results generator
for result in results:
    for c in result.boxes.cls:
        print(names[int(c)])
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    with open("coordinates.txt", "w") as file:
        file.write(f"""boxes = {boxes}\n------------\n
                   """)
        result.show()  # display to screen
        result.save(filename="result.jpg")  # save to disk
