FROM python:3

# Set up main directory and environment variable
RUN mkdir /app
WORKDIR /app
ENV SIERRA_ENV=PROD

# Clone repo for e-mini source data for sierra
RUN git clone https://github.com/robster970/e-mini.git

# Clone ES repo for latest update
RUN git clone https://github.com/robster970/ES.git

# Change directory and install Python dependencies
WORKDIR ES
RUN pip install -r requirements.txt

# Run it!
CMD [ "python", "./sierra_web.py" ]
