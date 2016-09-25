import io
doc = io.open("output.tsv",'r',encoding='utf-8').read()
doc = doc.lower().split("\n")
print len(doc)

unknown_doc = [i for i in doc if "[unknown]" in i]
known_doc = [i for i in doc if "[unknown]" not in i]
print len(unknown_doc)
print len(known_doc)

with io.open("nounknown.tsv",'a',encoding='utf-8') as myFile:
    for i in unknown_doc:
        myFile.write(i+"\n")
        
with io.open("known.tsv",'a',encoding='utf-8') as myFile:
    for i in known_doc:
        myFile.write(i+"\n")

