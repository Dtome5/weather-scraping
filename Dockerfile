FROM python:3.12-slim

# Set up environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN pip install uv


# Create and set working directory
WORKDIR /app

# Copy requirements file
COPY ./pyproject.toml .

# Install dependencies using UV
RUN uv sync

# Copy script files
COPY extract.py .
COPY viz.py .
COPY run.sh .
COPY websites.csv .

# Create an empty weather.hdf5 file to ensure it exists when viz.py is first run
RUN touch weather.hdf5

# Create cron job

RUN echo "0 12 * * * \n run.sh "| crontab -e

# Create log file for cron
RUN touch /var/log/cron.log

# Create an entrypoint script that starts cron and tails the log
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'crond -f -l 8 &' >> /entrypoint.sh && \
    echo 'tail -f /var/log/cron.log' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh
# Create a volume for persistent storage

# Command to run the script
CMD ["uv", "run", "extract.py"]
# Run entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
