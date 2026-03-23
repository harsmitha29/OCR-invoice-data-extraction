"""
input_handler.py - File input and validation
Place this file in: invoice_extraction/src/input_handler.py
"""

import os
from pathlib import Path
from typing import List, Tuple, Union
import logging

try:
    from pdf2image import convert_from_path
except ImportError:
    convert_from_path = None

from PIL import Image
from src.utils.logger import get_logger

logger = get_logger(__name__)

class InputHandler:
    """Handle input file validation and processing"""
    
    SUPPORTED_FORMATS = {'.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    def __init__(self):
        """Initialize input handler"""
        self.logger = get_logger(__name__)
    
    def validate_file(self, file_path: Union[str, Path]) -> Tuple[bool, str]:
        """Validate input file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            msg = f"File not found: {file_path}"
            self.logger.error(msg)
            return False, msg
        
        if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            msg = f"Unsupported format: {file_path.suffix}"
            self.logger.error(msg)
            return False, msg
        
        file_size = file_path.stat().st_size
        if file_size > self.MAX_FILE_SIZE:
            msg = f"File too large: {file_size} bytes"
            self.logger.error(msg)
            return False, msg
        
        self.logger.info(f"File validation passed: {file_path}")
        return True, "File is valid"
    
    def load_file(self, file_path: Union[str, Path], dpi: int = 300) -> List[Image.Image]:
        """Load file and return as list of images"""
        file_path = Path(file_path)
        
        is_valid, message = self.validate_file(file_path)
        if not is_valid:
            self.logger.error(f"Validation failed: {message}")
            return []
        
        images = []
        
        if file_path.suffix.lower() == '.pdf':
            try:
                if convert_from_path is None:
                    self.logger.error("pdf2image not installed")
                    return []
                
                pdf_images = convert_from_path(str(file_path), dpi=dpi)
                images = pdf_images
                self.logger.info(f"Converted PDF to {len(images)} images")
            
            except Exception as e:
                self.logger.error(f"Error converting PDF: {e}")
                return []
        
        else:
            try:
                image = Image.open(file_path)
                images = [image]
                self.logger.info(f"Image loaded: {file_path}")
            except Exception as e:
                self.logger.error(f"Error loading image: {e}")
                return []
        
        return images


def load_invoice(file_path: Union[str, Path]) -> List[Image.Image]:
    """Convenience function to load invoice"""
    handler = InputHandler()
    return handler.load_file(file_path)