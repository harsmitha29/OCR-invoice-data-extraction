# OCR Invoice Data Extraction

**Authors:** Harsmitha K & Jahnavi K L  
**Internship:** TechTheos — 2026  
**Stack:** FastAPI (Python) · React + TypeScript + Tailwind CSS · Tesseract OCR

---

## Project Structure

```
ocr-invoice-app/
├── backend/                  # FastAPI Python backend
│   ├── main.py               # FastAPI app entry point
│   ├── requirements.txt      # Python dependencies
│   ├── src/
│   │   ├── input_handler.py      # File validation & PDF→image conversion
│   │   ├── preprocessing.py      # OpenCV image enhancement
│   │   ├── ocr_engine.py         # Tesseract OCR wrapper
│   │   ├── text_processor.py     # Date/currency parsing
│   │   ├── field_extractor.py    # Regex-based field extraction
│   │   ├── validator.py          # Data validation rules
│   │   ├── output_generator.py   # JSON & CSV export
│   │   └── utils/
│   │       ├── logger.py         # Logging setup
│   │       └── helpers.py        # Shared utilities
│   └── output/               # Generated JSON/CSV files (auto-created)
│
└── frontend/                 # React + Vite frontend
    ├── src/
    │   ├── App.tsx
    │   ├── components/
    │   │   ├── Header.tsx
    │   │   ├── UploadZone.tsx    # Drag-and-drop upload
    │   │   └── ResultsPanel.tsx  # Extracted data display + downloads
    │   ├── hooks/
    │   │   └── useApi.ts         # Axios API calls
    │   └── types/
    │       └── invoice.ts        # TypeScript interfaces
    └── index.html
```

---

## Prerequisites

### System
- Python 3.9+
- Node.js 18+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on system
  - **Ubuntu/Debian:** `sudo apt install tesseract-ocr`
  - **macOS:** `brew install tesseract`
  - **Windows:** Download installer from the GitHub releases page
- **poppler** (for PDF→image conversion):
  - **Ubuntu/Debian:** `sudo apt install poppler-utils`
  - **macOS:** `brew install poppler`
  - **Windows:** Download poppler binaries and add to PATH

---

## Setup & Run

### 1. Backend

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: http://localhost:8000  
Interactive API docs: http://localhost:8000/docs

---

### 2. Frontend

```bash
cd frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

---

## How It Works

1. **Upload** — User drags and drops or selects an invoice (PDF or image) in the React UI.
2. **Transfer** — React sends the file to `POST /api/extract` via FormData.
3. **OCR Pipeline** (FastAPI):
   - `InputHandler` validates and converts PDF pages to PIL images.
   - `ImagePreprocessor` enhances image quality (grayscale, threshold, denoise, skew correct).
   - `OCREngine` runs Tesseract and returns raw text + confidence score.
   - `FieldExtractor` applies regex patterns to pull structured fields.
   - `InvoiceValidator` checks required fields.
4. **Results** — Extracted JSON is returned to React and rendered as a clean summary card.
5. **Download** — User can download output as JSON or CSV via `GET /api/download/{format}/{name}`.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/extract` | Upload invoice, returns extracted JSON |
| GET | `/download/json/{name}` | Download JSON output |
| GET | `/download/csv/{name}` | Download CSV output |

---

## Fields Extracted

| Field | Description |
|-------|-------------|
| `invoice_number` | Invoice / bill reference number |
| `invoice_date` | Date of the invoice |
| `vendor.name` | Supplier / vendor name |
| `customer.name` | Customer / buyer name |
| `subtotal` | Amount before tax |
| `tax` | GST / VAT / tax amount |
| `total` | Grand total amount |
| `validation_passed` | Whether all required fields were found |
| `validation_errors` | List of missing/invalid fields |
| `raw_text` | Full OCR text (for debugging) |

---

## Libraries Used

### Backend
| Library | Purpose |
|---------|---------|
| `fastapi` | Web framework & API |
| `uvicorn` | ASGI server |
| `python-multipart` | File upload support |
| `pytesseract` | Tesseract OCR wrapper |
| `Pillow` | Image handling |
| `opencv-python` | Image preprocessing |
| `pdf2image` | PDF → image conversion |
| `numpy` | Array operations |

### Frontend
| Library | Purpose |
|---------|---------|
| `react` + `typescript` | UI framework |
| `vite` | Build tool / dev server |
| `tailwindcss` | Utility-first CSS |
| `react-dropzone` | Drag-and-drop upload |
| `axios` | HTTP client |
| `react-hot-toast` | Toast notifications |
| `lucide-react` | Icons |

---

## Optional Enhancements (Future Work)

- [ ] EasyOCR as fallback for low-confidence Tesseract results
- [ ] Multi-invoice batch upload
- [ ] Line items table extraction
- [ ] Confidence score visualization per field
- [ ] Export to Excel (`.xlsx`)
- [ ] Docker Compose setup for one-command startup

---

## Troubleshooting

**`TesseractNotFoundError`** — Tesseract is not installed or not in PATH. Install it and ensure `tesseract` is accessible from the terminal.

**PDF extraction fails** — `poppler-utils` is not installed. See prerequisites above.

**CORS error in browser** — Make sure the backend is running on port 8000 and the frontend on port 3000.

**Low extraction accuracy** — Try scanning/photographing the invoice at higher resolution (300 DPI+). Ensure the image is not skewed.
