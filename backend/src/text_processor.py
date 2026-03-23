"""
text_processor.py - Parse and structure extracted text
Place this file in: invoice_extraction/src/text_processor.py
"""

import re
from typing import Dict, List, Any
import logging
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)

class TextProcessor:
    """Process and parse extracted OCR text"""
    
    def __init__(self):
        """Initialize text processor"""
        self.logger = get_logger(__name__)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        try:
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'[^\w\s\-\./,():%@]', '', text)
            text = text.strip()
            
            self.logger.info("Text cleaned")
            return text
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return text
    
    def extract_lines(self, text: str) -> List[str]:
        """Extract lines from text"""
        lines = text.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        
        self.logger.info(f"Extracted {len(lines)} lines")
        return lines
    
    def extract_words(self, text: str) -> List[str]:
        """Extract words from text"""
        words = text.split()
        return words
    
    def find_pattern_in_text(self, text: str, pattern: str) -> List[str]:
        """Find all matches of pattern in text"""
        try:
            matches = re.findall(pattern, text, re.IGNORECASE)
            return matches
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return []
    
    def find_pattern_first_match(self, text: str, pattern: str) -> str:
        """Find first match of pattern"""
        try:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1) if match.groups() else match.group(0)
            return ""
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return ""
    
    def parse_currency_amount(self, amount_str: str) -> float:
        """Parse currency amount"""
        try:
            cleaned = re.sub(r'[^\d,.-]', '', amount_str)
            cleaned = cleaned.replace(',', '')
            amount = float(cleaned)
            return amount
        
        except Exception as e:
            self.logger.warning(f"Error parsing amount: {e}")
            return 0.0
    
    def parse_date(self, date_str: str) -> str:
        """Parse date string and normalize"""
        try:
            formats = [
                '%d-%m-%Y',
                '%d/%m/%Y',
                '%Y-%m-%d',
                '%d.%m.%Y',
                '%d-%m-%y',
            ]
            
            date_str = date_str.strip()
            
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    normalized = date_obj.strftime('%Y-%m-%d')
                    self.logger.info(f"Date parsed: {normalized}")
                    return normalized
                except ValueError:
                    continue
            
            return date_str
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return date_str
    
    def structure_text(self, text: str) -> Dict[str, Any]:
        """Structure raw OCR text"""
        try:
            cleaned = self.clean_text(text)
            lines = self.extract_lines(cleaned)
            
            structure = {
                'raw_text': text,
                'cleaned_text': cleaned,
                'lines': lines,
                'line_count': len(lines),
                'word_count': len(self.extract_words(cleaned)),
                'has_numbers': bool(re.search(r'\d', text)),
                'has_currency': bool(re.search(r'Rs|$|£|€', text)),
            }
            
            self.logger.info("Text structured")
            return structure
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return {}


def process_text(text: str) -> Dict[str, Any]:
    """Convenience function"""
    processor = TextProcessor()
    return processor.structure_text(text)