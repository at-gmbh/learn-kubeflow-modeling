from modeling import model_saving
from modeling import model_definition
from modeling import artifact_storage
import json
import click

def train(
        model_definition_name: str,
        model_params: str,
        train_inputs_uri: str,
        train_targets_uri: str,
        valid_inputs_uri: str,
        valid_targets_uri: str,
        model_filename: str,
        model_local_dir: str,
        model_savedmodel_uri: str,
        model_hdf5_uri: str,
        epochs: int =5,
        batch_size: int =32,
        optimizer: str ="Adam",
        loss: str ="categorical_crossentropy",
    ):

    model_params = json.loads(model_params)

    # define and compile model
    print("Now comping model")
    define_model = getattr(model_definition, model_definition_name)
    model = define_model(**model_params)
    model.compile(optimizer=optimizer, loss=loss)
    print(model.summary)

    # fetch data
    print(f"Now reading training inputs and targets from {train_targets_uri} and {train_targets_uri}")
    train_inputs = artifact_storage.read_array_from_s3(train_inputs_uri)
    train_targets = artifact_storage.read_array_from_s3(train_targets_uri)

    print(f"Now reading validation inputs and targets from {valid_inputs_uri} and {valid_targets_uri}")
    valid_inputs = artifact_storage.read_array_from_s3(valid_inputs_uri)
    valid_targets = artifact_storage.read_array_from_s3(valid_targets_uri)

    # fit model
    print("Now fitting model")
    model.fit(
        x=train_inputs,
        y=train_targets,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(valid_inputs, valid_targets)
    )

    # save model and copy it to S3
    # SavedModel
    print(f"Saving model in SavedModel format to {model_savedmodel_uri}")
    local_path = model_saving.save_tensorflow_saved_model(model, model_local_dir, model_filename)
    artifact_storage.copy_from_disk_to_s3(local_path, model_savedmodel_uri)

    #HDF5
    print(f"Saving model in HDF5 format to {model_hdf5_uri}")
    local_path = model_saving.save_keras_hdf5(model, model_local_dir, model_filename)
    artifact_storage.copy_from_disk_to_s3(local_path, model_hdf5_uri)

@click.command()
@click.option("--model_definition_name")
@click.option("--model_params")
@click.option("--train_inputs_uri")
@click.option("--train_targets_uri")
@click.option("--valid_inputs_uri")
@click.option("--valid_targets_uri")
@click.option("--model_filename")
@click.option("--model_local_dir")
@click.option("--model_savedmodel_uri")
@click.option("--model_hdf5_uri")
@click.option("--epochs", type=int)
@click.option("--batch_size", type=int)
@click.option("--optimizer")
@click.option("--loss")
def cli(*args, **kwargs):
    return train(*args, **kwargs)

if __name__=="__main__":
    cli()