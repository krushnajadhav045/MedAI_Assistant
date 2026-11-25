# MediGrid — Medical Prescription Extraction & AI Assistant

## Overview

**MediGrid** is a FastAPI-powered medical document intelligence application that extracts structured patient and medication details from prescription images using **Google Gemini (`gemini-2.5-flash`)**, enriches entries with nearby pharmacy **Google Maps** links based on user coordinates, checks critical medication warnings, persists records into **SQLite (`MediGrid.db`)**, and provides an interactive medical chat assistant.

> **Security Note:** Never commit your real `GEMINI_API_KEY` to GitHub or public files. Store it locally in a `.env` file listed in `.gitignore` and rotate any key that has been exposed.

## Key Features

* **Prescription Image OCR & Entity Extraction:** Uses `Handwritting_Extraction` (`Extracting_prescription_data.py`) with `Pillow` image resizing and `google-generativeai` (`gemini-2.5-flash`) to parse handwritten/printed prescriptions into structured JSON (`patient_info` and `Prescription_info`).

* **Nearby Pharmacy Map Links:** Generates Google Maps pharmacy search URLs from latitude and longitude coordinates via `location.py`.

* **Critical Warning Analysis:** Evaluates extracted prescription medications via `/critical_warnings` (`Critical_Warinings.py`).

* **SQLite Persistence & Inspection:** Saves prescription entries with timestamps into `MediGrid.db` (`SQLLITE3_DataBase.py`) and formats grouped records using `pandas`, with a CLI inspection utility (`check_database.py`).

* **AI Medical Chat Assistant:** Provides conversational support via `/chat` (`AI_assistant_logic.py`).

* **Static Web Frontend:** Serves `static/test1.html` at `/` and mounts `/static` assets with CORS enabled.

## Architecture & Pipeline

```text
Client / Browser (static/test1.html)
   │
   ├── GET /                     ──▶ Serves static/test1.html
   │
   ├── POST /data_extraction     ──▶ Extracting_prescription_data.py + location.py
   │                                  • Resizes image (Pillow) & runs gemini-2.5-flash OCR
   │                                  • Attaches Google Maps nearby pharmacy link
   │                                  • Returns structured patient_info & Prescription_info JSON
   │
   ├── POST /critical_warnings   ──▶ Critical_Warinings.py
   │                                  • Analyzes extracted medications for critical warnings
   │
   ├── POST /post_into_db        ──▶ SQLLITE3_DataBase.py ──▶ Inserts into MediGrid.db
   ├── GET  /get_Saved_data      ──▶ SQLLITE3_DataBase.py ──▶ Reads Prescription table
   │
   └── POST /chat                ──▶ AI_assistant_logic.py (MedicalAssistant)
```

## Project Structure

```text
.
├── fast_api_file.py                  # FastAPI app, routes, CORS & static file mounting
├── Extracting_prescription_data.py   # Gemini 2.5 Flash prescription OCR & JSON extraction
├── location.py                       # Generates Google Maps nearby pharmacy search URLs
├── SQLLITE3_DataBase.py              # SQLite (MediGrid.db) table creation, insert & display logic
├── check_database.py                 # CLI script to inspect saved rows in MediGrid.db
├── Critical_Warinings.py             # Critical medication warning analyzer
├── AI_assistant_logic.py             # MedicalAssistant conversational logic
├── static/
│   └── test1.html                    # Frontend interface served at /
├── MediGrid.db                       # SQLite database storing Prescription records
├── requirements_2.txt                # Python dependencies
├── How to run.txt                    # Uvicorn startup command reference
└── .env                              # Environment variables (GEMINI_API_KEY; keep out of Git)
```

## Installation

### 1. Create and activate a virtual environment

```bash
python -m venv .venv

# Linux / macOS:
source .venv/bin/activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Windows (Command Prompt):
.venv\Scripts\activate.bat
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements_2.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root (keep `.env` in `.gitignore`):

```env
GEMINI_API_KEY="your_gemini_api_key_here"
```

## Running the Application

Start the FastAPI server using the command in `How to run.txt`:

```bash
python -m uvicorn fast_api_file:api --reload --reload-exclude "*.db"
```

* **Frontend UI:** `http://127.0.0.1:8000/`

* **Interactive API Docs (Swagger UI):** `http://127.0.0.1:8000/docs`

### Inspect Saved Database Records via CLI

```bash
python check_database.py
```

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves `static/test1.html`. |
| `POST` | `/data_extraction` | Accepts multipart `image` file and optional JSON string `user_location` (`{"latitude": ..., "longitude": ...}`), returning extracted `patient_info` and `Prescription_info`. |
| `POST` | `/critical_warnings` | Accepts `{"Prescription_info": [...]}` and returns critical warning analysis. |
| `POST` | `/post_into_db` | Saves extracted `patient_info` and `Prescription_info` records into `MediGrid.db`. |
| `GET` | `/get_Saved_data` | Retrieves saved rows from the `Prescription` table ordered by `Data_Saved DESC`. |
| `POST` | `/chat` | Accepts `{"message": "..."}` and returns `{"response": "..."}` from `MedicalAssistant`. |

## Database Schema (`MediGrid.db`)

Table: **`Prescription`**

| Column | Type | Description |
| :--- | :--- | :--- |
| `PATIENT_NAME` | `TEXT` | Extracted patient name (defaults to `Unknown_Patient`) |
| `MEDICATION_NAME` | `TEXT` | Prescribed medicine name |
| `DOSAGE` | `TEXT` | Dosage instructions (e.g., `50mg`, `400mg`) |
| `FREQUENCY` | `TEXT` | Schedule and meal timings (e.g., `1-0-1 (after meals)`) |
| `DURATION` | `TEXT` | Treatment duration (e.g., `5 days`) |
| `MAP_LINK` | `TEXT` | Google Maps nearby pharmacy search link |
| `Data_Saved` | `DATETIME` | Timestamp when the record was saved (`YYYY-MM-DD HH:MM:SS`) |

## Dependencies (`requirements_2.txt`)

```text
google-generativeai
python-dotenv
pdfplumber
Pillow
fastapi
fastapi[standard]
uvicorn
pydantic
pandas
```

## Disclaimer & License

* **Medical Disclaimer:** This software is intended for data extraction and educational/prototype purposes only and does not provide professional medical advice.

* **License:** Add a `LICENSE` file to specify your license terms for this repository.

---

⭐ Always learning, building projects, and exploring new technologies in Data Science, Data Analytics, and AI.

## 🌐 Socials:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/your-linkedin-username)
[![Email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white)](mailto:your-email@example.com)

## 💻 Tech Stack:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

## 📊 GitHub Stats:

![krushnajadhav045's GitHub Stats](https://github-readme-stats.vercel.app/api?username=krushnajadhav045&show_icons=true&hide_border=true)
