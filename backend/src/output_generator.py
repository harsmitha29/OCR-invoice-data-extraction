"""
output_generator.py - Generate JSON and CSV output
Place this file in: invoice_extraction/src/output_generator.py
"""

import json
import csv
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
import logging

from src.utils.logger import get_logger

logger = get_logger(__name__)

class OutputGenerator:
    """Generate output in JSON and CSV formats"""
    
    def __init__(self, output_dir: str = 'output'):
        """Initialize output generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = get_logger(__name__)
    
    def save_json(self, data: Dict[str, Any], filename: str = 'extracted_data.json', 
                  indent: int = 2) -> bool:
        """Save data as JSON file"""
        try:
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            
            self.logger.info(f"JSON saved: {filepath}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False
    
    def save_csv(self, data: Dict[str, Any], filename: str = 'extracted_data.csv') -> bool:
        """Save data as CSV file"""
        try:
            filepath = self.output_dir / filename
            
            flat_data = self._flatten_dict(data)
            
            if not flat_data:
                self.logger.warning("No data")
                return False
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=flat_data.keys())
                writer.writeheader()
                writer.writerow(flat_data)
            
            self.logger.info(f"CSV saved: {filepath}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False
    
    @staticmethod
    def _flatten_dict(data: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        """Flatten nested dictionary"""
        items = []
        
        for k, v in data.items():
            new_key = f"{parent_key}_{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(OutputGenerator._flatten_dict(v, new_key).items())
            elif isinstance(v, list):
                items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
        
        return dict(items)
    
    def generate_all_outputs(self, data: Dict[str, Any], base_name: str = 'invoice') -> bool:
        """Generate all output formats"""
        try:
            results = []
            
            results.append(self.save_json(data, f'{base_name}.json'))
            results.append(self.save_csv(data, f'{base_name}.csv'))
            
            overall_success = all(results)
            
            if overall_success:
                self.logger.info(f"All outputs generated for {base_name}")
            else:
                self.logger.warning(f"Some outputs failed")
            
            return overall_success
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False


def save_invoice_data(data: Dict[str, Any], output_dir: str = 'output') -> bool:
    """Convenience function"""
    generator = OutputGenerator(output_dir)
    return generator.generate_all_outputs(data)