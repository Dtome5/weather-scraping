import subprocess
import time
import os
import signal

# Set environment variables for consistent port configuration
os.environ["PREFECT_API_URL"] = "http://127.0.0.1:4200/api"

# Start Prefect server with specific host and port
server_process = subprocess.Popen(
    ["prefect", "server", "start", "--host", "127.0.0.1", "--port", "4200"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Wait for server to initialize
print("Waiting for Prefect server to start...")
time.sleep(10)  # Give the server time to fully start

try:
    # Run your schedule script
    print("Running schedule script...")
    subprocess.run(["uv","run", "./schedule.py"], check=True)

    # Run the deployment
    print("Starting deployment...")
    subprocess.run(["prefect", "deployment", "run", "schedule/myflow"], check=True)

    # Keep the main process running to maintain the server
    print("Services started. Press Ctrl+C to stop.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Shutting down...")
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    # Clean up processes
    if server_process:
        print("Stopping Prefect server...")
        server_process.terminate()
        server_process.wait(timeout=5)
