FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils && \
    pip install --no-cache-dir -r requirements.txt || true
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt || true
CMD ["python3", "encriptacion.py"]
