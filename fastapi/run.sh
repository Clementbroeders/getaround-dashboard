# Build image
docker build -t fastapi .

# Run container
docker run -it -v "$(pwd):/home/app" -p 4000:4000 fastapi