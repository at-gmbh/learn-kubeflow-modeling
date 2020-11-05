from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from tensorflow.keras.applications import NASNetLarge

def nasnet_classification(input_size, nb_classes, final_activation="softmax"):
    # NOTE: If using imagenet, input size needs to be [331, 331].
    base_model = NASNetLarge(
        input_shape=(input_size[0], input_size[1], 3),
        include_top=False,
        weights="imagenet",
        input_tensor=None,
        pooling="avg",
    )

    x = base_model.output
    predictions = Dense(nb_classes, activation=final_activation)(x)

    model = Model(inputs=base_model.input, outputs=[predictions,])

    return model
