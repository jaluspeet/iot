FROM python:3

COPY client/ .

RUN pip3 install --no-cache-dir -r requirements.txt || true

CMD ["python3", "app.py"]
