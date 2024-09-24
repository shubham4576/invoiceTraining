import pandas as pd
import json
from openpyxl.reader.excel import load_workbook
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def autofit_excel_columns(_file_path):
    wb = load_workbook(_file_path)
    ws = wb.active

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except Exception as x:
                logger.warning(f"Error processing cell value: {x}")
        adjusted_width = max_length + 2
        ws.column_dimensions[column_letter].width = adjusted_width

    wb.save(_file_path)


def lookup_and_map_json(json_input, dummy_data_path, output_path):
    # Read the dummy data from the provided Excel file
    try:
        dummy_data = pd.read_excel(dummy_data_path)
    except Exception as e:
        print(f"Error reading the dummy data Excel file: {e}")
        return

    # Load the JSON input
    try:
        data = json.loads(json_input)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON input: {e}")
        return

    # Extract product names from the JSON input
    product_names = data.get('product_name', [])
    print(dummy_data)
    # Create a list to hold the mapped product names
    mapped_product_codes = []

    # Iterate through the product names and look them up in the dummy data
    for i, product_name in enumerate(product_names):
        product_code = data['product_code'][i]
        print(product_code) # Just for Debugging Purposes
        if product_code in dummy_data['Product Code'].values:
            index = dummy_data[dummy_data['Product Code'] == product_code].index[0]
            k = dummy_data.loc[index, 'Mapped Chef Code']  # Replace 'Mapped Column' with the actual column name
            mapped_product_codes.append(k)
        else:
            mapped_product_codes.append('NA')

    # Add the mapped product names to the JSON data
    data['Mapped_Chef_Code'] = mapped_product_codes
    print(data)
    # Create a new JSON output that contains only the details of the product that was found during mapping
    output_data = [
        {
            "ordered_by": data['ordered_by'][0],
            "buyer_email": data['buyer_email'][0],
            "buyer_name": data['buyer_name'][0],
            "requestor_name": data['requestor_name'][0],
            "requestor_email": data['requestor_email'][0],
            "po_number": data['po_number'][0],
            "order_date": data['order_date'][0],
            "po_total_aed": data['po_total_aed'][0],
            "tax_total_aed": data['tax_total_aed'][0],
            "grand_total_aed": data['grand_total_aed'][0],
            "bill_to": data['bill_to'][0],
            "supplier_address": data['supplier_address'][0],
            "product_group": product_group,
            "delivery_date": delivery_date,
            "uom": uom,
            "product_code": product_code,
            "quantity": quantity,
            "unit_price_aed": unit_price_aed,
            "tax_rate": tax_rate,
            "amount_aed": amount_aed,
            "line_total_aed": line_total_aed,
            "product_name": product_name,
            "Mapped_Chef_Code": mapped_product_codes
        }
        for
        product_name, product_group, delivery_date, uom, product_code, quantity, unit_price_aed, tax_rate, amount_aed,
        line_total_aed, mapped_product_codes
        in zip(
            product_names,
            data['product_group'],
            data['delivery_date'],
            data['uom'],
            data['product_code'],
            data['quantity'],
            data['unit_price_aed'],
            data['tax_rate'],
            data['amount_aed'],
            data['line_total_aed'],
            mapped_product_codes
        )
    ]
    # print(data)
    print(output_data)
    # Convert the JSON output to a DataFrame
    df = pd.json_normalize(output_data)

    # Write the updated JSON output to an output Excel file
    try:
        df.to_excel(output_path, index=False, engine='openpyxl')
        autofit_excel_columns(output_path)
        logger.info("Processing complete.")
    except Exception as e:
        print(f"Error writing to the output Excel file: {e}")


if __name__ == '__main__':
    # Sample JSON input
    json_input = '''
    {
        "ordered_by": ["Suhail Ediyanam Veed"],
        "buyer_email": ["suhail.veed@dhgroupservices.com"],
        "buyer_name": ["Suhail Ediyanam Veed"],
        "requestor_name": ["Jeremiah Nyahe Kimani"],
        "requestor_email": ["jeremiah.kimani@jumeirah.com"],
        "po_number": ["JFB-PO-OOO15058"],
        "order_date": ["03-APR-2024"],
        "po_total_aed": ["901.12"],
        "tax_total_aed": ["45.06"],
        "grand_total_aed": ["946.18"],
        "bill_to": ["Jumeirah F and B Concepts LLC, Level 1 Tower 4, Dubai Wharf(Jaddaf Waterfront Area), P O Box 123311"],
        "supplier_address": ["CHEF MIDDLE EAST LLC, Box 123311"],
        "product_group": ["Goods and/or Services", "Goods and/or Services"],
        "delivery_date": ["05-APR-2024", "05-APR-2024"],
        "uom": ["PACKA", "CASE"],
        "product_code": ["Fl105516", "F|115272"],
        "quantity": ["2", "8"],
        "unit_price_aed": ["55.00", "98.89"],
        "tax_rate": ["5.00", "5.00"],
        "amount_aed": ["110.00", "791.12"],
        "line_total_aed": ["115.50", "830.68"],
        "product_name": ["Egg Liquid Yolk Pasteurised EifiX Weisenhof", "French Fries Grade A Frozen 9*9mm McCain"]
    }
    '''

    # Paths to the input dummy data file and output file
    dummy_data_path = r'C:\Users\Shubham.Luxkar\Documents\Training\InvoicePOC\dummy_data.xlsx'
    output_path = r'C:\Users\Shubham.Luxkar\Documents\Training\InvoicePOC\output_mapped.xlsx'

    # Call the function with the provided JSON input and file paths
    lookup_and_map_json(json_input, dummy_data_path, output_path)
