"""
helpers.py - Helper utility functions
Place this file in: invoice_extraction/utils/helpers.py
"""

from pathlib import Path
from typing import Union, List, Dict, Any
import re

class FileHelper:
    """File utility functions"""
    
    @staticmethod
    def is_supported_file(file_path: Union[str, Path]) -> bool:
        """Check if file format is supported"""
        SUPPORTED = {'.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        file_path = Path(file_path)
        return file_path.suffix.lower() in SUPPORTED
    
    @staticmethod
    def get_file_size(file_path: Union[str, Path]) -> int:
        """Get file size in bytes"""
        return Path(file_path).stat().st_size
    
    @staticmethod
    def create_directory(directory: Union[str, Path]) -> bool:
        """Create directory"""
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def list_files(directory: Union[str, Path], pattern: str = '*') -> List[Path]:
        """List files in directory"""
        directory = Path(directory)
        if not directory.is_dir():
            return []
        
        return list(directory.glob(pattern))


class StringHelper:
    """String utility functions"""
    
    @staticmethod
    def truncate(text: str, length: int = 100) -> str:
        """Truncate text"""
        if len(text) > length:
            return text[:length-3] + "..."
        return text
    
    @staticmethod
    def clean_whitespace(text: str) -> str:
        """Remove extra whitespace"""
        return re.sub(r'\s+', ' ', text).strip()
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text"""
        text = text.lower()
        text = StringHelper.clean_whitespace(text)
        return text
    
    @staticmethod
    def is_empty(text: str) -> bool:
        """Check if text is empty"""
        return not text or not text.strip()


class ValidationHelper:
    """Validation utility functions"""
    
    @staticmethod
    def is_valid_amount(amount: float) -> bool:
        """Validate amount"""
        return isinstance(amount, (int, float)) and amount > 0
    
    @staticmethod
    def is_numeric(text: str) -> bool:
        """Check if text is numeric"""
        try:
            float(text)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        """Check if date format is valid"""
        from datetime import datetime
        
        formats = ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y']
        
        for fmt in formats:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        
        return False


class DataHelper:
    """Data utility functions"""
    
    @staticmethod
    def flatten_dict(data: Dict, parent_key: str = '') -> Dict:
        """Flatten nested dictionary"""
        items = []
        
        for k, v in data.items():
            new_key = f"{parent_key}_{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(DataHelper.flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        
        return dict(items)
    
    @staticmethod
    def remove_empty_values(data: Dict) -> Dict:
        """Remove empty values from dictionary"""
        return {k: v for k, v in data.items() if v or v == 0}