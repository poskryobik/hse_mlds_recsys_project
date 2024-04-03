FROM python:3.10-slim
COPY . ./app
WORKDIR /app
ADD https://drive.google.com/uc?export=download&id=1cXQdWRMbuMqcxWwwifP7tK6GuYWuSPd0 /app/products.csv
ADD https://drive.google.com/uc?export=download&id=1ZTHS47w0zVPpTJbygNDnawIYP0wdaJnL /app/zip_ratings/ratings_zip_piece_00
ADD https://drive.google.com/uc?export=download&id=1Irt-M9HHtxotEHpk4zzbxb0XWtjfU1JQ /app/zip_ratings/ratings_zip_piece_01
ADD https://drive.google.com/uc?export=download&id=13IlM0SvS4eD9cDVWjanUT5sYWm9xr7ro /app/zip_ratings/ratings_zip_piece_02
ADD https://drive.google.com/uc?export=download&id=1eodl9OlaYy3NTu9TpbtPLHNurXxeHlhh /app/models/encoder.pkl
ADD https://drive.google.com/uc?export=download&id=1-KTrXZV35DXB0sdzSxjxAlqkfloepE6r /app/models/lfm_model.pkl
RUN apt-get update && apt-get full-upgrade -y && apt-get install gcc -y 
RUN apt-get install unzip
RUN cat zip_ratings/* > ratings.zip && unzip ratings.zip
RUN pip install wheel setuptools pip --upgrade && pip install -r requirements.txt
WORKDIR /
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
