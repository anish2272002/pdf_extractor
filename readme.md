# 📄 PDF Page Extractor (Django + Next.js)

A full-stack application that allows users to:

- Upload a PDF
- Visually select the pages they want
- Download a new PDF with only those selected pages

Built with:

- 🐍 Django + Django REST Framework (Backend)
- ⚛️ Next.js 14 (Frontend with App Router)
- 📚 PyPDF2 for PDF processing
- 📘 pdf.js for PDF preview

---

## 🚀 Features

- Upload any PDF file
- Preview pages in-browser
- Select multiple pages visually
- Generate and download new PDF instantly
- Fully async and API-based

---

## 🧱 Tech Stack

| Layer    | Tool                                   |
| -------- | -------------------------------------- |
| Backend  | Django, DRF, PyPDF2                    |
| Frontend | Next.js 14 (App Router), Axios, pdf.js |
| Preview  | `pdfjs-dist` (local worker)            |
| Styling  | Basic CSS (customizable)               |

---

## 📦 Installation

### 1. Backend Setup

```bash
cd backend/
python3 -m venv penv
source penv/bin/activate
pip install -r requirements.txt
python manage.py runserver
curl -X POST http://localhost:8000/api/process/ \
  -F "pdf=@example.pdf" \
  -F "pages=1,3,4" \
  --output extracted.pdf
```

### 1. Frontend Setup

```bash
cd frontend/
npm install
npm run dev
```
