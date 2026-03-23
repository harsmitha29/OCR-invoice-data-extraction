"""
field_extractor.py - Extract specific fields from invoice text
Place this file in: invoice_extraction/src/field_extractor.py
"""

import re
from typing import Dict, Any, List
import logging

from .text_processor import TextProcessor
from src.utils.logger import get_logger

logger = get_logger(__name__)

class FieldExtractor:
    """Extract specific fields from invoice text"""
    
    DEFAULT_PATTERNS = {
        'invoice_number': r'(?:Invoice|Bill|Reference|Ref|INV)\s*(?:No\.?|Number|#)?\s*[:=]?\s*([A-Za-z0-9\-/]+)',
        'invoice_date': r'(?:Date|Invoice Date|Bill Date)\s*[:=]?\s*([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})',
        'vendor_name': r'(?:From|Vendor|Supplier|Company)\s*[:=]?\s*([A-Za-z\s&]+)',
        'customer_name': r'(?:To|Bill To|Customer|Buyer)\s*[:=]?\s*([A-Za-z\s&]+)',
        'subtotal': r'(?:Subtotal|Sub Total)\s*[:=]?\s*(?:Rs\.?|\$)?\s*([0-9,]+\.?[0-9]*)',
        'tax_amount': r'(?:Tax|GST|VAT)\s*[:=]?\s*(?:Rs\.?|\$)?\s*([0-9,]+\.?[0-9]*)',
        'total_amount': r'(?:Total|Grand Total|Amount Due)\s*[:=]?\s*(?:Rs\.?|\$)?\s*([0-9,]+\.?[0-9]*)',
    }
    
    def __init__(self, patterns: Dict = None):
        """Initialize field extractor"""
        self.patterns = patterns or self.DEFAULT_PATTERNS.copy()
        self.text_processor = TextProcessor()
        self.logger = get_logger(__name__)
    
    def extract_field(self, text: str, field_name: str, pattern: str = None) -> str:
        """Extract single field from text"""
        try:
            if pattern is None:
                pattern = self.patterns.get(field_name)
            
            if pattern is None:
                self.logger.warning(f"No pattern for: {field_name}")
                return ""
            
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            
            if match:
                value = match.group(1) if match.groups() else match.group(0)
                value = value.strip()
                self.logger.info(f"Extracted {field_name}: {value[:50]}")
                return value
            
            return ""
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return ""
    
    def extract_invoice_number(self, text: str) -> str:
        """Extract invoice number"""
        return self.extract_field(text, 'invoice_number')
    
    def extract_invoice_date(self, text: str) -> str:
        """Extract invoice date"""
        date_str = self.extract_field(text, 'invoice_date')
        if date_str:
            return self.text_processor.parse_date(date_str)
        return ""
    
    def extract_vendor_name(self, text: str) -> str:
        """Extract vendor name"""
        return self.extract_field(text, 'vendor_name')
    
    def extract_customer_name(self, text: str) -> str:
        """Extract customer name"""
        return self.extract_field(text, 'customer_name')
    
    def extract_amounts(self, text: str) -> Dict[str, float]:
        """Extract monetary amounts"""
        amounts = {}
        
        for field in ['subtotal', 'tax_amount', 'total_amount']:
            amount_str = self.extract_field(text, field)
            if amount_str:
                amounts[field] = self.text_processor.parse_currency_amount(amount_str)
            else:
                amounts[field] = 0.0
        
        return amounts
    
    def extract_all_fields(self, text: str) -> Dict[str, Any]:
        """Extract all available fields"""
        try:
            amounts = self.extract_amounts(text)
            
            extracted = {
                'invoice_number': self.extract_invoice_number(text),
                'invoice_date': self.extract_invoice_date(text),
                'vendor': {
                    'name': self.extract_vendor_name(text),
                },
                'customer': {
                    'name': self.extract_customer_name(text),
                },
                'subtotal': amounts['subtotal'],
                'tax': amounts['tax_amount'],
                'total': amounts['total_amount'],
            }
            
            self.logger.info("All fields extracted")
            return extracted
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return {}


def extract_invoice_fields(text: str) -> Dict[str, Any]:
    """Convenience function"""
    extractor = FieldExtractor()
    return extractor.extract_all_fields(text)