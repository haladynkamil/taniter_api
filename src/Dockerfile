FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "src.app.main:app", "--reload", "--workers", "8", "--host", "0.0.0.0", "--port", "8008"]

ENV PYTHONPATH /