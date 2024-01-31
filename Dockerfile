FROM python:3.9-alpine3.16

WORKDIR /app
COPY requirements.txt /temp/requirements.txt
COPY app /app
RUN pip install --upgrade pip && pip install -r /temp/requirements.txt

CMD ["python", "bot.py"]
