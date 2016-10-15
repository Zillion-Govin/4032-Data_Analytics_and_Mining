import uniqueListenerCount
import util

"""
remove song that have less than n amount of unique listener from raw data
"""
n=4

song_list = set(uniqueListenerCount.filterSongUniquePlayer(n))
#print len(song_list)

with open('user_id artist_id_track_id playcount.txt','r') as myFile:
    doc = myFile.read().split("\n")[1:]

temp = filter(lambda x: x.partition("\t")[2].partition("\t")[0] in song_list,doc)

util.writeToFile("\n".join(temp),"filteredRaw.txt")
