"""
validator.py - Validate extracted invoice data
Place this file in: invoice_extraction/src/validator.py
"""

import re
from typing import Dict, Any, Tuple, List
import logging
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)

class InvoiceValidator:
    """Validate extracted invoice data"""
    
    def __init__(self, rules: Dict = None):
        """Initialize validator"""
        self.rules = rules or {}
        self.logger = get_logger(__name__)
        self.errors = []
        self.warnings = []
    
    def validate_invoice_number(self, invoice_number: str) -> Tuple[bool, str]:
        """Validate invoice number"""
        if not invoice_number:
            msg = "Invoice number is empty"
            return False, msg
        
        if len(invoice_number) < 3:
            msg = "Invoice number too short"
            return False, msg
        
        return True, "Valid"
    
    def validate_date(self, date_str: str) -> Tuple[bool, str]:
        """Validate date"""
        if not date_str:
            return False, "Date is empty"
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            
            if date_obj > datetime.now():
                return False, "Date is in future"
            
            return True, "Valid"
        
        except ValueError:
            return False, f"Invalid date format: {date_str}"
    
    def validate_amount(self, amount: float, field_name: str = "Amount") -> Tuple[bool, str]:
        """Validate amount"""
        if amount < 0:
            return False, f"{field_name} cannot be negative"
        
        if amount == 0:
            return False, f"{field_name} is zero"
        
        return True, "Valid"
    
    def validate_invoice_totals(self, subtotal: float, tax: float, 
                               total: float, tolerance: float = 0.1) -> Tuple[bool, str]:
        """Validate invoice totals"""
        expected_total = subtotal + tax
        difference = abs(expected_total - total)
        
        if difference > tolerance:
            return False, f"Total mismatch"
        
        return True, "Valid"
    
    def validate_invoice_data(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate complete invoice data"""
        self.errors = []
        self.warnings = []
        
        try:
            # Validate invoice number
            is_valid, msg = self.validate_invoice_number(data.get('invoice_number', ''))
            if not is_valid:
                self.errors.append(msg)
            
            # Validate date
            is_valid, msg = self.validate_date(data.get('invoice_date', ''))
            if not is_valid:
                self.errors.append(msg)
            
            # Validate amounts
            is_valid, msg = self.validate_amount(data.get('total', 0), 'Total')
            if not is_valid:
                self.errors.append(msg)
            
            # Validate totals
            subtotal = data.get('subtotal', 0)
            tax = data.get('tax', 0)
            total = data.get('total', 0)
            
            if subtotal > 0 and total > 0:
                is_valid, msg = self.validate_invoice_totals(subtotal, tax, total)
                if not is_valid:
                    self.warnings.append(msg)
            
            overall_valid = len(self.errors) == 0
            
            if overall_valid:
                self.logger.info("Validation passed")
            else:
                self.logger.error(f"Validation failed: {len(self.errors)} errors")
            
            return overall_valid, self.errors
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False, [str(e)]


def validate_invoice(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Convenience function"""
    validator = InvoiceValidator()
    return validator.validate_invoice_data(data)