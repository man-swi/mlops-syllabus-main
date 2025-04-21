
# Docker CLI basic usage
## Containers
```
docker pull nginx

# Run an nginx container in detached mode
docker run -d --name my-nginx-container nginx

# See logs from the nginx container 
docker logs my-nginx-container

# Execute a command in the running nginx container
docker exec -it my-nginx-container /bin/bash

# Stop the nginx container
docker stop my-nginx-container  

# Remove the nginx container 
docker rm my-nginx-container

# List all nginx images on the host
docker images nginx

# Inspect metadata for the nginx image
docker inspect nginx
```


## Docker Registry
### Local Registry
```
# Start a local registry
docker run -d -p 5000:5000 --restart=always --name registry registry:2

# Pull an image from Docker Hub
docker pull nginx

# Re-tag the image to point to your local registry 
docker tag nginx:latest localhost:5000/nginx:latest

# Push the re-tagged image to your local registry
docker push localhost:5000/nginx:latest

# Pull the image from your local registry
docker pull localhost:5000/nginx:latest

# Run a container from the image pulled from local registry
docker run -d --name nginx-local localhost:5000/nginx:latest
```

### DockerHub
```
# Login to Docker Hub
docker login

# Pull an image from Docker Hub
docker pull nginx

# Tag an image to push to your Docker Hub repository
docker tag nginx:latest your-dockerhub-username/nginx:latest

# Push the tagged image to your Docker Hub repository
docker push your-dockerhub-username/nginx:latest

# Pull an image from your Docker Hub repository
docker pull your-dockerhub-username/nginx:latest

# Run a container from the image pulled from your Docker Hub repository
docker run -d --name nginx-hub your-dockerhub-username/nginx:latest
```

## Docker Networking

```
# List all networks on the Docker host
docker network ls

# Inspect a specific network
docker network inspect <NETWORK_ID>

# Create a new bridge network
docker network create --driver bridge my-bridge-network

# Create a new overlay network 
docker network create --driver overlay --attachable my-overlay-network

# Use host network

  docker run --rm --network host nginx
  
# Run a container and connect it to a specific network
docker run -d --name nginx --network my-bridge-network nginx

# Connect an existing container to a network
docker network connect my-overlay-network nginx

# Disconnect a container from a network
docker network disconnect my-overlay-network nginx

# Remove a network
docker network rm my-bridge-network
```

## Docker image build
```
# Show Available images
docker image ls

# Docker build image from a Dockerfile
docker build -t <DockerImageTag> -f <DockerfileName> .

# Show the history of an image
docker history <Image-ID/ImageName> 

# Show Running Containers
docker ps

# Docker Run with Port Forwarding
docker run -d -p 8000:8000 --name <ContainerName> <ImageName>
```
## Docker Compose

```
# Build or rebuild services
docker compose build

# Create and start containers
docker compose up 

# Stop and remove containers, networks
docker compose down

# Create & start containers with Watch (Watch source code and rebuild/refresh containers when files are updated.)
docker compose up --watch
```