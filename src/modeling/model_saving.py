import os
import shutil
import tensorflow as tf
import logging
import platform

def save_keras_hdf5(model,  local_dir, filename, extension=None):

    if not extension:
        extension = ".h5"

    _make_dirs(local_dir)
    filename = filename + extension
    path = os.path.join(local_dir + "/" + filename)
    model.save(path)

    return path


def save_tensorflow_saved_model_archived(model, local_dir, filename, extension=".zip", model_number="1",
                                         temp_base_dir=None):

    if not temp_base_dir:
        if platform.system()=="Windows":
            temp_base_dir="C:\\tmp"
        else:
            temp_base_dir = os.path.join(os.getcwd(), "_tmp_model")


    root_dir = save_tensorflow_saved_model(model=model,
                                           local_dir=temp_base_dir,
                                           filename=os.path.splitext(filename)[0],
                                           model_number=model_number)

    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)

    shutil.make_archive(
        base_name=os.path.join(local_dir, filename),
        format=extension[1:],
        root_dir=root_dir,
        base_dir=model_number)

    shutil.rmtree(root_dir, ignore_errors=True)

    return os.path.join(local_dir, filename + extension)


def save_tensorflow_saved_model(model, local_dir, filename, model_number="1"):

    root_dir = os.path.join(local_dir, filename)
    sub_dir = os.path.join(root_dir, model_number)

    if not os.path.isdir(sub_dir):
        os.makedirs(sub_dir)

    tf.saved_model.save(model, sub_dir)

    return root_dir


def _make_dirs(dir):
    import os
    if not os.path.exists(dir):
        os.makedirs(dir)
