FROM python:3.10-slim
COPY . ./app
WORKDIR /app/models
ADD https://drive.google.com/uc?export=download&id=1cXQdWRMbuMqcxWwwifP7tK6GuYWuSPd0 products.csv
ADD https://drive.google.com/uc?export=download&id=1JuSJa9EJmCfj7pUYvVi6j5BGMmpZB6Pd encoder_1.pt
ADD https://drive.google.com/uc?export=download&id=1vVlg4U2hdUqvaD2hu0aNbXzCLYNFd4BR /decoder/decoder_00
ADD https://drive.google.com/uc?export=download&id=1RyXoqGdPU3WaKzzeu0s2Z9FaLe4HiMoj /decoder/decoder_01
ADD https://drive.google.com/uc?export=download&id=13Npbiv2SxBtLjx5bbJm4xv67nitYjpvi /decoder/decoder_02
ADD https://drive.google.com/uc?export=download&id=1hTN8nRgsuBUsOrJXky9Kgc-uocoDu-Fc users_baskets.parquet
ADD https://drive.google.com/uc?export=download&id=1bSrkP9SkCTGOmTC4u0HoE0GN9llqCMtL product_to_id.pickle
ADD https://drive.google.com/uc?export=download&id=1hC6HQTmKA04Olv5c20u9eejZSmMb1O_O user_to_id.pickle
ADD https://drive.google.com/uc?export=download&id=1sWNqKU-kJtJ4YacqEu0BmOY4JYJ2wXs2 id_to_product.pickle
ADD https://drive.google.com/uc?export=download&id=1Nx5UmUOZenLZCiTKbAYLous6A8BMxOS5 top_product.pickle
RUN apt-get update && apt-get full-upgrade -y && apt-get install gcc -y 
RUN apt-get install unzip
RUN cat /decoder/* > decoder.zip && unzip decoder.zip decoder_1.pt
WORKDIR /
RUN pip install wheel setuptools pip --upgrade && pip install -r /app/requirements.txt
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
