FROM python:3.11-slim


WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY ./app /app/app
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic


EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]