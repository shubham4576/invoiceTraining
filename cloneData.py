import os
import shutil


def clone_files(file1_path, file2_path, num_clones):
    # Check if both files exist
    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        print("Error: One or both input files do not exist.")
        return

    # Create a directory to store labelme_json_dir (if it doesn't exist)
    clone_dir = "img_clone"
    os.makedirs(clone_dir, exist_ok=True)

    # Create labelme_json_dir of both files
    for i in range(2, num_clones + 2):  # Start naming from invoiceImg_02
        clone_name1 = os.path.join(clone_dir, f"invoiceImg_{i}_1.jpg")
        clone_name2 = os.path.join(clone_dir, f"invoiceImg_{i}_2.jpg")

        # Clone file 1
        shutil.copyfile(file1_path, clone_name1)
        print(f"Created clone: {clone_name1}")

        # Clone file 2
        shutil.copyfile(file2_path, clone_name2)
        print(f"Created clone: {clone_name2}")


if __name__ == "__main__":
    file1_path = "invoiceImages/invoiceImg_01.jpg"  # Replace with actual file path
    file2_path = "invoiceImages/invoiceImg_02.jpg"  # Replace with actual file path
    num_clones = 50  # Number of labelme_json_dir to create

    clone_files(file1_path, file2_path, num_clones)
