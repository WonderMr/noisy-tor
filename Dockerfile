FROM python:3.12.0rc1-slim-bullseye
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /
ENTRYPOINT ["python", "update.py"]
ENTRYPOINT ["python", "noisy.py"]
CMD ["--config", "config.json"]
