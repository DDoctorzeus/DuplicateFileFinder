
import hashlib
import threading

class FilesHasher (threading.Thread):
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
            currentMd5 = FilesHasher.ReadFile(filePath, currentMd5)

            #Check hash result
            hashResult = currentMd5.hexdigest()

            #Save to array
            FilesHasher.allFileHashes[filePathCount] = hashResult
            filePathCount=filePathCount+1

            #Increment hash calculation count
            ++FilesHasher.hashCalculationCount
    #__HashFiles_END