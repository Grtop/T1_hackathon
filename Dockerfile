FROM python:3.10-slim

# RUN apt-get update && \
#     apt-get install -y software-properties-common && \
#     apt-add-repository non-free && \
#     apt-get update && \
#     apt-get install -y rar unrar && \
#     rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

RUN mkdir -p /app/good_files /app/uploads

COPY start.sh /app
RUN chmod +x /app/start.sh

CMD ["bash", "/app/start.sh"]

