import math
from math import sqrt
import numpy as np
import tensorflow as tf
from tensorflow.python.framework import dtypes
from tensorflow.python.ops import random_ops
import tensorflow.contrib.layers as layers
from utils.tf_util import layer_norm_fn
from utils.optimizers import huber_loss, minimize_and_clip, l2_loss, minimize
FLAGS = tf.app.flags.FLAGS


class SFNetwork:
    def __init__(self, nb_actions, nb_states, scope):
        with tf.variable_scope(scope):

            self.nb_actions = nb_actions
            self.nb_states = nb_states

            self.features = tf.placeholder(shape=[None, nb_states], dtype=tf.float32, name="Input")

            self.w_sf = tf.Variable(tf.random_uniform([nb_states, nb_actions * nb_states], 0, 0.01))
            self.sf = tf.matmul(self.fi, self.w_sf)
            self.sf = tf.reshape(self.sf, [-1, self.nb_actions, nb_states])

            if scope != 'target':
                self.actions = tf.placeholder(shape=[None], dtype=tf.int32, name="actions")
                self.actions_onehot = tf.one_hot(self.actions, nb_actions, dtype=tf.float32, name="actions_one_hot")
                self.actions_onehot = tf.tile(self.actions_onehot, [1, 1, nb_states])
                self.target_sf = tf.placeholder(shape=[None, nb_states], dtype=tf.float32, name="target_SF")

                self.sf_a = tf.reduce_sum(tf.multiply(self.sf, self.actions_onehot),
                                                  reduction_indices=1, name="SF")
                # Loss functions
                td_error_sf = self.sf_a - self.target_sf
                self.sf_loss = tf.reduce_mean(huber_loss(td_error_sf))
                if FLAGS.optimizer == "Adam": # to add more optimizers
                    optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.lr)
                else: # default = Adam
                    optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.lr)
                gradients, self.train_op = minimize_and_clip(optimizer, self.sf_loss, tf.trainable_variables(), FLAGS.gradient_norm_clipping)
                # gradients, self.train_op = minimize(optimizer, self.action_value_loss, tf.trainable_variables())
                self.summaries = []
                # self.summaries.append(
                #     tf.contrib.layers.summarize_collection("variables"))  # tf.get_collection("variables")))
                # self.summaries.append(tf.contrib.layers.summarize_collection("activations",
                #                                                              summarizer=tf.contrib.layers.summarize_activation))

                for grad, weight in gradients:
                    if grad is not None:
                        self.summaries.append(tf.summary.histogram(weight.name + '_grad', grad))
                        self.summaries.append(tf.summary.histogram(weight.name, weight))

                self.merged_summary = tf.summary.merge(self.summaries)




