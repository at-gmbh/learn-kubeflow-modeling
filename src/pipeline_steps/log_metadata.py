import mlflow
import click
import json

def log_meta_data(
        experiment_name: str,
        run_id: str,
        tracking_uri: str,
        metadata_dict: str,
        metadata_type: str,
):
    metadata_dict=json.loads(metadata_dict)
    if metadata_type == "metrics":
        log_many = mlflow.log_metrics
    elif metadata_type == "params":
        log_many = mlflow.log_params
    elif metadata_type == "tags":
        log_many = mlflow.set_tags
    else:
        raise NotImplementedError(
            f"Unknown meta_data_type '{metadata_type}'. Please select either 'metrics', 'params' or 'tags'"
        )

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    print(f"Now logging {metadata_type} metadata to run {run_id} of experiment {experiment_name} on tracking server {tracking_uri}")
    with mlflow.start_run(run_id=run_id):
        log_many(metadata_dict)

@click.command()
@click.option("--experiment_name")
@click.option("--run_id")
@click.option("--tracking_uri")
@click.option("--metadata_dict")
@click.option("--metadata_type")
def cli(*args, **kwargs):
    return log_meta_data(*args, **kwargs)

if __name__=="__main__":
    cli()
