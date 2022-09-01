#!/usr/bin/python

import hashlib
from importlib.resources import read_binary
import os
import re
import multiprocessing
import time
from tokenize import Number

walkPath="/mnt/tmp/"
searchRegexStr="*"
allFileHashes = []
hashCalculationCount = 0

def ReadFile(filePath, md5Obj):
    BUF_SIZE = 65536
    readingFinished = False

    with open(filePath, 'rb') as file:
                while not readingFinished:
                    data = file.read(BUF_SIZE)
                    
                    if data:
                        md5Obj.update(data)
                    else:
                        readingFinished = True
                
    return md5Obj

def HashFiles(coreN, startIndex, endIndex, filePaths):
    print("Core " + str(coreN) + " starting hashing")

    subFilePathsArr=filePaths[startIndex:endIndex]

    filePathCount=startIndex
    for filePath in subFilePathsArr:
        currentMd5 = hashlib.md5()

        #Read in file
        currentMd5 = ReadFile(filePath, currentMd5)

        #Check hash result
        hashResult = currentMd5.hexdigest()

        #Save to array
        allFileHashes[filePathCount] = hashResult
        filePathCount=filePathCount+1

        #Increment hash calculation count
        ++hashCalculationCount
#__HashFiles_END

#Get no of cores
numCores=multiprocessing.cpu_count()
print("Found " + str(numCores) + " cores")

#Find all files that match this pattern
print("Searching For Files")
allFoundFiles=[]
for root, dir, fileNames in os.walk(walkPath):
    for fileName in fileNames:
            if (searchRegexStr == "*" or re.match(searchRegexStr, fileName)):
                allFoundFiles.append(os.path.join(root, fileName))
                allFileHashes.append(0x0)

fileCount = len(allFoundFiles)
if (fileCount == 0):
    print("No files matching pattern found, exiting..")
    exit()
else:
    print("Found " + str(fileCount) + " files")

#Loop through each core
print("Dividing up files amongst the cores")
filesPerThread=(fileCount/numCores)
coreStartIndex=0
for coreN in range(numCores):

    #Work out the end index allocation of files in the array
    coreEndIndex=int(round((coreN+1)*filesPerThread, 0))

    #Call hashing function with thread
    HashFiles(coreN, coreStartIndex, coreEndIndex, allFoundFiles)

    #Set core start index to end index
    coreStartIndex=coreEndIndex

#Loop through comparing
print("Comparing Hashes")
count = 0
for count in range(fileCount):
    fileA = allFoundFiles[count]
    hashA = allFileHashes[count]

    for count2 in range(count+1, fileCount):
        fileB = allFoundFiles[count2]
        hashB = allFileHashes[count2]

        #If we found a duplicate
        if hashA == hashB:
            print("Duplicate file found { " + fileA + " = " + fileB + " }")

print("Waiting for threads to finish")
while hashCalculationCount < fileCount:
    time.sleep(1)