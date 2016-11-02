import numpy
import pandas
import io
import os
from sklearn.cross_validation import train_test_split

ENCODING = 'ASCII'
FILE_PATH = 'dataset_matrix\\matrix.csv'
TRAIN_SOURCE = 'dataset_partitioned\\ratings_training.dat'
TEST_SOURCE = 'dataset_partitioned\\ratings_test.dat'

def get_list(path):
    movie_list ={}
    user_list = {}
    with io.open(path, 'r', encoding=ENCODING) as source:
        for lines in source:
            line = lines.strip().split('::')
            movie_list[line[1]] = 0
            user_list[line[0]] = 0
    return movie_list,user_list

def create_file(data,path):
    if not os.path.exists(path):
        with io.open(path,'w+',encoding = ENCODING):
            print "creating file..."
    data.to_csv(path, encoding=ENCODING)
    print 'finish'

def create_matrix(path,dest):
    movie_list,user_list = get_list(path)
    # range(0, len(user_list.keys()))
    data = pandas.DataFrame(0,columns=user_list.keys(),index=movie_list.keys(),dtype='uint8')
    with io.open(path, 'r', encoding=ENCODING) as source:
        for i, lines in enumerate(source, 0):
            line = lines.split('::')
            data.loc[line[1]][line[0]] = int(line[2])
    data.replace(0, numpy.NaN, inplace=True)
    create_file( data= data,path=dest)

def get_matrix(path):
    data = pandas.DataFrame.from_csv(path,encoding = ENCODING)
    return data

if __name__ == "__main__":
    create_matrix(path = TRAIN_SOURCE,dest = FILE_PATH)