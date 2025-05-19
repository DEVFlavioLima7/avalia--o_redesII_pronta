FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install -y iproute2 iputils-ping net-tools && \
    echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

CMD ["python", "router.py"]
