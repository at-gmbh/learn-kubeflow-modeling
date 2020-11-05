from tensorflow.keras.initializers import glorot_normal
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.models import Sequential

def conv_simple(input_size_x, input_size_y, final_activation, nb_classes, dropout_rate, channels=3, seed=1234):
    dense_initializer = glorot_normal(seed=seed)
    conv_initializer = glorot_normal(seed=seed)

    model = Sequential()
    model.add(
        Conv2D(
            8,
            kernel_size=(4, 4),
            strides=(2, 2),
            kernel_initializer=conv_initializer,
            input_shape=(input_size_x, input_size_y, channels),
        )
    )

    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(Flatten())
    model.add(Dense(4, activation="relu", kernel_initializer=dense_initializer))
    model.add(Dropout(rate=dropout_rate, seed=seed))

    model.add(Dense(nb_classes, activation=final_activation))

    return model
