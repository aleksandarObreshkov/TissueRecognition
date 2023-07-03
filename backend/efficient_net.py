import efficientnet.keras as efn
from tensorflow import keras
import datasets

class accuracy_callback(keras.callbacks.Callback):
    def on_epoch_end(self,epoch,logs={}):
        if (logs.get("accuracy")>0.98):
            print("\nReached desired accuracy so stopping training")
            self.model.stop_training =True

callback = accuracy_callback()
base_model = efn.EfficientNetB0(input_shape = (50, 50, 3), include_top = False, weights = 'imagenet')

for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = keras.layers.Flatten()(x)
x = keras.layers.Dense(2048, activation='relu')(x)
x = keras.layers.Dropout(0.5)(x)

# Add a final sigmoid layer with 1 node for classification output
predictions = keras.layers.Dense(1, activation='sigmoid')(x)
model_final = keras.models.Model(inputs = base_model.input, outputs = predictions)

model_final.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001, decay=1e-6), 
                    loss='binary_crossentropy', 
                    metrics=['accuracy'])

model_final.build((1,50,50,3))
model_final.summary()

eff_history = model_final.fit(datasets.get_training_dataset(), 
                              validation_data = datasets.get_validation_dataset(), 
                              epochs = 300, 
                              callbacks=[callback])

model_final.save('tissue_recogniser_efficient')
