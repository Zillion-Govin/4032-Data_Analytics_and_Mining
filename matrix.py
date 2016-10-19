import numpy
import pandas
import io
import os
from sklearn.cross_validation import train_test_split

ENCODING = 'ASCII'
FILE_PATH = 'matrix_userxmovies.csv'
MAT = 'matrix.csv'
# FILE_SOURCE = '1.tsv'
FILE_SOURCE ='ratings.dat'
TRAIN_SOURCE = 'train_file.csv'
TEST_SOURCE = 'test_file.csv'

def train_test(data):
    seed = 8
    numpy.random.seed(seed)
    train_file,test_file = train_test_split(data,test_size = 0.2, random_state = seed)
    create_file(train_file,TRAIN_SOURCE)
    create_file(test_file,TEST_SOURCE)

def get_list(type):
    movie_list ={}
    user_list = {}
    # with io.open(TRAIN_SOURCE, 'r', encoding=ENCODING) as source:
    #     for lines in source:
    #         line = lines.strip().split(',')
    #         movie_list[line[2]] = 0
    #         user_list[line[1]] = 0
    if type == 'normal':
        with io.open(FILE_SOURCE, 'r', encoding=ENCODING) as source:
            for lines in source:
                line = lines.strip().split('::')
                movie_list[line[1]] = 0
                user_list[line[0]] = 0
    elif type == 'train':
        with io.open(TRAIN_SOURCE, 'r', encoding=ENCODING) as source:
            for lines in source:
                line = lines.strip().split(',')
                movie_list[line[2]] = 0
                user_list[line[1]] = 0
    else:
        with io.open(TEST_SOURCE, 'r', encoding=ENCODING) as source:
            for lines in source:
                line = lines.strip().split(',')
                movie_list[line[2]] = 0
                user_list[line[1]] = 0

    return movie_list,user_list

def create_file(data,path):
    if not os.path.exists(path):
        with io.open(path,'w+',encoding = ENCODING):
            print "creating file..."
    data.to_csv(path, encoding=ENCODING)
    print 'finish'

def create_matrix(type = 'normal'):
    source = pandas.read_csv(FILE_SOURCE,delimiter ='::',encoding=ENCODING)
    train_test(source)
    movie_list,user_list = get_list(type)
    # range(0, len(user_list.keys()))
    data = pandas.DataFrame(0,columns=user_list.keys(),index=movie_list.keys(),dtype='uint8')
    if type =='normal':
        with io.open(FILE_SOURCE, 'r', encoding=ENCODING) as source:
            for i, lines in enumerate(source, 0):
                line = lines.split('::')
                data.loc[line[1]][line[0]] = line[2]
    elif type=='train':
        with io.open(TRAIN_SOURCE, 'r', encoding=ENCODING) as source:
            for i, lines in enumerate(source, 0):
                line = lines.split(',')
                data.loc[line[2]][line[1]] = line[3]
    else:
        with io.open(TEST_SOURCE, 'r', encoding=ENCODING) as source:
            for i, lines in enumerate(source, 0):
                line = lines.split(',')
                data.loc[line[2]][line[1]] = line[3]
    data.replace(0,numpy.NaN,inplace=True)
    create_file( data= data,path=FILE_PATH)

def get_matrix():
    data = pandas.DataFrame.from_csv(MAT,encoding = ENCODING)
    return data

if __name__ == "__main__":
    create_matrix(type = 'normal')
    # print get_matrix()
    # df = get_matrix()
    # create_file(df.T,FILE_PATH)