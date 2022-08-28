FROM python:3.10.0a6-alpine3.13
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /
ENTRYPOINT ["python", "noisy.py", "update.py"]
CMD ["--config", "config.json"]
