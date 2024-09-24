
---

# InvoicePOC

## Overview
InvoicePOC is a Python-based project designed to handle various operations related to invoices. This includes email extraction, PDF processing, JSON data generation, and schema validation. The project is organized into several modules, each responsible for a specific aspect of the process.

## Directory Structure
```
InvoicePOC
│   .env
│   dummy_data.xlsx
│   img.png
│   main.py
│   output.xlsx
│   output_mapped.xlsx
│   scheduler.py
│
├───.idea
│   │   .gitignore
│   │   InvoicePOC.iml
│   │   material_theme_project_new.xml
│   │   misc.xml
│   │   modules.xml
│   │   workspace.xml
│   │
│   └───inspectionProfiles
│           profiles_settings.xml
│
├───email_tools
│       email_fetch.py
│       __init__.py
│
├───excel_tools
│       excel_lookup.py
│       __init__.py
│
├───extracted_text
│   │   PO_JFB_PO_00015058_03.txt
│   │   PO_JFB_PO_00015058_03_details.txt
│   │
│   └───.ipynb_checkpoints
│           PO_JFB_PO_00015058_03-checkpoint.txt
│           PO_JFB_PO_00015058_03_details-checkpoint.txt
│
├───generateJson
│       PO_json.py
│       __init__.py
│
├───mailPdfs
│       PO_JFB_PO_00015058_03.pdf
│
├───processing_tools
│       pdf_processor.py
│       __init__.py
│
└───schema_structure
    │   schemas.py
    │   __init__.py
    │
    ├───.ipynb_checkpoints
    │       email_fetch-checkpoint.py
    │       email_fetch_test-checkpoint.py
    │       pdf_processor-checkpoint.py
    │       schemas-checkpoint.py
    │
    └───__pycache__
            schemas.cpython-311.pyc
            schemas.cpython-312.pyc
            __init__.cpython-311.pyc
            __init__.cpython-312.pyc
```

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/InvoicePOC.git
    ```
2. Navigate to the project directory:
    ```bash
    cd InvoicePOC
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the environment variables:
    - Create a `.env` file in the root directory and add necessary environment variables.

## Usage
1. **Email Fetching**: To fetch emails and extract PDFs, run:
    ```bash
    python email_tools/email_fetch.py
    ```
2. **PDF Processing**: To process PDFs and extract text, run:
    ```bash
    python processing_tools/pdf_processor.py
    ```
3. **Generate JSON**: To generate JSON data from the extracted text, run:
    ```bash
    python generateJson/PO_json.py
    ```
4. **Excel Lookup**: To perform Excel lookups, run:
    ```bash
    python excel_tools/excel_lookup.py
    ```
5. **Scheduler**: To schedule tasks, run:
    ```bash
    python scheduler.py
    ```

## Modules

### email_tools
- **email_fetch.py**: Fetches emails and extracts attachments.

### excel_tools
- **excel_lookup.py**: Handles lookups and operations related to Excel files.

### extracted_text
- Contains extracted text files from PDFs.

### generateJson
- **PO_json.py**: Generates JSON data from extracted text.

### mailPdfs
- Stores the PDFs fetched from emails.

### processing_tools
- **pdf_processor.py**: Processes PDFs and extracts text.

### schema_structure
- **schemas.py**: Contains schema definitions and validation logic.

## Code Improvement Suggestions
- **Modularization**: Ensure that each function performs a single task and modules are clearly defined.
- **Error Handling**: Implement comprehensive error handling to manage exceptions gracefully.
- **Logging**: Incorporate logging to track the flow of the application and debug issues.
- **Documentation**: Document functions and modules to provide clear descriptions of their functionality.
- **Testing**: Write unit tests for critical functions to ensure reliability and correctness.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

---

Feel free to customize this README file further according to your project's specific requirements and details.