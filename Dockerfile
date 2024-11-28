FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y wget && \
    wget https://www.rarlab.com/rar/rarlinux-x64-6.0.2.tar.gz && \
    tar -xzf rarlinux-x64-6.0.2.tar.gz && \
    cd rar && \
    cp -v rar unrar /usr/local/bin/ && \
    rm -rf /rarlinux-x64-6.0.2.tar.gz /rar && \
    apt-get remove -y wget && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

RUN mkdir -p /app/good_files /app/uploads

COPY start.sh /app
RUN chmod +x /app/start.sh

CMD ["bash", "/app/start.sh"]

