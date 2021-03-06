#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import sys
import tensorflow as tf
import datautils
from fm import FMClassifier, FMRegressor


# model related
INPUT_DIM = 18765
HIDDEN_DIM = 128
REG_W = 0.0
REG_V = 0.0
# dump related
MDL_CKPT_DIR = './model_ckpt/'
MDL_CMPT_DIR = './model_ckpt/'
TRAIN_FILE = './rt-polarity.shuf.train'
TEST_FILE = './rt-polarity.shuf.test'
# feed function related
feed_fn = datautils.index_input_func

# read test data
test_x, test_y = feed_fn([x.rstrip('\n') for x in open(TEST_FILE).readlines()], INPUT_DIM)

model_ = FMClassifier(
    input_dim=INPUT_DIM,
    hidden_dim=HIDDEN_DIM,
    lambda_w=REG_W,
    lambda_v=REG_V)

sess = tf.Session()

# restore with local variables (optimizer)
# model_.ckpt_saver.restore(sess, tf.train.latest_checkpoint(MDL_CKPT_DIR))
model_.saver.restore(sess, tf.train.latest_checkpoint(MDL_CMPT_DIR))
print('Global steps:', sess.run(model_.global_step))

with open('train_done_test_res', 'w') as f:
    preds = model_.predict_proba(sess, test_x)
    for l, p in zip(test_y, preds):
        print(*map(str, [l[0], p[0]]), sep='\t', file=f)
    embs = model_.get_embedding(sess, test_x)
    for e in embs:
        print(e, file=f)

sess.close()
