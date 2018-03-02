FROM tiangolo/uwsgi-nginx-flask:python3.6

# Set up environment variables
ENV SIERRA_ENV=PROD

# Create directory where source is pulled
RUN mkdir -p /source
WORKDIR /source

# Clone repo for e-mini source data for sierra
RUN git clone https://github.com/robster970/e-mini.git

# Clone ES repo for latest update of ES
RUN git clone https://github.com/robster970/ES.git

# Set up main app directory and environment variable
WORKDIR /app
RUN mkdir -p /app/.sierra_data

# Copy main application into /app directory
RUN cp -rp /source/ES/* .

# Change directory and install Python dependencies
RUN pip install -r requirements.txt

# Run it!
CMD [ "python", "./main.py" ]
