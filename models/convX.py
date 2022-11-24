import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense

'''
Code sources:
https://github.com/uber-research/deconstructing-lottery-tickets/blob/dbad201f77c7d1423569f0310971926be91d8856/network_builders.py
https://www.tensorflow.org/guide/keras/sequential_model
https://pyimagesearch.com/2019/10/28/3-ways-to-create-a-keras-model-with-tensorflow-2-0-sequential-functional-and-model-subclassing/

Model references:
Figure 2 in "THE LOTTERY TICKET HYPOTHESIS: FINDING SPARSE, TRAINABLE NEURAL NETWORKS"
Table 1 in "What’s Hidden in a Randomly Weighted Neural Network?"
'''

glorot_normal = tf.keras.initializers.glorot_normal()

def create_model(convs, fcs):
    layers = []

    def add_conv(dim):
        layers.append(Conv2D(dim, 3, kernel_initializer=glorot_normal, padding='same'))
        layers.append(Activation('relu'))

    for dim in convs:
        add_conv(dim)
        add_conv(dim)
        layers.append(MaxPooling2D((2, 2), (2, 2)))

    layers.append(Flatten())

    add_dense = lambda dim, act: layers.append(Dense(dim, kernel_initializer=glorot_normal, activation=act))
    for dim in fcs[:-1]: add_dense(dim, 'relu')
    add_dense(fcs[-1], 'linear')

    return Sequential(layers)

create_ = lambda out_dim, convs: create_model(convs, [256, 256, out_dim])
conv2 = lambda out_dim: create_(out_dim, [64, ])
conv4 = lambda out_dim: create_(out_dim, [64, 128])
conv6 = lambda out_dim: create_(out_dim, [64, 128, 256])
conv8 = lambda out_dim: create_(out_dim, [64, 128, 256, 512])
conv10= lambda out_dim: create_(out_dim, [64, 128, 256, 512, 1024])
