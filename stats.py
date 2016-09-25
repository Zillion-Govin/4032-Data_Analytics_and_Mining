import io

doc = io.open("output.tsv",'r',encoding='utf-8').readlines()
print len(doc)

doc = io.open("known.tsv",'r',encoding='utf-8').readlines()
print len(doc)

doc = io.open("nounknown.tsv",'r',encoding='utf-8').readlines()
print len(doc)

doc = io.open("nourl.tsv",'r',encoding='utf-8').readlines()
print len(doc)

doc = io.open("url.tsv",'r',encoding='utf-8').readlines()
print len(doc)
