# Build image
docker build -t getaround-streamlit .

# Run container
docker run -it -v "$(pwd):/home/app" -p 8501:8501 getaround-streamlit