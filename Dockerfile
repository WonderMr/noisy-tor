FROM python:3.10.8-slim-bullseye
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /
ENTRYPOINT ["python", "noisy.py", "update.py"]
CMD ["--config", "config.json"]
