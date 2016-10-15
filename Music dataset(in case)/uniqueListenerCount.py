import util
import collections
"""
from raw data
check unique listener of each song and filter it
"""
filename = 'user_id artist_id_track_id playcount.txt'
#filename = "secondFilteredRaw.txt"

def filterSongUniquePlayer(n):
    with open(filename,'r') as myFile:
        doc = myFile.read().split("\n")

    temp = [i.partition("\t")[2].partition("\t")[0] for i in doc]
    cnt = collections.Counter(temp).items()
    sorted_cnt = sorted(cnt,key=lambda x: x[1],reverse=True)

    filteredCount = filter(lambda x: x[1]>=n,sorted_cnt)

    #util.writeToFile("\n".join(["{}\t{}".format(i,j) for i,j in filteredCount]),"uniqueListenerCount.txt")

    return [i[0] for i in filteredCount]
    

#filterSongUniquePlayer(4)
