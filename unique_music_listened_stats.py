import util
import collections
with open('user_id trackcount.txt','r') as myFile:
    doc = myFile.read().split("\n")[1:]
temp_doc = [i.partition("\t") for i in doc]

#util.head(temp_doc,0,9)

unique_song_listened = [int(i[2]) for i in temp_doc]
#util.head(unique_song_listened,0,10)
cnt = collections.Counter(unique_song_listened).items()
temp = sorted(cnt,key =lambda x: x[0])
for i in temp:
    print i
