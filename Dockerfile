FROM alpine:3.18

# Install Python and other dependencies
RUN apk add --no-cache python3 py3-pip gcc musl-dev python3-dev libffi-dev openssl-dev \
    geos geos-dev

# Set the working directory
WORKDIR /app

# Copy the application code to the working directory
COPY . .

# Ensure requirements.txt is present
RUN ls -l /app

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Mount the credentials secret
VOLUME /app/credentials

# Set the environment variable to point to the mounted secret path
ENV GOOGLE_APPLICATION_CREDENTIALS=./gen-lang-client-0103422251-0e5b41436c77.json
ENV access_token=./access_token.json

ENV host="72.52.176.216"
ENV user="rewardola__cms_admin"
ENV password="q{k25mgx&DKu"
ENV database="rewardola__cms_admin"   
# Expose the port that the application listens on
EXPOSE 8000

# Run the application
CMD chainlit run app.py -w