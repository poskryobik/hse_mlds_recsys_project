FROM python:3.10-slim
COPY . ./app
WORKDIR /app
RUN apt-get update && apt-get full-upgrade -y && apt-get install gcc -y 
RUN pip install wheel setuptools pip --upgrade && pip install -r requirements.txt
# CMD ["python", "bot.py", "YOUR_TOKEN"]