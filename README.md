# Download datasets
* Auto downloading datasets:
```
python -c 'import tensorflow_datasets as tfds; tfds.load("mnist")'
python -c 'import tensorflow_datasets as tfds; tfds.load("fashion_mnist")'
python -c 'import tensorflow_datasets as tfds; tfds.load("cifar10")'

python -c 'import tensorflow_datasets as tfds; tfds.load("imagenet_resized/8x8")'
python -c 'import tensorflow_datasets as tfds; tfds.load("imagenet_resized/16x16")'
python -c 'import tensorflow_datasets as tfds; tfds.load("imagenet_resized/32x32")'
python -c 'import tensorflow_datasets as tfds; tfds.load("imagenet_resized/64x64")'

python -c 'import tensorflow_datasets as tfds; tfds.load("imagenet2012")
```

* The last requires manually downloading original imagenet data to `tensorflow_datasets/downloads/manual` from http://www.image-net.org/challenges/LSVRC/2012/downloads as instructed in https://www.tensorflow.org/datasets/catalog/imagenet2012. 
