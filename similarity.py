import numpy as np
import time
import pandas as pd
import io
import os
from scipy.spatial.distance import cosine

ENCODING = 'ASCII'
FILE_SOURCE = os.path.join('dataset_matrix', 'matrix.csv')

source = pd.read_csv(FILE_SOURCE, delimiter =',', encoding = ENCODING)

path_cosine = os.path.join('similarity_matrix', 'similarity_cosine.csv')
path_adjusted = os.path.join('similarity_matrix', 'similarity_adjusted_cosine.csv')
path_correlation = os.path.join('similarity_matrix', 'similarity_correlation.csv')

def cosine_similarity():
    sou = pd.read_csv(FILE_SOURCE, delimiter = ',' , encoding = ENCODING)
    indexing = get_list()
    df = pd.DataFrame(float(0), index = indexing, columns = indexing)
    num_movie = len(indexing)
    for i in range(0,num_movie):
        for j in range(i,num_movie):
            tempMatrix = sou.iloc[[i,j],1:].T
            tempMatrix = tempMatrix.dropna(how='any')
            
            if(tempMatrix.empty):
                result = 0
            else:
                result = float("{0:.2f}".format(1-cosine(tempMatrix.iloc[:,0],tempMatrix.iloc[:,1])))
            df.iat[i,j] = result
            df.iat[j,i] = result
        print(i)
    print(df)
    create_file(df,path_cosine)
        
def correlation_similarity():
    sou = pd.read_csv(FILE_SOURCE, delimiter = ',' , encoding = ENCODING)
    indexing = get_list()
    print(sou)
    df = pd.DataFrame(float(0), index = indexing, columns = indexing)
    sou = sou.set_index(indexing).T
    averrating = sou.iloc[1:,:].mean()
    print(averrating)
    sou = sou.T.sub(averrating,axis='index').T
    print(sou)
    num_movie = len(indexing)
    for i in range(0,num_movie):
        starttime = time.time()
        for j in range(i,num_movie):
            tempMatrix = sou.iloc[1:,[i,j]]
            tempMatrix = tempMatrix.dropna(how='any')
            '''if(tempI == 0 or tempJ == 0):
                cosineSim[i][j] = -10
                cosineSim[j][i] = -10
            else:
                cosineSim[i][j] = float("{0:.2f}".format(temp/((tempI**0.5)*(tempJ**0.5))))
                cosineSim[j][i] = cosineSim[i][j]'''
            
            if(tempMatrix.empty):
                result = 0
            else:
                result = float("{0:.2f}".format(2-cosine(tempMatrix.iloc[:,0],tempMatrix.iloc[:,1])))/2
            df.iat[i,j] = result
            df.iat[j,i] = result
            print(result)
        stoptime=time.time()-starttime
        print(i)
        print(stoptime)
    create_file(df,path_correlation)
    
def adjusted_cosine_similarity():
    sou = pd.read_csv(FILE_SOURCE, delimiter = ',' , encoding = ENCODING)
    indexing = get_list()
    df = pd.DataFrame(float(0), index = indexing, columns = indexing)
    num_movie = len(indexing)
    averrating = pd.Series(float(0), index = sou.columns)
    num_user = sou.shape[1]
    bu = sou.mean()
    print("user rating raw done")
    alpha = 1
    ru = pd.Series(float(0), index = sou.columns)
    total_valid= 0.0
    total_data = 0.0
    for i in range(1, num_user):
        ru.iat[i] = len(sou.iloc[:,i].dropna(how='any'))
        total_valid+= ru.iat[i]
        total_data += bu[i]*ru.iat[i]
    print("|RU| done")
    globalmean = total_data/total_valid
    print("global mean done")
    
    for i in range(1, num_user):
        averrating.iat[i]=alpha/(alpha+ru[i])*globalmean+ru[i]/(alpha+ru[i])*bu[i]
    print("normalized user rating done")
    
    for i in range(0,num_movie):
        starttime = time.time()
        for j in range(i,num_movie):
            tempMatrix = sou.iloc[[i,j],1:].T.sub(averrating,axis='index').dropna(how='any')
            
            '''if(tempI == 0 or tempJ == 0):
                cosineSim[i][j] = -10
                cosineSim[j][i] = -10
            else:
                cosineSim[i][j] = float("{0:.2f}".format(temp/((tempI**0.5)*(tempJ**0.5))))
                cosineSim[j][i] = cosineSim[i][j]'''
            
            if(tempMatrix.empty):
                result = 0
            else:
                result = float("{0:.2f}".format(2-cosine(tempMatrix.iloc[:,0],tempMatrix.iloc[:,1])))/2
            df.iat[i,j] = result
            df.iat[j,i] = result

        stoptime=time.time()-starttime
        print(i)
        print(stoptime)
    create_file(df,path_adjusted)
    print(df)
                
def create_file(data,path):
    if not os.path.exists(path):
        with io.open(path,'w+',encoding = ENCODING):
            print ("creating file...")
    data.to_csv(path, encoding=ENCODING)
    print ('finish')

def get_list():
    movie_list = source.iloc[:,0]
    return (movie_list)

    
