FROM python:3.13-slim

WORKDIR /app

RUN pip install flask requests

COPY . /app

EXPOSE 3000

CMD ["python", "app.py"]