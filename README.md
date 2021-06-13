# Security Bot

## Hardware environment
- Raspberry Pi 4 Model B
- [Raspberry Pi Camare Module V2 8MP](https://ricelee.com/product/camera-module-v2)
## Software environment
- Python 3.6.9
- OpenCV 3.4.1
- Tensorflow latest
## Deploy
sudo docker build . -t CV-bot
## Run
sudo docker run --device=/dev/vchiq --device=/dev/video0 --net=host -p 3000:3000 -it <Docker Image ID> 
