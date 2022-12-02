FROM python:3.9-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY explorer explorer/
COPY run.py .

CMD ["python3", "./run.py"]
