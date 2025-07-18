# 1. Use official Python image (slim version for smaller size)
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements (for caching pip install)
COPY requirement.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# 5. Copy application code
COPY . .

# 6. Set environment variable for Flask (optional)
ENV FLASK_APP=api_services.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 7. Expose port (default Flask port)
EXPOSE 8080

# 8. Run the app (using flask CLI or gunicorn for production)
# If you use Flask's development server:
# CMD ["flask", "run"]

# For production, use gunicorn (recommended)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
