docker container stop api_app
docker container rm api_app
docker build -t api_app -f Dockerfile .
sleep 3
docker run -d --name api_app -p 8000:80 api_app
