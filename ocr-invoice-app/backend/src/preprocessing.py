"""
preprocessing.py - Image enhancement and preprocessing
Place this file in: invoice_extraction/src/preprocessing.py
"""

import cv2
import numpy as np
from PIL import Image
from typing import Union
import logging

from src.utils.logger import get_logger

logger = get_logger(__name__)

class ImagePreprocessor:
    """Handle image preprocessing for better OCR"""
    
    def __init__(self):
        """Initialize preprocessor"""
        self.logger = get_logger(__name__)
    
    @staticmethod
    def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
        """Convert PIL image to OpenCV format"""
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def cv2_to_pil(cv2_image: np.ndarray) -> Image.Image:
        """Convert OpenCV image to PIL format"""
        return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
    
    def resize_image(self, image: np.ndarray, scale_factor: float = 2.0) -> np.ndarray:
        """Resize image for better OCR"""
        try:
            height, width = image.shape[:2]
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            resized = cv2.resize(image, (new_width, new_height), 
                                interpolation=cv2.INTER_CUBIC)
            
            self.logger.info(f"Image resized: {width}x{height} -> {new_width}x{new_height}")
            return resized
        
        except Exception as e:
            self.logger.error(f"Error resizing: {e}")
            return image
    
    def grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale"""
        try:
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                self.logger.info("Converted to grayscale")
                return gray
            return image
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return image
    
    def apply_threshold(self, image: np.ndarray, threshold_value: int = 127) -> np.ndarray:
        """Apply binary thresholding"""
        try:
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            _, thresh = cv2.threshold(image, threshold_value, 255, 
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            self.logger.info("Threshold applied")
            return thresh
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return image
    
    def denoise(self, image: np.ndarray) -> np.ndarray:
        """Remove noise from image"""
        try:
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            denoised = cv2.bilateralFilter(gray, 9, 75, 75)
            
            self.logger.info("Denoising applied")
            return denoised
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return image
    
    def enhance_contrast(self, image: np.ndarray, clip_limit: float = 2.0) -> np.ndarray:
        """Enhance image contrast using CLAHE"""
        try:
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            self.logger.info("Contrast enhanced")
            return enhanced
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return image
    
    def preprocess_image(self, image: np.ndarray, 
                        resize: bool = True, 
                        scale_factor: float = 2.0,
                        apply_grayscale: bool = True,
                        apply_threshold: bool = True,
                        apply_denoise: bool = True,
                        apply_contrast: bool = True) -> np.ndarray:
        """Complete preprocessing pipeline"""
        try:
            processed = image.copy()
            
            if resize:
                processed = self.resize_image(processed, scale_factor)
            
            if apply_grayscale:
                processed = self.grayscale(processed)
            
            if apply_denoise:
                processed = self.denoise(processed)
            
            if apply_contrast:
                processed = self.enhance_contrast(processed)
            
            if apply_threshold:
                processed = self.apply_threshold(processed)
            
            self.logger.info("Preprocessing complete")
            return processed
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return image


def preprocess_pil_image(pil_image: Image.Image) -> Image.Image:
    """Convenience function"""
    preprocessor = ImagePreprocessor()
    cv2_image = preprocessor.pil_to_cv2(pil_image)
    processed = preprocessor.preprocess_image(cv2_image)
    return preprocessor.cv2_to_pil(processed)