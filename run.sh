#/bin/bash  

# load the environment variables
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

# Run the microservice
sudo docker run  -p 5000:5000 -v .:/app --name ai-microservice ai-microservice