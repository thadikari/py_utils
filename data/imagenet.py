import tensorflow_datasets as tfds
import tensorflow as tf
import os

from . import prep_iterator


MANUAL_DIR = os.path.join(os.path.expanduser('~'), 'SCRATCH/DATASETS/tensorflow_datasets/manual')

def preproc_func(dd):
    dd['image'] = tf.image.resize_with_crop_or_pad(dd['image'], 227, 227)
    return dd

def get_dataset_pipeline(batch_size, test_size):
    if 0:
        splits, ds_info = tfds.load('imagenet_resized/16x16', with_info=True)
    else:
        config = tfds.download.DownloadConfig(manual_dir=MANUAL_DIR)
        splits, ds_info = tfds.load('imagenet2012', with_info=True, download_and_prepare_kwargs={'download_config':config})

    assert(test_size>0)
    preproc = lambda ds_: ds_.map(preproc_func, num_parallel_calls=4)
    train_ds = preproc(splits['train']).shuffle(batch_size*8).repeat().batch(batch_size).prefetch(4)
    test_ds = preproc(splits['validation']).shuffle(test_size*16).repeat().batch(test_size).prefetch(2)

    # fig = tfds.show_examples(ds_info, test_ds)
    return prep_iterator(train_ds, test_ds)
