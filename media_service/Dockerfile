FROM python:3.12

WORKDIR /app

COPY media_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY media_service/ .
COPY shared/ shared/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]