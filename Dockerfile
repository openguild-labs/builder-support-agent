# Use the official Python image from Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy the rest of the application code into the container
COPY . .

# Set the environment variables
ENV GOOGLE_AI_KEY=${GOOGLE_AI_KEY}
ENV DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
ENV MAX_HISTORY=${MAX_HISTORY}
ENV GITHUB=${GITHUB}
ENV PORT=8080

# Create a cron job file
RUN echo "0 */6 * * * python3 /app/crawl.py >> /var/log/cron.log 2>&1" > /etc/cron.d/crawl_job

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crawl_job
RUN crontab /etc/cron.d/crawl_job

# Start cron and the main application
CMD cron && tail -f /var/log/cron.log
