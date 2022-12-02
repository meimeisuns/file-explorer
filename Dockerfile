FROM python:3.9-slim-buster as base

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY explorer explorer/
COPY tests tests/
COPY run.py .

CMD ["python3", "./run.py"]

FROM base as test
CMD ["pytest", "tests"]
