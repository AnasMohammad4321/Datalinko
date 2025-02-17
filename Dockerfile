FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8060

ENV FLASK_ENV=development

# Command to run the application
CMD ["python", "wsgi.py"]
