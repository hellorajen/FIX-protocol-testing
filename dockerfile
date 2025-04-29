FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install simplefix
CMD ["python", "fix_server.py"]