FROM python:3.9
ENV PYTHONUNBUFFERED 1
COPY requirements.txt ./
RUN pip install --user -r requirements.txt
COPY . app
COPY run_server.sh ./
RUN chmod +x run_server.sh
EXPOSE 8000
ENTRYPOINT ["./run_server.sh"]
