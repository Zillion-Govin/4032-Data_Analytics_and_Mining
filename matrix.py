import numpy
import pandas
import io
import os

ENCODING = 'utf-8'
FILE_PATH = 'example.csv'
# FILE_SOURCE = '1.csv'
FILE_SOURCE ='new_raw.txt'

def get_list():
    music_list ={}
    user_list = {}
    with io.open(FILE_SOURCE, 'r', encoding=ENCODING) as source:
        for lines in source:
            line = lines.split('\t')
            music_list[line[1]] = 0
            user_list[line[0]] = 0
        return music_list,user_list

def create_file(data):
    if not os.path.exists(FILE_PATH) or  os.stat(FILE_PATH).st_size == 0 :
        with io.open(FILE_PATH,'w+',encoding = ENCODING):
            print "creating file..."
    data.to_csv(FILE_PATH, encoding=ENCODING)
    print 'finish '

def create_matrix():
    music_list,user_list = get_list()
    # range(0, len(user_list.keys()))
    data = pandas.DataFrame(0,columns=user_list.keys(),index=music_list.keys(),dtype='uint8')
    with io.open(FILE_SOURCE, 'r', encoding=ENCODING) as source:
        for i,lines in enumerate(source,0):
            line = lines.split('\t')
            data.loc[line[1]][line[0]] = line[2].strip('\n')
    create_file( data= data)

def get_matrix():
    data = pandas.DataFrame.from_csv(FILE_PATH,encoding = ENCODING)
    return data

if __name__ == "__main__":
    create_matrix()
    # print get_matrix()