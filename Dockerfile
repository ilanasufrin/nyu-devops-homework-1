# Start with a Linux micro-container to keep the image tiny
FROM alpine:latest

# Document who is responsible for this image
MAINTAINER Mohammad Afshar "ma2510@nyu.edu"

# Install just the Python runtime (no dev)
RUN apk add --update \
    python \
    py-pip \
 && rm -rf /var/cache/apk/*

# Expose any ports the app is expecting in the environment
ENV PORT 5000
EXPOSE $PORT

# Set up a working folder and install the pre-reqs
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

# Add the code as the last Docker layer because it changes the most
COPY icecream.py /app

# Run the service
CMD [ "python", "icecream.py" ]
