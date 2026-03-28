# OCR Invoice Data Extraction
**Authors:** Harsmitha K & Jahnavi K L  
**Stack:** FastAPI · React · Tesseract OCR · OpenPyXL

---

## Quick Start

### 1. Install System Dependencies (once)
**Windows:**
- Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Poppler: https://github.com/oschwartz10612/poppler-windows/releases → extract to C:\poppler\ → add C:\poppler\Library\bin to PATH

### 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
Server runs at: http://127.0.0.1:8000

### 3. Option A — Excel Portal (No Node.js needed)
Double-click `invoice-portal.html` in your browser.
- Upload invoice → Extract → Download .xlsx

### 4. Option B — React Frontend
```bash
cd frontend
npm install
npm run dev
```
Open: http://localhost:3000

---

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /extract | Upload invoice, returns JSON |
| GET | /download/xlsx/{name} | Download Excel file |
| GET | /download/csv/{name} | Download CSV file |
| GET | /download/json/{name} | Download JSON file |
| GET | /health | Health check |

---

## Fields Extracted
- Invoice Number, Invoice Date
- Vendor Name, Customer Name
- Subtotal, Tax Amount, Total Amount
- Validation status

## Troubleshooting
- `TesseractNotFoundError` → Install Tesseract and add to PATH
- PDF fails → Install Poppler and add to PATH
- `No module named fastapi` → Activate venv first: `venv\Scripts\activate`
