filename = "new_raw.txt"
with open(filename,'r') as myFile:
    doc = myFile.readlines()[1:]
songs = [i.split("\t")[1] for i in doc]
print len(songs)
unique_song = set(songs)
print len(unique_song)
