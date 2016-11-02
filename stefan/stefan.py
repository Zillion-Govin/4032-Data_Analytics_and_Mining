# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:22:44 2016

@author: Stefan Setyadi
"""

import numpy as np
import pandas as pd
import time
from sklearn.metrics import mean_squared_error as mse, mean_absolute_error as mae
from sklearn.metrics import pairwise_distances as distance

def cos_sim(matrix, epsilon=1e-9):
    sim = matrix.T.dot(matrix) + epsilon
    norms = np.array([np.sqrt(np.diagonal(sim))])
    #print(norms)
    return (sim/norms/norms.T)

def correlation_sim(matrix):
    return np.corrcoef(matrix.T)    
    
def predict_wsum(ratings,similarity):
    return ratings.dot(similarity)/ np.array([np.abs(similarity).sum(axis=0)])
    
def predict_topk(ratings,similarity,k):
    pred = np.zeros(ratings.shape).astype(np.float32)
    topk = get_topk_pos(similarity,k)
    for i in range(len(topk)):
        new_sim = similarity[i,topk[i]]
        new_rating = ratings[:,topk[i]]
        pred[:,i] = predict_wsum(new_rating,new_sim)
    return pred
    
def get_score(pred, actual):
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()
    mseResult = mse(pred,actual)
    maeResult = mae(pred,actual)
    print("MSE = {}, MAE = {}".format(mseResult,maeResult))
    return mseResult    
    
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
    np.fill_diagonal(item_sim,0)
    for i in k:
        starttime = time.time()
        prediction = predict_topk(train,item_sim,i)
        #print(prediction[:4,:4])
        train_mse.append(get_score(prediction,train))
        test_mse.append(get_score(prediction,test))
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
        
def load_kc_sim(pathName,id_to_idx,eps=1e-9):
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
    return sim+eps
        
trainingPathName = "./../dataset_partitioned/ratings_training.csv"
testPathName = "./../dataset_partitioned/ratings_test.csv"
headerName = ['user_id','item_id','rating','timestamp']
simName = "./../similarity_matrix/" + "newest_adjusted_cosine" + ".csv"


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
#item_sim = 1-distance(train.T, metric='cosine')
item_sim = correlation_sim(train)
#item_sim = load_kc_sim(simName,id2_index)
print(item_sim[:4,:4])

#print(test[:4,:4])
k = [1,2,5,10,20,40,100]#,200,500]
#k = [10,11,12,13,14,15]
topk_mse(train,test,item_sim,k)

#writePath = "top10-adjusted_cosine.txt"
#topk_to_file(writePath,item_sim,10)