"""
ocr_engine.py - OCR text extraction using Tesseract
Place this file in: invoice_extraction/src/ocr_engine.py
"""

import pytesseract
import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Dict
import logging

from src.utils.logger import get_logger

logger = get_logger(__name__)

class OCREngine:
    """Handle OCR text extraction"""
    
    def __init__(self, config: Dict = None):
        """Initialize OCR engine"""
        self.config = config or {}
        self.logger = get_logger(__name__)
    
    def extract_text(self, image) -> Tuple[str, float]:
        """Extract text from image"""
        try:
            if isinstance(image, np.ndarray):
                image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            psm = self.config.get('page_segmentation_mode', 3)
            oem = self.config.get('oem', 3)
            lang = self.config.get('language', 'eng')
            
            config_str = f"--psm {psm} --oem {oem}"
            
            text = pytesseract.image_to_string(image, lang=lang, config=config_str)
            
            data = pytesseract.image_to_data(image, lang=lang, config=config_str, 
                                            output_type=pytesseract.Output.DICT)
            
            confidences = [int(conf) for conf in data['confidence'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            confidence = avg_confidence / 100.0
            
            self.logger.info(f"Text extracted. Confidence: {confidence:.2f}")
            return text, confidence
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return "", 0.0
    
    def extract_text_with_details(self, image) -> Dict:
        """Extract text with detailed information"""
        try:
            if isinstance(image, np.ndarray):
                image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            psm = self.config.get('page_segmentation_mode', 3)
            oem = self.config.get('oem', 3)
            lang = self.config.get('language', 'eng')
            
            config_str = f"--psm {psm} --oem {oem}"
            
            text = pytesseract.image_to_string(image, lang=lang, config=config_str)
            
            data = pytesseract.image_to_data(image, lang=lang, config=config_str,
                                            output_type=pytesseract.Output.DICT)
            
            confidences = [int(conf) for conf in data['confidence'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            confidence = avg_confidence / 100.0
            
            result = {
                'text': text,
                'confidence': confidence,
                'word_count': len(text.split()),
                'char_count': len(text),
            }
            
            self.logger.info("Detailed extraction complete")
            return result
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return {'text': '', 'confidence': 0.0, 'word_count': 0, 'char_count': 0}
    
    def validate_ocr_quality(self, text: str, confidence: float, 
                            min_confidence: float = 0.7) -> Tuple[bool, str]:
        """Validate OCR quality"""
        if confidence < min_confidence:
            return False, f"Low confidence: {confidence:.2f}"
        
        if len(text.strip()) < 10:
            return False, "Text too short"
        
        return True, "Quality acceptable"


def extract_text_from_image(image) -> Tuple[str, float]:
    """Convenience function"""
    engine = OCREngine()
    return engine.extract_text(image)