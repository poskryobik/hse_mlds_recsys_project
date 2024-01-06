FROM python:3.10-slim
COPY . ./app
WORKDIR /app
ADD https://drive.google.com/uc?export=download&id=1cXQdWRMbuMqcxWwwifP7tK6GuYWuSPd0 /app/products.csv
ADD https://drive.google.com/uc?export=download&id=1epGrpzB8BEC2t5Od3hrL3x07B1VZIm3c /app/ratings.csv
ADD https://drive.google.com/uc?export=download&id=1eodl9OlaYy3NTu9TpbtPLHNurXxeHlhh /app/encoder.pkl
ADD https://drive.google.com/uc?export=download&id=1-KTrXZV35DXB0sdzSxjxAlqkfloepE6r /app/lfm_model.pkl
RUN apt-get update && apt-get full-upgrade -y && apt-get install gcc -y
RUN pip install wheel setuptools pip --upgrade && pip install -r requirements.txt
CMD ["python", "bot.py", "YOUR_TOKEN"]
