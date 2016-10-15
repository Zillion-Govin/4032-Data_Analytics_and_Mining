with open("user_id trackcount.txt",'r') as myFile:
    doc = myFile.read().split('\n')

playcount = [i.partition("\t") for i in doc[1:]]
print len(playcount)

new_doc = ["".join(i) for i in playcount if i[2] not in '12']
new_doc = "\n".join([doc[0]] + new_doc)

with open("unique_song_listener.txt",'w+') as newFile:
    newFile.write(new_doc)
