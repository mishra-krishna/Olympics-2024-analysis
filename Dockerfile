FROM python:3.11-slim

COPY . /app


WORKDIR /app


RUN pip install --no-cache-dir -r requirements.txt

CMD streamlit run app.py