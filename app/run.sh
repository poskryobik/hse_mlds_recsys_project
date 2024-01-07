docker container stop api_app
docker container rm api_app
docker build -t api_app -f Dockerfile .
sleep 3
docker run -d --network host --restart=always --name api_app api_app
