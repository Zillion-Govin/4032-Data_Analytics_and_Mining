import io
import re


#already lowercase
doc = io.open("known.tsv",'r',encoding='utf-8').readlines()

url = io.open("url.tsv",'a',encoding='utf-8')
nourl = io.open("nourl.tsv",'a',encoding='utf-8')


for i in doc:
    if re.search('[-a-zA-Z0-9]{2,256}\.(com|org|pl)', i) is not None:
        url.write(i)
    else:
        nourl.write(i)
