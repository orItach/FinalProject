import os
import sys
import time


class Scripts:

    # 26/11/17 Or: glove constant
    VOCAB_FILE = "vocab.txt"
    COOCCURRENCE_FILE = "cooccurrence.bin"
    COOCCURRENCE_SHUF_FILE = "cooccurrence.shuf.bin"
    # BUILDDIR = build
    SAVE_FILE = "vectors"
    VERBOSE = 2
    MEMORY = 4.0
    VOCAB_MIN_COUNT = 1
    VECTOR_SIZE = 50
    MAX_ITER = 15
    WINDOW_SIZE = 15
    BINARY = 2
    NUM_THREADS = 8
    X_MAX = 10

    # 26/11/17 Or: my constant
    # where all glove exes are located
    BasePath = "C:\FinalProject\glove-win_devc_x64"

    def use_vocab_count(self, min_count,verbose,input_file, vocab_file):
        os.system(self.BasePath+"\\vocab_count.exe -min-count " + str(min_count) + " -verbose "
                  + str(verbose)+" <"+str(input_file)+"> " + str(vocab_file))

    def use_cooccur(self,memory,vocab_file, verbose, window_size, input_file,cooccurrence_file):
        print self.BasePath+"\\cooccur.exe -memory " + str(memory) + " -vocab-file " +str(vocab_file) +" -verbose "+str(verbose)+" -window-size " + str(window_size)+" <"+str(input_file)+"> " +str(cooccurrence_file)

        os.system(self.BasePath+"\\cooccur.exe -memory " + str(memory) + " -vocab-file " +str(vocab_file) +" -verbose "+str(verbose)
                  +"-window-size " + str(window_size)+" <"+str(input_file)+"> " +str(cooccurrence_file))

    def use_shuffle(self,memory, verbose,cooccurrence_file,cooccurrence_shuf_file):
        print self.BasePath+"\\shuffle.exe -memory " + str(memory) + " -verbose " + str(verbose) +" <" + str(cooccurrence_file) + "> " + str(cooccurrence_shuf_file)
        os.system(self.BasePath+"\\shuffle.exe -memory " + str(memory) + " -verbose " + str(verbose)+
                   " <" + str(cooccurrence_file) + "> " + str(cooccurrence_shuf_file))

    def use_glove(self, save_file, num_threads,cooccurrence_shuf_file, x_max, max_iter, vector_size, binary,vocab_file,verbose):
        print self.BasePath+"\\glove.exe -save-file " + str(save_file) +" -threads " + str(num_threads) + " -input-file "+ str(cooccurrence_shuf_file)+ " -x-max " +str(x_max)+" -iter " +str(max_iter)+" -vector-size " +str(vector_size)+ " -binary " +str(binary)+" -vocab-file " +str(vocab_file)+" -verbose " + str(verbose)
        os.system(self.BasePath+"\\glove.exe -save-file " + str(save_file) +" -threads " + str(num_threads) + " -input-file "+ str(cooccurrence_shuf_file)+
                 " -x-max " +str(x_max)+" -iter " +str(max_iter)+" -vector-size " +str(vector_size)+ " -binary " +str(binary)+" -vocab-file " +str(vocab_file)+
                 " -verbose " + str(verbose))

    # 26/11/17 Or: look at https://stackoverflow.com/questions/2212643/python-recursive-folder-read
    def porccesFile(self,sourceDirectory,destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            for folder in subFolders:
                # 26/11/17 Or: its the long path to the files
                outfileName= os.path.join(sourceDirectory,folder)
                self.porccesFile(outfileName,destinationDirectory )
                #outfileName = sourceDirectory + "/" + folder + "/py-outfile.txt"  # hardcoded path
                #folderOut = open(outfileName, 'w')
                #print
                #"outfileName is " + outfileName

            # 26/11/17 Or: files are file in root directory
            for currentFile in files:

                if currentFile.endswith(".txt"):
                    fileName= currentFile.split(".")[0]
                    filePath=os.path.join(sourceDirectory,currentFile)
                    print "build Vocab_Count to " + fileName
                    self.use_vocab_count(self.VOCAB_MIN_COUNT, self.VERBOSE, filePath, fileName+"_" + self.VOCAB_FILE)
                    time.sleep(2)
                    print "build Cooccur to " + os.path.join(destinationDirectory,fileName+"_"+self.VOCAB_FILE)
                    temp =  os.path.join(destinationDirectory,fileName+"_"+self.VOCAB_FILE)
                    self.use_cooccur(self.MEMORY,temp, self.VERBOSE,self.WINDOW_SIZE, filePath, fileName+"_"+self.COOCCURRENCE_FILE)
                    time.sleep(2)
                    print "build Shuffle to " + fileName
                    self.use_shuffle(self.MEMORY,self.VERBOSE,os.path.join(fileName+"_"+self.COOCCURRENCE_FILE),os.path.join(fileName+"_"+self.COOCCURRENCE_SHUF_FILE))
                    print "build Glove to " + fileName
                    self.use_glove(fileName+"_"+self.SAVE_FILE,self.NUM_THREADS, os.path.join(fileName+"_"+self.COOCCURRENCE_SHUF_FILE),self.X_MAX, self.MAX_ITER,self.VECTOR_SIZE,self.BINARY,os.path.join(fileName+"_"+self.VOCAB_FILE),self.VERBOSE)
                    # filePath = sourceDirectory + '/' + currentfile
                    #f = open(filePath, 'r')
                    #toWrite = f.read()
                    #print
                    #"Writing '" + toWrite + "' to" + filePath
                    #folderOut.write(toWrite)
                    #f.close()

                #folderOut.close()
        #for filename in os.listdir(sourceDirectory):
        #        if filename.endswith(".txt"):
        #            use_vocab_count(VOCAB_MIN_COUNT,)

    starts = {"יו","את","כב","בד","כד","בש","כו","דא","כל","דב","כמ","דה","כש","די","לד","דל","לכ","דמ","למ","דנ","לש","דת","מו","הא","מכ","הב","מל","הד","הו","נת","הי","שא","הכ","שב","הל","שה","המ","שי","הנ","של","הש","שמ","הת","שנ","וא","שת","וב","תו","וד","תי","וה","וי","וכ","ול","ומ","ונ","וש","ות" }

    def cutStart(self,word):
        for start in self.starts:
            if word[:2] == start:
                if len(word[-len(word-2):])>3:
                    return word[-len(word-2):]


    def cutEnd(self, word):
        for end in self.starts:
            if word[:2] == end:
                if len(word[-len(word-2):])>3:
                    return word[-len(word-2):]

    def getMinWord(self, word):
        word ="c"

    def readFile(self, fileName):
        for line in open(fileName,"r"):
            for word in line.split():
                resultWithEnd = self.cutStart(word)
                resultWitoutStart= self.cutEnd(resultWithEnd)
                resultWithStart =self.cutEnd(word)
                # write resultWithStart to file
                if resultWitoutStart == "":
                    continue
                # write resultWitoutStart to file

Scripts().porccesFile( "C:\FinalProject\clean_shut_B4_replace", "C:\FinalProject\pyhonScripts")
# Scripts().use_cooccur(4.0, "C:\\FinalProject\\pyhonScripts\\10A_vocab.txt", 2,
#                 15, "C:\\FinalProject\\clean_shut_B4_replace\\abdalla_somech\\10A.txt", "10A" + "_" + "cooccurrence.bin")
