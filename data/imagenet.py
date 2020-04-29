import tensorflow_datasets as tfds
import tensorflow as tf
import os

from . import prep_iterator


# http://www.image-net.org/challenges/LSVRC/2012/downloads
# https://www.tensorflow.org/datasets/catalog/imagenet2012

MANUAL_DIR = os.path.join(os.path.expanduser('~'), 'SCRATCH/DATASETS/tensorflow_datasets/manual')

def preproc_func(dd):
    dd['image'] = tf.image.resize_with_crop_or_pad(dd['image'], 227, 227)
    return dd

def get_dataset_pipeline(ds_name, batch_size, test_size):
    if ds_name!='imagenet2012':
        # solution to resource exhaustion: https://github.com/tensorflow/datasets/issues/1441
        #(name="imagenet_resized", builder_kwargs={'config':'64x64'}) # 16x16 32x32 64x64
        splits, ds_info = tfds.load(ds_name, with_info=True)
        preproc = lambda ds_:ds_
    else:
        config = tfds.download.DownloadConfig(manual_dir=MANUAL_DIR)
        splits, ds_info = tfds.load(ds_name, with_info=True, download_and_prepare_kwargs={'download_config':config})
        preproc = lambda ds_:ds_.map(preproc_func, num_parallel_calls=4)

    assert(test_size>0)
    train_ds = preproc(splits['train']).shuffle(batch_size*8).repeat().batch(batch_size).prefetch(4)
    test_ds = preproc(splits['validation']).shuffle(test_size*16).repeat().batch(test_size).prefetch(2)

    # fig = tfds.show_examples(ds_info, test_ds)
    return prep_iterator(train_ds, test_ds)
