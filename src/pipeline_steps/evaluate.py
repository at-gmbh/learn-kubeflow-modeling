from modeling import artifact_storage, metrics
import json
import json_tricks
import click


def evaluate(
    predictions_uri: str,
    targets_uri: str,
    metric_names: list,
) -> dict:
    predictions = artifact_storage.read_array_from_s3(predictions_uri)
    targets = artifact_storage.read_array_from_s3(targets_uri)
    results = {}

    for metric_name in metric_names:
        print("Now calculating {}".format(metric_name))
        metric_function = getattr(metrics, metric_name)
        results[metric_name] = metric_function(targets=targets, predictions=predictions)

    results = _prepare_numpy_dict(results)
    print("Calculated metrics: \n{}".format(json.dumps(results, indent=2)))

    return results

def _prepare_numpy_dict(d):
    return json.loads(json_tricks.dumps(d, indent=2, allow_nan=True))

@click.command()
@click.option("--predictions_uri")
@click.option("--targets_uri")
@click.option("--metric_names")
def cli(*args, **kwargs) -> dict:
    return evaluate(*args, **kwargs)

if __name__=="__main__":
    cli()