import pdf2image
import pytesseract
import os
import json
from requests.exceptions import ConnectionError

from excel_tools.excel_lookup import lookup_and_map_json
from generateJson.PO_json import gen_json


def read_pdf(file_path):
    images = pdf2image.convert_from_path(file_path, dpi=300, grayscale=True)
    extracted_text = ""
    for image in images[:1]:
        extracted_text += pytesseract.image_to_string(image)
    return extracted_text


def process_pdfs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    total_files = len(pdf_files)

    if total_files == 0:
        raise Exception("No PDF files found in the input folder.")

    processed_files = []

    for index, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_text = read_pdf(pdf_path)

        output_file_path = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_details.txt")
        if os.path.exists(output_file_path):
            with open(output_file_path, "r") as json_file:
                json_content = json.load(json_file)
            processed_files.append({"pdf_file": pdf_file, "json_content": json_content})
            continue  # Skip already processed files

        try:
            json_content = json.dumps(gen_json(pdf_text), indent=4)
            # print(jsoon)
            # Json to Excel by Mapping
            dummy_data_path = r'C:\Users\Shubham.Luxkar\Documents\Training\InvoicePOC\dummy_data.xlsx'
            output_path = r'C:\Users\Shubham.Luxkar\Documents\Training\InvoicePOC\output_mapped.xlsx'

            with open(output_file_path, "w") as txt_file:
                # Call the function with the provided JSON input and file paths
                lookup_and_map_json(json_content, dummy_data_path, output_path)
                txt_file.write(json_content)

        except ConnectionError:
            raise ConnectionError(f"Failed to connect to the Ollama model server for file: {pdf_file}. Please make "
                                  f"sure the server is running and try again.")
        except KeyError as e:
            raise KeyError(f"Key error for file: {pdf_file}: {e}. Please check the input text and schema.")
        except Exception as e:
            raise Exception(f"An error occurred for file: {pdf_file}: {e}")

    return processed_files



