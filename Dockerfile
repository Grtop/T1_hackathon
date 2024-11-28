FROM python:3.10-slim
RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

RUN mkdir -p /app/good_files /app/uploads

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["./start.sh"]