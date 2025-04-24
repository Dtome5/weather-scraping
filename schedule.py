from datetime import datetime
import subprocess
from prefect import flow, task
from extract import load
from viz import plot_locs, plot_vals, dataframes,show

@task()
def load_process():
    load()
@task()
def plot():
    plot_locs(dataframes)
    plot_vals(dataframes)
    show()
@flow()
def schedule():
    load_process()
    plot()
   


if __name__ == "__main__":
    schedule.serve(name="myflow", cron="* * * * *")
