#from __future__ import absolute_import, unicode_literals
#from celery import Celery
from celery import shared_task
import subprocess as sp
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
import sys
#app = Celery('tasks', backend='rpc://', broker=f'amqp://guest:guest@rabbit:5672//')

#@app.task
#def startAPI(x):
#    return x

class fashion_tools(object):
    def __init__(self,imageid,model,version=1.1):
        self.imageid = imageid
        self.model   = model
        self.version = version
        
    def get_dress(self,stack=False):
        """limited to top wear and full body dresses (wild and studio working)"""
        """takes input rgb----> return PNG"""
        name =  self.imageid
        file = cv2.imread(name)
        file = tf.image.resize_with_pad(file,target_height=512,target_width=512)
        rgb  = file.numpy()
        file = np.expand_dims(file,axis=0)/ 255.
        seq = self.model.predict(file)
        seq = seq[3][0,:,:,0]
        seq = np.expand_dims(seq,axis=-1)
        c1x = rgb*seq
        c2x = rgb*(1-seq)
        cfx = c1x+c2x
        dummy = np.ones((rgb.shape[0],rgb.shape[1],1))
        rgbx = np.concatenate((rgb,dummy*255),axis=-1)
        rgbs = np.concatenate((cfx,seq*255.),axis=-1)
        if stack:
            stacked = np.hstack((rgbx,rgbs))
            return stacked
        else:
            return rgbs
        
        
    def get_patch(self):
        return None


@shared_task
def startAPI(x):
    saved = load_model("/home/ubuntu/save_ckp_frozen.h5")
    api = fashion_tools(x, saved)
    image_ = api.get_dress(False)
    print('start API :', x)
    cv2.imwrite(x, image_)
    return x
