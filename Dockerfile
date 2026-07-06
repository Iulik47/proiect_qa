# 1. Folosim o versiune oficială și ușoară de Python
FROM python:3.12-slim

# 2. Setăm folderul de lucru în interiorul containerului
WORKDIR /app

# 3. Copiem fișierul de cerințe și instalăm librăria
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Instalăm Playwright și absolut toate dependențele de Linux necesare pentru browser
RUN playwright install --with-deps chromium

# 5. Copiem restul codului (scriptul tău)
COPY . .

# 6. Comanda finală pe care o dă serverul când pornește containerul
CMD ["python", "test_login.py"]