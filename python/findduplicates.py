#!/usr/bin/python

import FilesHasher
from importlib.resources import read_binary
import os
import re
import multiprocessing
import time
from tokenize import Number

walkPath="/mnt/tmp/"
searchRegexStr="*"

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