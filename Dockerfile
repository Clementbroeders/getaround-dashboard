FROM continuumio/miniconda3

WORKDIR /home/app

# Install Python Dependencies
COPY requirements.txt /home/app
RUN pip install --no-cache-dir -r requirements.txt

# Send file to container
COPY . /home/app/

# Set the default value for the environment variable
ENV PORT=8501

# Run the Streamlit app
CMD streamlit run --server.port $PORT app.py