def head(myList,start,end):
    for i in myList[start:end]:
        print repr(i)

def writeToFile(myStr, filename):
    with open(filename,'w') as newFile:
        newFile.write(myStr)
