from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50

def resnet50_classifcation(input_size, nb_classes, final_activation="softmax"):
    # NOTE: Input size needs to be at least (32, 32).
    base_model = ResNet50(
        include_top=False,
        weights="imagenet",
        input_tensor=None,
        input_shape=(input_size[0], input_size[1], 3),
        pooling=None,
        classes=nb_classes,
    )
    x = base_model.output
    predictions = Dense(nb_classes, activation=final_activation)(x)
    model = Model(inputs=base_model.input, outputs=[predictions,])
    return model
