FROM python:3.9

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]