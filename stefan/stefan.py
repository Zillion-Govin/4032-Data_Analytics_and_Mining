# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:22:44 2016

@author: Stefan Setyadi
"""

import numpy as np
import pandas as pd
import time
from sklearn.metrics import mean_squared_error as mse

def cos_sim(matrix, epsilon=1e-9):
    sim = matrix.T.dot(matrix) + epsilon
    norms = np.array([np.sqrt(np.diagonal(sim))])
    #print(norms)
    return (sim/norms/norms.T)

def predict_wsum(ratings,similarity):
    #print(np.array([np.abs(similarity).sum(axis=1)]))
    return ratings.dot(similarity)/ np.array([np.abs(similarity).sum(axis=0)])
    
def predict_topk(ratings,similarity,k):
    np.fill_diagonal(similarity,0)
    pred = np.zeros(ratings.shape).astype(np.float32)
    topk = get_topk_pos(similarity,k)
    for i in range(len(topk)):
        new_sim = similarity[i,topk[i]]
        new_rating = ratings[:,topk[i]]
        pred[:,i] = new_rating.dot(new_sim)/np.array([np.abs(new_sim).sum(axis=0)])
    return pred       
    
def get_mse(pred, actual):
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()
    return mse(pred, actual)    
    
def loadDF(pathName,name,cut_last=True):
    temp_df = pd.read_csv(pathName, sep=',', names=name)
    if(cut_last):
        temp_df.drop(name[-1:], axis=1, inplace=True)    
    return temp_df

def get_topk_pos(similarity,k):
    ## argpartition will return topk but not ordered
    return np.argpartition(-similarity,(0,k))[:,0:k]

def topk_mse(train,test,item_sim,k):
    test_mse = []
    train_mse = []
    print("starting top-k MSE")
    for i in k:
        starttime = time.time()
        prediction = predict_topk(train,item_sim,i)
        #print(prediction[:4,:4])
        train_mse.append(get_mse(prediction,train))
        test_mse.append(get_mse(prediction,test))
        print("k={}, time={}".format(i,time.time()-starttime))
    print("Train\t: {}".format(train_mse))
    print("Test\t: {}".format(test_mse))

def topk_to_file(writePathName, similarity,k):
    writeStr = []
    np.fill_diagonal(similarity,0)
    top10 = np.argpartition(-similarity,[i for i in range(k+1)])[:,0:k] # without the item itself
    for i in range(len(top10)):
        writeStr.append("{}:{}".format(index2_id[i],
                        ",".join(["{}={}".format(index2_id[j],similarity[i,j]) for j in top10[i]])))
    writeStr = "\n".join(writeStr)
    with open(writePathName, 'w') as writeFile:
        writeFile.write(writeStr)
        
def load_kc_sim(pathName,id_to_idx):
    temp = pd.read_csv(pathName, sep=',').values
    movie_id = temp[:,0].astype(np.int32)
    temp_sim = temp[:,1:].astype(np.float32)
    sim = np.zeros(temp_sim.shape).astype(np.float32)
    starttime = time.time()
    print("Start loading sim matrix")
    for i in range(len(movie_id)):
        for j in range(len(movie_id)):
            sim[id_to_idx[movie_id[i]],id_to_idx[movie_id[j]]] = temp_sim[i,j]
    print("Sim matrix loaded ,time:{}".format(time.time()-starttime))    
    return sim
        
trainingPathName = "./../dataset_partitioned/ratings_training.csv"
testPathName = "./../dataset_partitioned/ratings_test.csv"
headerName = ['user_id','item_id','rating','timestamp']
simName = "./../similarity_matrix/" + "similarity_cosine" + ".csv"


train_df = loadDF(trainingPathName,headerName)
test_df = loadDF(testPathName, headerName)
    
n_item = train_df.item_id.unique()
## create index between df index and raw item_id
index2_id = {}
id2_index = {}
for i in range(n_item.shape[0]):
    #print("{} {}".format(i,n_item[i]))
    index2_id[i] = n_item[i]
    id2_index[n_item[i]] = i

n_item = n_item.shape[0]
n_user = train_df.user_id.unique().shape[0]

#print("{} {}".format(n_user,n_item))

## fill up matrix with training data
train = np.zeros((n_user,n_item)).astype(np.float32)
for i in train_df.itertuples():
    #print( id2_index[i[2]])    
    train[i[1]-1, id2_index[i[2]]] = i[3]
print(train[:4,:4])

## create separate matrix to contain actual data (for testing)
test = np.zeros((n_user,n_item)).astype(np.float32)
for i in test_df.itertuples():
    #print( id2_index[i[2]])
    test[i[1]-1, id2_index[i[2]]] = i[3]

sparsity = float(len(train.nonzero()[0])) / n_user / n_item * 100
print("Train Sparsity: {:6.2f}%".format(sparsity))
sparsity = float(len(test.nonzero()[0])) / n_user / n_item * 100
print("Test Sparsity: {:6.2f}%".format(sparsity))

#item_sim = cos_sim(train)
item_sim = load_kc_sim(simName,id2_index)
print(item_sim[:4,:4])

#print(test[:4,:4])
#k = [1,2,5,10,20,40,100]#,200,500]
#k = [3,4,5,6,7,8,9]
#topk_mse(train,test,item_sim,k)

writePath = "top10-cosine_without_0.txt"
topk_to_file(writePath,item_sim,10)