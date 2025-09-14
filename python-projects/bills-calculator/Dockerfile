FROM python:3.12-slim

# Prevent Python from writing .pyc files / buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Workdir inside the image
WORKDIR /app

# Install app deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app
COPY . .

# run as non-root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Your app listens on 5000
EXPOSE 5000

# Use Gunicorn in containers (not the Flask dev server)
CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "8", "-b", "0.0.0.0:5000", "app:app"]
