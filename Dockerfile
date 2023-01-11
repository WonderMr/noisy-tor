FROM python:3.12.0a3-slim-bullseye
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /
ENTRYPOINT ["python", "noisy.py", "update.py"]
CMD ["--config", "config.json"]
