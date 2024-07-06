FROM python:3.10-slim
WORKDIR /app
COPY  /backend/ /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0" ,"--reload"]