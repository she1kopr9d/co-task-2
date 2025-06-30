FROM python:3.12

WORKDIR /app

COPY frontend_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend_service/ .
COPY shared/ shared/

RUN python manage.py collectstatic --noinput --clear

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]