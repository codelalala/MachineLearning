# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 22:17:30 2017
Example from: https://indico.io/blog/getting-started-with-mxnet/
"""

import mxnet as mx
import numpy as np

data=mx.sym.Variable("data")
label=mx.sym.Variable("softmax_label")

w1=mx.sym.Variable("weight1")
b1=mx.sym.Variable("bias1")
l1=mx.sym.FullyConnected(data=data,num_hidden=128,name="layer1",weight=w1,bias=b1)
a1=mx.sym.Activation(data=l1,act_type="relu",name="act1")

l2=mx.sym.FullyConnected(data=a1,num_hidden=10,name="layer2")

cost_classification=mx.sym.SoftmaxOutput(data=l2,label=label)

batch_size=128
input_shapes={"data":(batch_size,28*28),"softmax_label":(batch_size,)}
executor=cost_classification.simple_bind(ctx=mx.gpu(0),grad_req='write',**input_shapes)

executor_test=cost_classification.bind(ctx=mx.gpu(0),grad_req='null',args=executor.arg_arrays)

for r in executor.arg_arrays:
    r[:]=np.random.randn(*r.shape)*0.02
    
from skdata.mnist.view import OfficialVectorClassification

data=OfficialVectorClassification()
trIdx=data.sel_idxs[:]
teIdx=data.val_idxs[:]
for epoch in range(10):
    print("starting epoch",epoch)
    np.random.shuffle(trIdx)
    
    for x in range(0,len(trIdx),batch_size):
        batchX=data.all_vectors[trIdx[x:x+batch_size]]
        batchY=data.all_labels[trIdx[x:x+batch_size]]
        
        if(batchX.shape[0]!=batch_size):
            continue
        executor.arg_dict['data'][:]=batchX/255.
        
        executor.arg_dict['softmax_label'][:]=batchY
        executor.forward()
        executor.backward()
        
        for pname,W,G in zip(cost_classification.list_arguments(),executor.arg_arrays,executor.grad_arrays):
            if pname in ['data','softmax_label']:
                continue
            W[:]=W-G*.001
        
    num_correct=0
    num_total=0        
        
    for x in range(0,len(teIdx),batch_size):
        batchX=data.all_vectors[teIdx[x:x+batch_size]]
        batchY=data.all_labels[teIdx[x:x+batch_size]]
        
        if(batchX.shape[0]!=batch_size):
            continue
        executor_test.arg_dict['data'][:]=batchX/255.
        executor_test.forward()
        
        num_correct+=sum(batchY==np.argmax(executor_test.outputs[0].asnumpy(),axis=1))
        num_total+=len(batchY)
    print("accuracy thus far", num_correct/num_total)