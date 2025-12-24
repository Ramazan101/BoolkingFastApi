FROM python:3.12

WORKDIR /app

COPY req.txt .
RUN pip install --upgrade pip && pip install -r req.txt

COPY . .
