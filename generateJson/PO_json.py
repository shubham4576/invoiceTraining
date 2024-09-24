from langchain.chains import create_extraction_chain
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from schema_structure.schemas import *

model = OllamaFunctions(model="llama3.1:latest", tempurature=0)


def combine_json_objects(*args):
    """
    Combine multiple JSON objects (dictionaries) into a single dictionary.

    If a list is encountered, its elements are recursively processed.
    If a dictionary is encountered, its key-value pairs are added to the combined dictionary.

    :param args: Variable number of arguments (dictionaries or lists)
    :return: A single dictionary containing all key-value pairs
    """
    combined_data = {}
    for arg in args:
        if isinstance(arg, dict):
            combined_data.update(arg)
        elif isinstance(arg, list):
            for item in arg:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if key in combined_data and isinstance(combined_data[key], list):
                            combined_data[key].append(value)
                        elif key in combined_data:
                            combined_data[key] = [combined_data[key], value]
                        else:
                            combined_data[key] = [value]
                else:
                    combined_data[str(len(combined_data))] = item
    return combined_data


def gen_json(text_data):
    detail_1 = get_user_data_schema()
    chain_1 = create_extraction_chain(detail_1, model)
    output_1 = chain_1.run(text_data)

    detail_2 = get_product_data_schema()
    chain_2 = create_extraction_chain(detail_2, model)
    output_2 = chain_2.run(text_data)

    detail_3 = get_supplier_data_schema()
    chain_3 = create_extraction_chain(detail_3, model)
    output_3 = chain_3.run(text_data)

    detail_4 = get_product_item_schema()
    chain_4 = create_extraction_chain(detail_4, model)
    output_4 = chain_4.run(text_data)

    final_output = combine_json_objects(output_1, output_2, output_3, output_4)
    return final_output
