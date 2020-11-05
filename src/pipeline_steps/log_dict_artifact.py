import mlflow
import os
import yaml
import json
import click

def log_dict_artifact(
        experiment_name: str,
        run_id: str,
        tracking_uri: str,
        artifact: str,
        artifact_name: str,
        artifact_path: str = None,
        output_type="yaml",
        local_path="./tmp/{filename}",
):
    if artifact_path =="None":
        artifact_path = None

    artifact=json.loads(artifact)

    if not os.path.isdir(local_path):
        os.makedirs(local_path)

    filename = f"{artifact_name}.{output_type}"
    local_path = local_path.format(filename=filename)

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_id=run_id):
        with open(local_path, "wt") as f:
            if output_type == "yaml":
                yaml.dump(artifact, f)
            elif output_type == "json":
                json.dump(artifact, f, indent=2)
            else:
                raise NotImplementedError(
                    f"Unknown output_type '{output_type}'. Please select either 'yaml' or 'json'"
                )

        print("Now logging dictionary artifact to {}".format(artifact_path))
        mlflow.log_artifact(local_path, artifact_path)

@click.command()
@click.option("--experiment_name")
@click.option("--run_id")
@click.option("--tracking_uri")
@click.option("--artifact")
@click.option("--artifact_name")
@click.option("--artifact_path")
@click.option("--output_type")
@click.option("--local_path")
def cli(*args, **kwargs):
    return log_dict_artifact(*args, **kwargs)

if __name__=="__main__":
    cli()