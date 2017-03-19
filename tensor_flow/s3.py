'''
Created on 18 mars 2017

@author: nicolas
'''

# import gym
# env = gym.make('CartPole-v0')
# env.reset()
# for _ in range(1000):
#     env.render()
#     env.step(env.action_space.sample()) # take a random action

import boto3
# 
# # Let's use Amazon S3 to read some data
# def read_file_from_S3():
#     s3 = boto3.resource('s3')
#     bucket = s3.Bucket('grislain')
#     data = bucket.Object('All-seasons.csv')
#     print data.get()['Body'].read(1000)
#     s3
# 
# with open('/Users/nicolas/Data/Iris.csv') as f:
#     for l in f:
#         print l

import tensorflow as tf
from tensorflow.python.ops.io_ops import ReaderBase

class S3Reader(ReaderBase):
    BUFFER_SIZE = 1<<16
    def __init__(self, skip_header_lines=None, name=None):
        self.current_name = None
        self.skip_header_lines = skip_header_lines
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket('grislain')
        self.current_object = None
        self.buffer = None
        self.last = ''
        self.current_line = 0
    def _read(self, name):
        if self.current_object == None:
            print name
            self.current_object = self.bucket.Object(name)
            self.buffer = self.current_object.get()['Body'].read(self.BUFFER_SIZE).split('\n')
            self.current_line = self.skip_header_lines
        if self.buffer == None:
            self.buffer = self.current_object.get()['Body'].read(self.BUFFER_SIZE).split('\n')
            self.current_line = 0
            self.buffer[0] = self.last+self.buffer[0]
        result = self.buffer[self.current_line]
        self.current_line+=1
        if self.current_line == len(self.buffer)-1:
            self.last = self.buffer[self.current_line]
            self.buffer = None
        return str(self.current_object), result
    def read(self, queue):
        if self.current_object == None:
            self.current_name = queue.dequeue()
        return tf.py_func(self._read, [self.current_name], [tf.string, tf.string])

#filename_queue = tf.train.string_input_producer(['/Users/nicolas/Data/Iris.csv'])
s3_queue = tf.train.string_input_producer(['Iris.csv'])
reader = S3Reader(skip_header_lines=1)
key, value = reader.read(s3_queue)
decode = tf.py_func(lambda t:map(float,t.split(',')[0:2]), [value], [tf.double, tf.double])
data = tf.decode_csv(value, [[0.0],[0.0],[0.0],[0.0],[0.0],['']])

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    for i in range(100):
        print sess.run([data, decode])
    coord.request_stop()
    coord.join(threads)
