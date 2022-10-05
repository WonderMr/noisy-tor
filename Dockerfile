FROM python:3.8-alpine3.13
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /
ENTRYPOINT ["python", "noisy.py", "update.py"]
CMD ["--config", "config.json"]
