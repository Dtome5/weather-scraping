FROM python:3.12-slim

# Set up environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && \
    apt-get install -y cron
# Install system dependencies
RUN pip install uv

WORKDIR /app
# Copy requirements file
COPY ./pyproject.toml ./

# Install dependencies using UV
RUN uv sync

# Copy script files
COPY *.py ./
COPY run.sh ./
COPY websites.csv ./

# Create an empty weather.hdf5 file to ensure it exists when viz.py is first run

# Create cron job

RUN echo "0 12 * * * /path/to/run.sh" | crontab -

# Create log file for cron
RUN touch /var/log/cron.log

# Create an entrypoint script that starts cron and tails the log

# Command to run the scriptmg

CMD ["uv", "run", "launch.py"]
# Run entrypoint script

