FROM python:3.12.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
