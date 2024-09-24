import pdf2image
import pytesseract
import os
import json
from requests.exceptions import ConnectionError
from schema_structure.models import model

def read_pdf(file_path):
    images = pdf2image.convert_from_path(file_path, dpi=300, grayscale=True)
    extracted_text = ""
    for image in images:
        extracted_text += pytesseract.image_to_string(image)
    return extracted_text

def extract_details_from_text(pdf_text):
    order_details = model.invoke(pdf_text, function_call={"name": "get_order_details"})
    product_details = model.invoke(pdf_text, function_call={"name": "get_product_details"})
    return {"order_details": order_details, "product_details": product_details}

def extract_tool_calls_data(details):
    tool_calls_data = {}
    for key, value in details.items():
        tool_calls = value.tool_calls
        for call in tool_calls:
            tool_calls_data[key] = call['args']
    return tool_calls_data

def process_pdfs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf") ]
    total_files = len(pdf_files)

    if total_files == 0:
        raise Exception("No PDF files  in the input folder.")

    processed_files = []

    for index, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_text = read_pdf(pdf_path)
        
        # # Save extracted text to a file
        # extracted_text_file_path = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}.txt")
        # with open(extracted_text_file_path, "w") as text_file:
        #     text_file.write(pdf_text)

        output_file_path = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_details.txt")
        if os.path.exists(output_file_path):
            with open(output_file_path, "r") as json_file:
                json_content = json.load(json_file)
            processed_files.append({"pdf_file": pdf_file, "json_content": json_content})
            continue  # Skip already processed files

        try:
            details = extract_details_from_text(pdf_text)
            tool_calls_data = extract_tool_calls_data(details)
            json_content = json.dumps(tool_calls_data, indent=4)

            with open(output_file_path, "w") as txt_file:
                txt_file.write(json_content)

            processed_files.append({"pdf_file": pdf_file, "json_content": tool_calls_data})
        except ConnectionError:
            raise ConnectionError(f"Failed to connect to the Ollama model server for file: {pdf_file}. Please make sure the server is running and try again.")
        except KeyError as e:
            raise KeyError(f"Key error for file: {pdf_file}: {e}. Please check the input text and schema.")
        except Exception as e:
            raise Exception(f"An error occurred for file: {pdf_file}: {e}")

    return processed_files
