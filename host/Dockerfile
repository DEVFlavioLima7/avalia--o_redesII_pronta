FROM python:3.9-slim

RUN apt-get update && apt-get install -y iputils-ping net-tools iproute2

WORKDIR /app

COPY host.py .

CMD ["python3", "host.py"]
