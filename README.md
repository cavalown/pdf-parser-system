# pdf-parser-system

Parse PDF files and preview extracted content.

## Project structure

```txt
pdf-parser-system/
  frontend/   React + Vite frontend
  backend/    Python FastAPI server
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Default local URL:

```txt
http://localhost:5173
```

Build check:

```bash
cd frontend
npm run build
```

## Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Default local URL:

```txt
http://localhost:3000
```

Health check:

```txt
http://localhost:3000/api/health
```

API docs (Swagger UI):

```txt
http://localhost:3000/docs
```
