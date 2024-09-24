from pydantic import BaseModel
from typing import List, Dict, Any

class PDFProcessRequest(BaseModel):
    input_folder: str
    output_folder: str
    
class PDFProcessResponse(BaseModel):
    message: str
    processed_files: List[Dict[str, Any]]
