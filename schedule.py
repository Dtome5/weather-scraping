from datetime import datetime
import subprocess
from prefect import flow, task
from extract import load
from viz import show,make_plots

@task()
def load_process():
    load()
@task()
def plot():
    make_plots()
    show()
@flow()
def schedule():
    load_process()
    plot()

if __name__ == "__main__":
    schedule.serve(name="myflow", cron="* * * * *")
