FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.req
CMD ["python", "scrap.py"]
