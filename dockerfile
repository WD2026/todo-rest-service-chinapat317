FROM python:3.11.14-slim
WORKDIR /user/src/app
COPY ./src .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]