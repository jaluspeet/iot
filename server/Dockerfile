FROM python:3

COPY server/ .

RUN pip3 install --no-cache-dir -r requirements.txt || true

# open port
EXPOSE 1883

CMD ["python3", "server.py"]
