import os

from processing_tools.pdf_processor import process_pdfs_in_folder


def process_pdfs(_input_folder: str, _output_folder: str):
    try:
        # Process PDFs using hardcoded folder paths
        processed_files = process_pdfs_in_folder(_input_folder, _output_folder)

        if processed_files:
            # Return success message if any files were processed
            return {"message": "PDF processing completed successfully."}
        else:
            return {"message": "No PDF files processed."}
    except Exception as e:
        return {"message": f"Error processing PDFs: {str(e)}"}


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(current_dir, "mailPdfs")
    output_folder = os.path.join(current_dir, "extracted_text")
    process_pdfs(input_folder, output_folder)
