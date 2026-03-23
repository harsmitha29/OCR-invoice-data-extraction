"""
FastAPI Backend - OCR Invoice Data Extraction
Authors: Harsmitha K & Jahnavi K L
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import tempfile
import os
import shutil
from pathlib import Path
from typing import Optional
import logging

from src.input_handler import InputHandler
from src.preprocessing import ImagePreprocessor
from src.ocr_engine import OCREngine
from src.text_processor import TextProcessor
from src.field_extractor import FieldExtractor
from src.validator import InvoiceValidator
from src.output_generator import OutputGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OCR Invoice Data Extraction API",
    description="Extract structured data from invoice documents using OCR",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


class InvoiceExtractionPipeline:
    """Complete invoice extraction pipeline"""

    def __init__(self):
        self.input_handler = InputHandler()
        self.preprocessor = ImagePreprocessor()
        self.ocr_engine = OCREngine()
        self.text_processor = TextProcessor()
        self.field_extractor = FieldExtractor()
        self.validator = InvoiceValidator()
        self.output_generator = OutputGenerator(str(OUTPUT_DIR))

    def process_invoice(self, file_path: str) -> dict:
        """Process a single invoice file"""
        import cv2
        import numpy as np

        logger.info(f"Processing: {file_path}")

        images = self.input_handler.load_file(file_path)
        if not images:
            raise ValueError("Failed to load invoice file")

        all_text = ""
        for image in images:
            cv2_image = self.preprocessor.pil_to_cv2(image)
            processed = self.preprocessor.preprocess_image(cv2_image)
            text, confidence = self.ocr_engine.extract_text(processed)
            all_text += text + "\n"

        extracted_data = self.field_extractor.extract_all_fields(all_text)
        is_valid, errors = self.validator.validate_invoice_data(extracted_data)
        extracted_data["validation_passed"] = is_valid
        extracted_data["validation_errors"] = errors
        extracted_data["raw_text"] = all_text.strip()

        logger.info("Processing complete")
        return extracted_data


pipeline = InvoiceExtractionPipeline()


@app.get("/")
def root():
    return {"message": "OCR Invoice Extraction API", "status": "running", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/extract")
async def extract_invoice(file: UploadFile = File(...)):
    """
    Upload an invoice (PDF or image) and extract structured data.
    Supported formats: PDF, JPG, JPEG, PNG, BMP, TIFF
    """
    allowed_types = {
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/bmp",
        "image/tiff",
    }
    allowed_extensions = {".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Allowed: {', '.join(allowed_extensions)}",
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        result = pipeline.process_invoice(tmp_path)

        # Save outputs
        base_name = Path(file.filename).stem
        pipeline.output_generator.generate_all_outputs(result, base_name)

        return JSONResponse(
            content={
                "success": True,
                "filename": file.filename,
                "data": result,
            }
        )

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        os.unlink(tmp_path)


@app.get("/download/{format}/{filename}")
def download_output(format: str, filename: str):
    """Download extracted data as JSON or CSV"""
    if format not in ("json", "csv"):
        raise HTTPException(status_code=400, detail="Format must be 'json' or 'csv'")

    file_path = OUTPUT_DIR / f"{filename}.{format}"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")

    media_type = "application/json" if format == "json" else "text/csv"
    return FileResponse(path=str(file_path), media_type=media_type, filename=f"{filename}.{format}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
