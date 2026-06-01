# pdf-parser-system

Parse PDF files and preview extracted content.

## Project structure

```txt
pdf-parser-system/
  frontend/   React + Vite frontend
  backend/    NestJS API server
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
npm install
npm run start:dev
```

Default local URL:

```txt
http://localhost:3000
```

Health check:

```txt
http://localhost:3000/api/health
```

Build check:

```bash
cd backend
npm run build
```
