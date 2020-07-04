import tensorflow_datasets as tfds
import tensorflow as tf
import numpy as np
import os


def make_dataset(name, dataset_args):
    splits, ds_info = tfds.load(name, with_info=True)
    train_size = ds_info.splits['train'].num_examples
    test_size = ds_info.splits['test'].num_examples
    dataset_args.update({'train_buffer':train_size, 'train_prefetch':10,
                         'test_buffer':test_size, 'test_prefetch':10})
    return Dataset(splits['train'], splits['test'], train_num_examples=train_size, **dataset_args)


class Dataset:
    def __init__(self, train_ds, test_ds, batch_size, test_size, train_num_examples,
                 train_buffer, test_buffer, train_prefetch, test_prefetch,
                 num_workers=1, worker_index=0):

        self.train_num_examples = train_num_examples
        train_ds = train_ds.shard(num_shards=num_workers, index=worker_index)\
                    .shuffle(train_buffer).repeat().batch(batch_size).prefetch(train_prefetch)
        test_ds = test_ds.shuffle(test_buffer).repeat().batch(test_size).prefetch(test_prefetch)

        v1d = tf.compat.v1.data
        self.handles = [_ds.make_one_shot_iterator().string_handle() for _ds in [train_ds, test_ds]]
        self.handle = tf.placeholder(tf.string, shape=[])
        iterator = v1d.Iterator.from_string_handle(self.handle, v1d.get_output_types(train_ds), v1d.get_output_shapes(train_ds))
        next_batch = iterator.get_next()
        self.placeholders = tf.cast(next_batch['image'], tf.float32)/255.0, next_batch['label']

    def init(self, sess):
        self.train_fd, self.test_fd = [{self.handle: hl} for hl in sess.run(self.handles)]

    def get_train_fd(self): return self.train_fd
    def get_test_fd(self): return self.test_fd


def merge_feed_dicts(*train_test_dicts_list):
    ret_callers = []
    train_list_test_list = list(zip(*train_test_dicts_list))
    for feed_dict_list in train_list_test_list:
        # https://stackoverflow.com/questions/3431676/creating-functions-in-a-loop
        # need early binding within a for loop
        def get_fd_call(feed_dict_list=feed_dict_list):
            merged_dict = {}
            for feed_dict in feed_dict_list:
                if callable(feed_dict): feed_dict = feed_dict()
                merged_dict.update(feed_dict)
            return merged_dict
        ret_callers.append(get_fd_call)
    return ret_callers


def compute_metrics_inner(logits, target, correct_pred):
    num_classes = logits.shape[-1]
    target_1h = tf.one_hot(tf.cast(target, tf.int32), num_classes)
    losses = tf.losses.softmax_cross_entropy(target_1h, logits, reduction='none')
    sum_loss = tf.reduce_sum(losses)
    avg_loss = tf.reduce_mean(losses)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32), name='accuracy')
    return accuracy, sum_loss, avg_loss

def compute_metrics_topk(logits, target, k):
    correct_pred = tf.nn.in_top_k(predictions=logits, targets=target, k=k)
    return compute_metrics_inner(logits, target, correct_pred)

def compute_metrics(logits, target):
    correct_pred = tf.equal(tf.argmax(logits, 1), tf.cast(target, 'int64'))
    return compute_metrics_inner(logits, target, correct_pred)


def l2_reg_loss(var_list):
    return tf.add_n([tf.nn.l2_loss(v) for v in var_list])
