from processing_tools.pdf_processor import process_pdfs_in_folder


def process_pdfs():
    try:
        # Process PDFs using hardcoded folder paths
        processed_files = process_pdfs_in_folder(input_folder, output_folder)

        if processed_files:
            # Return success message if any files were processed
            return {"message": "PDF processing completed successfully."}
        else:
            return {"message": "No PDF files processed."}
    except Exception as e:
        return {"message": f"Error processing PDFs: {str(e)}"}


if __name__ == '__main__':
    input_folder = "/home/trainee/Project/InvoicePOC/mailPdfs"
    output_folder = "/home/trainee/Project/InvoicePOC/extracted_text"
    process_pdfs()