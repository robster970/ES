FROM tiangolo/uwsgi-nginx-flask:python3.6

# Set up environment variables
ENV SIERRA_ENV=PROD
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create directory where source is pulled
RUN mkdir -p /source
WORKDIR /source

# Clone ES repo for latest update of ES
RUN git clone https://github.com/robster970/ES.git

# Change directory and install Python dependencies
WORKDIR /source/ES
RUN pip install -r requirements.txt

# Clone repo for e-mini source data for sierra
WORKDIR /source
RUN git clone https://github.com/robster970/e-mini.git

# Set up main app directory
WORKDIR /app
RUN mkdir -p /app/.sierra_data

# Copy main application into /app directory
RUN cp -rp /source/ES/* .

# Run it!
CMD [ "python", "./main.py" ]
