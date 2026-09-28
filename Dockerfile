# 1. Folosim o versiune oficială și ușoară de Python
FROM python:3.12-slim

# 2. Setăm folderul de lucru în interiorul containerului
WORKDIR /app

# 3. Copiem fișierul de cerințe și instalăm librăriile (pytest, playwright...)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Instalăm Playwright și absolut toate dependențele de Linux necesare pentru browser
RUN playwright install --with-deps chromium

# 5. Copiem restul codului (scriptul tău)
COPY . .

# 6. Comanda finală: rulăm suita și salvăm raportul HTML în /app/reports
CMD ["pytest", "test_suite.py", "--html=reports/raport_final.html", "--self-contained-html"]