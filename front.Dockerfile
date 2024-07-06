FROM python:3.10-slim
WORKDIR /app
COPY  /frontend/ /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0", "--reload"]