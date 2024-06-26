import os

import fitz


def rename_files_in_directory(directory_path):
    # List all files in the directory
    files = sorted(os.listdir(directory_path))
    # Initialize a counter
    counter = 1
    for filename in files:
        # Construct the new file name with zero-padded counter
        new_name = f"invoice_{counter:02d}"
        # Get the file extension
        file_extension = os.path.splitext(filename)[1]
        # Combine new name with original extension
        new_file_name = f"{new_name}{file_extension}"
        # Get full file paths
        old_file = os.path.join(directory_path, filename)
        new_file = os.path.join(directory_path, new_file_name)
        # Rename the file
        os.rename(old_file, new_file)

        # Increment the counter
        counter += 1


def pdftoimg(directory_path):
    # Ensure the output directory exists
    output_dir = "invoiceImages"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Initialize a counter for the images filenames
    counter = 1
    # Iterate through each file in the directory
    for filename in sorted(os.listdir(directory_path)):
        # Open the PDF file
        doc = fitz.open(os.path.join(directory_path, filename))
        # Iterate over each page in the PDF
        for page_num in range(0, 1):
            # Select the page
            page = doc.load_page(page_num)
            # Render page to an images
            pix = page.get_pixmap()
            # Generate the images file name
            img_file_name = f"invoiceImg_{counter:02d}.jpg"
            img_file_path = os.path.join(output_dir, img_file_name)
            # Save the images
            pix.save(img_file_path, "jpg", jpg_quality=100)
            # Increment the counter
            counter += 1


if __name__ == '__main__':
    path_to_directory = "dataset"
    rename_files_in_directory(path_to_directory)
    pdftoimg(path_to_directory)
