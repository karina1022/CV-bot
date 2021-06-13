# Security Bot

## Hardware environment

## Software environment

## Deploy
sudo docker build . -t CV-bot
## Run
sudo docker run --device=/dev/vchiq --device=/dev/video0 --net=host -p 3000:3000 -it <Docker Image ID> 
