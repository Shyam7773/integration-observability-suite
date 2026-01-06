from prefect import flow, task
from orchestration.run_once import main as run_pipeline

@task
def run_all():
    run_pipeline()

@flow(name="connector-observability")
def pipeline():
    run_all()

if __name__ == "__main__":
    pipeline()
