FROM python:3.10-slim
COPY . ./bot
WORKDIR /bot
RUN apt-get update && apt-get full-upgrade -y && apt-get install gcc -y 
RUN pip install wheel setuptools pip --upgrade && pip install -r requirements.txt
WORKDIR /
# CMD ["python", "bot/main.py"]