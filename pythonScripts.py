# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
import shutil
import sys
import time

import errno

import io
import datetime
import re
import math

import itertools

from scipy import stats
from decimal import Decimal
#reload(sys)
#sys.setdefaultencoding('utf8')

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
    VECTOR_SIZE = 200
    MAX_ITER = 30
    WINDOW_SIZE = 8
    BINARY = 2
    NUM_THREADS = 8
    X_MAX = 10

    # 26/11/17 Or: my constant
    # where all glove exes are located
    BasePath = "C:\FinalProject\glove-win_devc_x64"

    # maybe- need to check input file its the original file
    def use_vocab_count(self, min_count, verbose, input_file, vocab_file):
        os.system(self.BasePath + "\\vocab_count.exe -min-count " + str(min_count) + " -verbose "
                  + str(verbose) + " <" + str(input_file) + "> " + str(vocab_file))

    def use_cooccur(self, memory, vocab_file, verbose, window_size, input_file, cooccurrence_file):
        print(self.BasePath + "\\cooccur.exe -memory " + str(memory) + " -vocab-file " + str(
            vocab_file) + " -verbose " + str(verbose) + " -window-size " + str(window_size) + " <" + str(
            input_file) + "> " + str(cooccurrence_file))

        os.system(self.BasePath + "\\cooccur.exe -memory " + str(memory) + " -vocab-file " + str(
            vocab_file) + " -verbose " + str(verbose)
                  + "-window-size " + str(window_size) + " <" + str(input_file) + "> " + str(cooccurrence_file))

    def use_shuffle(self, memory, verbose, cooccurrence_file, cooccurrence_shuf_file):
        print(self.BasePath + "\\shuffle.exe -memory " + str(memory) + " -verbose " + str(verbose) + " <" + str(
            cooccurrence_file) + "> " + str(cooccurrence_shuf_file))
        os.system(self.BasePath + "\\shuffle.exe -memory " + str(memory) + " -verbose " + str(verbose) +
                  " <" + str(cooccurrence_file) + "> " + str(cooccurrence_shuf_file))

    def use_glove(self, save_file, num_threads, cooccurrence_shuf_file, x_max, max_iter, vector_size, binary,
                  vocab_file, verbose):
        print(self.BasePath + "\\glove.exe -save-file " + str(save_file) + " -threads " + str(
            num_threads) + " -input-file " + str(cooccurrence_shuf_file) + " -x-max " + str(x_max) + " -iter " + str(
            max_iter) + " -vector-size " + str(vector_size) + " -binary " + str(binary) + " -vocab-file " + str(
            vocab_file) + " -verbose " + str(verbose))
        os.system(self.BasePath + "\\glove.exe -save-file " + str(save_file) + " -threads " + str(
            num_threads) + " -input-file " + str(cooccurrence_shuf_file) +
                  " -x-max " + str(x_max) + " -iter " + str(max_iter) + " -vector-size " + str(
            vector_size) + " -binary " + str(binary) + " -vocab-file " + str(vocab_file) +
                  " -verbose " + str(verbose))

    # 26/11/17 Or: look at https://stackoverflow.com/questions/2212643/python-recursive-folder-read
    def porccesFile(self, sourceDirectory, destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            for folder in subFolders:
                # 26/11/17 Or: its the long path to the files
                newSourceDirectory = os.path.join(sourceDirectory, folder)
                newDestinationDirectory = os.path.join(destinationDirectory, folder)
                print(newDestinationDirectory)
                Utils().ensure_dir(newDestinationDirectory)
                self.porccesFile(newSourceDirectory, newDestinationDirectory)

            # 26/11/17 Or: files are file in root directory
            for currentFile in files:
                if currentFile.endswith(".txt"):
                    fileName = currentFile.split(".")[0]
                    filePath = os.path.join(sourceDirectory, currentFile)
                    destVocabFilePath = os.path.join(destinationDirectory,fileName+"_"+self.VOCAB_FILE)
                    print("build Vocab_Count to " + fileName)
                    self.use_vocab_count(self.VOCAB_MIN_COUNT, self.VERBOSE, filePath,destVocabFilePath) #ileName + "_" + self.VOCAB_FILE)
                    print("build Cooccur to " + os.path.join(destinationDirectory, fileName + "_" + self.VOCAB_FILE))
                    destCooccurFilePath = os.path.join(destinationDirectory, fileName + "_" + self.COOCCURRENCE_FILE)
                    self.use_cooccur(self.MEMORY, destVocabFilePath, self.VERBOSE, self.WINDOW_SIZE, filePath,
                                     destCooccurFilePath)#fileName + "_" + self.COOCCURRENCE_FILE)
                    print("build Shuffle to " + fileName)
                    destShuffleFilePath = os.path.join(destinationDirectory, fileName + "_" + self.COOCCURRENCE_SHUF_FILE)
                    self.use_shuffle(self.MEMORY, self.VERBOSE, destCooccurFilePath,#os.path.join(fileName + "_" + self.COOCCURRENCE_FILE),
                                     destShuffleFilePath)#os.path.join(fileName + "_" + self.COOCCURRENCE_SHUF_FILE))
                    print("build Glove to " + fileName)
                    destGloveFilePath = os.path.join(destinationDirectory, fileName + "_" + self.SAVE_FILE)
                    self.use_glove(destGloveFilePath, self.NUM_THREADS,
                                   destShuffleFilePath, self.X_MAX,
                                   self.MAX_ITER, self.VECTOR_SIZE, self.BINARY,
                                   destVocabFilePath, self.VERBOSE)
                    # filePath = sourceDirectory + '/' + currentfile
                    # f = open(filePath, 'r')
                    # toWrite = f.read()
                    # print
                    # "Writing '" + toWrite + "' to" + filePath
                    # folderOut.write(toWrite)
                    # f.close()

                # folderOut.close()
        # for filename in os.listdir(sourceDirectory):
        #        if filename.endswith(".txt"):
        #            use_vocab_count(VOCAB_MIN_COUNT,)

    # start resioyt and sefiyot
    #starts = {"יו": 0, "את": 0, "כב": 0, "בד": 0, "כד": 0, "בש": 0, "כו": 0, "דא": 0, "כל": 0, "דב": 0, "כמ": 0,
    #          "דה": 0, "כש": 0, "די": 0, "לד": 0, "דל": 0, "לכ": 0, "דמ": 0, "למ": 0, "דנ": 0, "לש": 0, "דת": 0,
    #          "מו": 0, "הא": 0, "מכ": 0, "הב": 0, "מל": 0, "הד": 0, "הו": 0, "נת": 0, "הי": 0, "שא": 0, "הכ": 0,
    #          "שב": 0, "הל": 0, "שה": 0, "המ": 0, "שי": 0, "הנ": 0, "של": 0, "הש": 0, "שמ": 0, "הת": 0, "שנ": 0,
    #          "וא": 0, "שת": 0, "וב": 0, "תו": 0, "וד": 0, "תי": 0, "וה": 0, "וי": 0, "וכ": 0, "ול": 0, "ומ": 0,
    #          "ונ": 0, "וש": 0, "ות": 0}
    #ends = {"אה": 0, "או": 0, "אי": 0, "כך": 0, "אין": 0, "כל": 0, "אם": 0, "כם": 0, "אן": 0, "לא": 0, "אני": 0,
    #        "לאו": 0, "את": 0, "לה": 0, "בה": 0, "לו": 0, "בו": 0, "לי": 0, "בי": 0, "לך": 0, "בין": 0, "לכך": 0,
    #        "בך": 0, "בכל": 0, "בת": 0, "מה": 0, "הו": 0, "מו": 0, "הוא": 0, "מי": 0, "הוה": 0, "נא": 0, "הם": 0,
    #        "נה": 0, "הן": 0, "נו": 0, "התם": 0, "ני": 0, "וי": 0, "וך": 0, "ןת": 0, "זה": 0, "זן": 0, "טעם": 0,
    #        "יה": 0, "שם": 0, "יו": 0, "תא": 0, "יי": 0, "תה": 0, "יך": 0, "תוך": 0, "ים": 0, "תי": 0, "תך": 0,
    #        "ית": 0, "תם": 0, "כדי": 0, "תן": 0}

    def cutStart(self, word):
        for start in self.starts:
            if word[:len(start)] == start:
                if len(word[-len(word - len(start)):]) > 3:
                    return word[-len(word - len(start)):]

    def cutEnd(self, word):
        for end in self.starts:
            if word[:len(end)] == end:
                if len(word[-len(word - len(end)):]) > 3:
                    return word[-len(word - len(end)):]

    def getMinWord(self, word):
        word = "c"

    def readFile(self, fileName, detFileName):
        for line in open(fileName, "r"):
            for word in line.split():
                resultWithEnd = self.cutStart(word)
                resultWitoutStart = self.cutEnd(resultWithEnd)
                resultWithStart = self.cutEnd(word)
                # write resultWithStart to file
                if len(resultWithEnd) == 3:
                    result = resultWithEnd
                elif len(resultWithStart) == 3:
                    result = resultWithStart
                elif len(resultWitoutStart) == 3:
                    result = resultWitoutStart
                with open(detFileName, 'a') as the_file:
                    the_file.write(result + "\n")
                # write result to file

    # heartWord is the 3 len word
    def secondReadFile(self, fileName, heartWord, detFileName):
        for line in open(fileName, "r"):
            for word in line.split():
                if heartWord in word:
                    with open(detFileName, 'a') as the_file:
                        the_file.write(word + "\n")
                        # write to file

    def bigSecondReadFile(self, fileName, heartWordFileName, detFileName):
        for line in open(heartWordFileName, "r"):
            for word in line.split():
                self.secondReadFile(fileName, word, detFileName)

    def allReadFile(self, sourceDirectory, destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            for folder in subFolders:
                # 26/11/17 Or: its the long path to the files
                outfileName = os.path.join(sourceDirectory, folder)
                self.porccesFile(outfileName, destinationDirectory)

            # 26/11/17 Or: files are file in root directory
            for currentFile in files:
                if currentFile.endswith(".txt"):
                    fileName = currentFile.split(".")[0]
                    filePath = os.path.join(sourceDirectory, currentFile)
                    self.readFile(filePath, "heartWord" + fileName)

    # here we start code about tagger
    PATH_TO_TAGGER = "java -Xmx1G -cp C:\\FinalProject\\tagger\\trove-2.0.2.jar;C:\\FinalProject\\tagger\\morphAnalyzer.jar;C:\\FinalProject\\tagger\\opennlp.jar;C:\\FinalProject\\tagger\\gnu.jar;C:\\FinalProject\\tagger\\chunker.jar;C:\\FinalProject\\tagger\\splitsvm.jar;C:\\FinalProject\\tagger\\duck1.jar;C:\\FinalProject\\tagger\\tagger.jar;C:\\FinalProject\\tagger\\. NewDemo C:\FinalProject\\tagger\\"

    def use_tagger(self, inputFilePath, outputFilePath):
        print(self.PATH_TO_TAGGER + " " + inputFilePath + " " + outputFilePath)
        os.system(self.PATH_TO_TAGGER + " " + inputFilePath + " " + outputFilePath)

        # 1 for start dict
    def handleLine(self, line, start):
        try:
            words = line.split(" ")
            if (words[1] != 'None\n') and (start == 1):
                if words[1] in self.starts:
                    self.starts[words[1]] = self.starts[words[1]] + 1
            if (words[1] != 'None\n') and (start == 0):
                if words[1] in self.ends:
                    self.ends[words[1]] = self.ends[words[1]] + 1
        except:
            print("error in handelLine function line is: " + line)

    def handleTaggerOutput(self, fileName):
        for line in open(fileName, "r"):
            if "Prefixes" in line:
                self.handleLine(line, 1)
            if "Suffix" in line:
                self.handleLine(line, 0)

    def writeDicnaryToFile(self, outputFilePath):
        with open(outputFilePath, 'r') as file:
            file.write(str(self.starts))
            file.write(str(self.ends))

    def ensure_dir(self, filePath):
        print("ensure_dir been caled "+filePath)
        #directory = os.path.dirname(filePath)
        #if not os.path.exists(directory):
        #    os.makedirs(directory)
        try:
            os.makedirs(filePath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def proccesTaggerFile(self, sourceDirectory, destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            #for folder in subFolders:
            #    # 26/11/17 Or: its the long path to the files
            #    outfileName = os.path.join(sourceDirectory, folder)
            #    desFilePath = os.path.join(destinationDirectory, folder)
            #    self.ensure_dir(desFilePath)
            #    self.proccesTaggerFile(outfileName, desFilePath)
                # outfileName = sourceDirectory + "/" + folder + "/py-outfile.txt"  # hardcoded path
                # folderOut = open(outfileName, 'w')
                # print
                # "outfileName is " + outfileName

            # 26/11/17 Or: files are file in root directory
            try:
                for currentFile in files:
                    if currentFile.endswith(".txt"):
                        fileName = currentFile.split(".")[0]
                        if "taggerInput" in fileName and not ("taggerOutput" in fileName):
                            filePath = os.path.join(sourceDirectory, currentFile)
                            outputFilePath = os.path.join(destinationDirectory,fileName+"_taggerOutput"+".txt")
                            print("build tagger file " + fileName + " time is: "+datetime.datetime.now())
                            time.sleep(10)
                            self.use_tagger(filePath, outputFilePath)
                            # maybe not so good
                            self.handleTaggerOutput(outputFilePath)
            except :
                print ("some error oucred   " +fileName)
            else:
                self.writeDicnaryToFile("C:\\FinalProject\\resultDicnary.txt")
                print(str(self.starts))
                print(str(self.ends))

    def copyDataSet(self, sourceDirectory, destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            for folder in subFolders:
                # 26/11/17 Or: its the long path to the files
                outfilePath = os.path.join(sourceDirectory, folder)
                desFilePath = os.path.join(destinationDirectory, folder)
                self.copyDataSet(outfilePath, destinationDirectory)
                #self.ensure_dir(desFilePath)
                #self.proccesTaggerFile(outfileName, desFilePath)
            # 26/11/17 Or: files are file in root directory
            for currentFile in files:
                if currentFile.endswith(".txt"):
                    fileName = currentFile.split(".")[0]
                    filePath = os.path.join(sourceDirectory, currentFile)
                    #print("!!!" + os.pardir)
                    #parantFolderName =  os.path.abspath(os.path.join(os.path.join(sourceDirectory, currentFile), os.pardir))

                    #print(filePath+"!!!"+filePath.split("\\")[3])
                    fileName = fileName + "_"+"taggerInput"+"_"+filePath.split("\\")[3]#+ parantFolderName

                    outputFilePath = os.path.join(destinationDirectory, fileName + ".txt")
                    print ("copy DataSetFile: " + fileName)
                    shutil.copyfile(filePath, outputFilePath)


# Scripts().use_tagger("C:\\FinalProject\\tagger\\exs1.txt", "C:\\FinalProject\\tagger\\exs1PythonOut.txt")
#Scripts().handelTaggerOutput("C:\\FinalProject\\tagger\\exs1PythonOut.txt")
#Scripts().proccesTaggerFile("C:\\FinalProject\\tagger","C:\\FinalProject\\tagger")
#Scripts().copyDataSet("C:\\FinalProject\\clean_shut_B4_replace","C:\\FinalProject\\tagger")
#Scripts().porccesFile( "C:\FinalProject\wiki_head&tail_output", "C:\FinalProject\wiki_head&tail_glove_output")
# Scripts().use_cooccur(4.0, "C:\\FinalProject\\pyhonScripts\\10A_vocab.txt", 2,
#                 15, "C:\\FinalProject\\clean_shut_B4_replace\\abdalla_somech\\10A.txt", "10A" + "_" + "cooccurrence.bin")

#arrange code 01/03/18
class PreProcces:
    # <editor-fold desc="Glove">
    # </editor-fold>


    # <editor-fold desc="Tagger">
    def reqConvertFile2UTF8(self,sourceDirectory,destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            #try:
                for folder in subFolders:
                    print(folder)
                #    # 26/11/17 Or: its the long path to the files
                    newSourceDirectory = os.path.join(sourceDirectory, folder)
                    newDestinationDirectory = os.path.join(destinationDirectory, folder)
                    print(newDestinationDirectory)
                    Utils().ensure_dir(newDestinationDirectory)
                    self.reqConvertFile2UTF8(newSourceDirectory,newDestinationDirectory)
                # 26/11/17 Or: files are file in root directory
                for currentFile in files:
                    print(currentFile)
                    if currentFile.endswith(".txt"):
                        fileName = currentFile.split(".")[0]
                        content = io.open(sourceDirectory+"\\"+currentFile, 'r').read()

                        newContent = ""
                        try:
                            with io.open(sourceDirectory+"\\"+currentFile, 'r') as sourceFile:
                                for line in sourceFile:
                                    for word in line.split():
                                        newContent =+ " " +unicode(word).encode("utf-8")
                        except:
                            print("some thing get wrong word: "+ word + "file name: "+currentFile)
                        io.open(destinationDirectory+"\\"+currentFile, "w" ,encoding="utf-8").write(unicode(newContent,"utf-8"))
            #except:
                print("something get wrong folder: " )

    def genrateTaggerFile(self, sourceDirectory, destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            for folder in subFolders:
               # 26/11/17 Or: its the long path to the files
               newSourceDirectory = os.path.join(sourceDirectory, folder)
               newDestinationDirectory = os.path.join(destinationDirectory, folder)
               Utils().ensure_dir(newDestinationDirectory)
               self.genrateTaggerFile(newSourceDirectory, newDestinationDirectory)
            # 26/11/17 Or: files are file in root directory
            try:
                for currentFile in files:
                    if currentFile.endswith(".txt"):
                        fileName = currentFile.split(".")[0]
                        outputFilePath = os.path.join(destinationDirectory, fileName  + ".txt")
                        print("build tagger file " + fileName)
                        filePath = os.path.join(sourceDirectory, currentFile)
                        self.use_tagger(filePath, outputFilePath)
                        # maybe not so good
                        #self.handleTaggerOutput(outputFilePath)
            except:
                print ("some error oucred   " + fileName)
            #else:
                #self.writeDicnaryToFile("C:\\FinalProject\\resultDicnary.txt")
                #print(str(self.starts))
                #print(str(self.ends))

    PATH_TO_TAGGER = "java -Xmx2G -cp C:\\FinalProject\\tagger\\trove-2.0.2.jar;C:\\FinalProject\\tagger\\morphAnalyzer.jar;C:\\FinalProject\\tagger\\opennlp.jar;C:\\FinalProject\\tagger\\gnu.jar;C:\\FinalProject\\tagger\\chunker.jar;C:\\FinalProject\\tagger\\splitsvm.jar;C:\\FinalProject\\tagger\\duck1.jar;C:\\FinalProject\\tagger\\tagger.jar;C:\\FinalProject\\tagger\\tagger.orig.jar;C:\\FinalProject\\tagger\\. NewDemo C:\FinalProject\\tagger\\"

    def use_tagger(self, inputFilePath, outputFilePath):
        print(self.PATH_TO_TAGGER + " " + inputFilePath + " " + outputFilePath)
        os.system(self.PATH_TO_TAGGER + " " + inputFilePath + " " + outputFilePath)

    def test(self):
        x = 5

    # </editor-fold>
#not in use, don't use it
class BuildDataSet:

    lemmaRegex = "[ ]+Lemma:[ ]+ [א-ת]^+[א-ת]+"
    originalRegex = "*[א-ת]"
    def genStimingFile(self,sourceDirectory,destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            try:
                for folder in subFolders:
                    print(folder)
                #    # 26/11/17 Or: its the long path to the files
                    newSourceDirectory = os.path.join(sourceDirectory, folder)
                    newDestinationDirectory = os.path.join(destinationDirectory, folder)
                    print(newDestinationDirectory)
                    Utils().ensure_dir(newDestinationDirectory)
                    self.genStimingFile(newSourceDirectory,newDestinationDirectory)
                # 26/11/17 Or: files are file in root directory
                for currentFile in files:
                    print(currentFile)
                    if currentFile.endswith(".txt"):
                        regex = BuildDataSet().lemmaRegex
                        contentResult =""
                        for line in  open(currentFile, "r"):
                            if "Lemma" in line:
                                regexResult = re.search(regex,line)
                                if regexResult:
                                    stimResult = regexResult.group()[0]
                                    contentResult += stimResult+" "
                        print("build stiming file " + currentFile + " time is: "+ datetime.datetime.now())
                        io.open(destinationDirectory+"\\"+currentFile, "w" ,encoding="utf-8").write(contentResult)#unicode(contentResult,"utf-8"))
                        #fileName = currentFile.split(".")[0]
                        #outputFilePath = os.path.join(destinationDirectory, fileName + ".txt")
                        #filePath = os.path.join(sourceDirectory, currentFile)
                        #self.use_tagger(filePath, outputFilePath)
            except:
                print("something get wrong folder: " )

    def genWitoutHeaderAndTailFile(self,sourceDirectory,destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            #try:
                for folder in subFolders:
                    print(folder)
                #    # 26/11/17 Or: its the long path to the files
                    newSourceDirectory = os.path.join(sourceDirectory, folder)
                    newDestinationDirectory = os.path.join(destinationDirectory, folder)
                    print(newDestinationDirectory)
                    Utils().ensure_dir(newDestinationDirectory)
                    self.genWitoutHeaderAndTailFile(newSourceDirectory,newDestinationDirectory)
                # 26/11/17 Or: files are file in root directory
                for currentFile in files:
                    print("currenFiles:"+currentFile+" currentFolder: "+str(subFolders))
                    if currentFile.endswith(".txt"):
                        originalRegex = BuildDataSet().originalRegex
                        lemmaRegex = BuildDataSet().lemmaRegex
                        originalWord=""
                        lemmaWord =""
                        contentResult =""
                        WithoutHeadAndTailResult=""
                        with io.open(sourceDirectory + "\\" + currentFile, 'r', encoding="utf8") as sourceFile:
                            for line in sourceFile:
                                line = line.strip('\n')
                                line = line.strip('\t')
                                if line.isalpha():
                                    originalWord = line
                                    lemmaWord=""
                                matchObj = re.match(r'Lemma: ([א-ת]*)(.*)', line,re.M|re.I)
                                if matchObj:
                                    lemmaWord= matchObj.group(2).replace("^",""),
                                if "Lemma:" in line:
                                    tempLine = line.encode("utf-8")
                                    lemmaWord = BuildDataSet().getLemmaFromLine(tempLine)
                                #print(matchObj.group())
                                #if matchObj.group(1):
                                #    print("1", matchObj.group(1))
                                #if matchObj.group(2):
                                #    print("2", matchObj.group(2))
                                #if matchObj.group(0):
                                #    print("0", matchObj.group(0))
                                #temp = matchObj.group(2)
                                #print temp
                                ##matchObj = re.search(r'Lemma: [א-ת]^\)*[א-ת]+\)*', line)
                                ##temp = 'Lemma: [א-ת]*(^[א-ת])+'
                                ##temp = 'Lemma: [\u0590-\u05fe]+(\^[\u0590-\u05fe]+)*'
                                ##unicode(line,"unicode-1-1-utf-7")
                                ##matchObj = re.match('Lemma: [\u0590-\u05fe]*(^[\u0590-\u05fe]+)*',line)
                                #if matchObj:
                                #    print "match --> matchObj.group() : ", matchObj.group()
                                #    if matchObj.group(1):
                                #        print("ddf", matchObj.group(1))
                                #else:
                                #    print "No match!!"
                                ##originalRegexResult = re.search(r'originalRegex',line)
                                ##if originalRegexResult:
                                ##    originalWord = originalRegexResult.group()[0]
                                #lemmaRegexResult = re.match(lemmaRegex,line)
                                #if lemmaRegexResult:
                                #    lemmaWord = lemmaRegexResult.group(0)

                                if lemmaWord != "":
                                    start, newOriginal, end = BuildDataSet().generateSplittedWord(originalWord.encode("utf-8"),lemmaWord)
                                    contentResult = start+ " " + newOriginal + " " + end
                                    io.open(destinationDirectory + "\\" + currentFile, "w").write(contentResult.decode("utf-8"))
                                    x =5
                                else:
                                    print(lemmaWord+ " "+ originalWord)
                            print("build stiming file " + currentFile + " time is: "+ str(datetime.datetime.now()))
                            outputFilePath = os.path.join(destinationDirectory, currentFile)
                            io.open(destinationDirectory+"\\"+currentFile, "w" ,encoding="utf-8").write(unicode(contentResult,"utf-8"))
                        #fileName = currentFile.split(".")[0]
                        #outputFilePath = os.path.join(destinationDirectory, fileName + ".txt")
                        #filePath = os.path.join(sourceDirectory, currentFile)
                        #self.use_tagger(filePath, outputFilePath)
            #except:
            #    print("something get wrong : ")

    def generateSplittedWord(self,original, lemme):
        start="false"
        end="false"
        newOriginal=""
        try:
            tempStart = BuildDataSet().getStart(lemme[0], original)
            if tempStart == "false":
                tempStart = BuildDataSet().getStart(lemme[1], original)
                if tempStart == "false":
                    print("error in split word,couldn't get start, the original is:" + original + "the lemme is:" + lemme)
            start = tempStart
            #[begin:end:step]
            tempEnd = BuildDataSet().getEnd(lemme[len(lemme)-1],original[::-1])
            if tempEnd == "false":
                tempEnd = BuildDataSet().getEnd(lemme[len(lemme)-2],original[::-1])
                if tempEnd == "false":
                    print("error in split word, couldn't get end, the original is:" + original + " the lemme is:" + lemme)
            end = tempEnd
            #print(end.encode('utf-8').strip())
            #print(unicode(end).encode('utf8'))
        except:
            print("error in word "+original)
        if start == "false" and end == "false":
            print("error in get start and end")
            return "", original, ""
        if start != "false" and end != "false":
            t0= original[1:2]
            t3 = str(original[2:3])
            print("t3, ",t3)
            t=original[len(start):]
            t1= original[:len(end)]
            t2 = original[len(end):len(start)]
            return start, original[len(start):len(end)], end
        if end != "false":
            return "", original[:len(end)], end
        if start != "false":
            return start, original[len(start):], ""
        print("weired error")

    #endCharT
    def parseToUTF8(self,word):
        result = ""
        for char in word:
            try:
                result += word#unicode(word).encode("utf-8")
            except:
                print("error in ")

    #return false or the start
    def getStart(self,startChar,original):
        foundPosition=-1
        for firstCharLocation in range(0,2):
            if original[firstCharLocation] == startChar:
                if firstCharLocation>foundPosition:
                    foundPosition= firstCharLocation
        if foundPosition == -1:
            return "false"
        else:
            return original[:firstCharLocation]

    def getEnd(self,endChar,originalReversd):
        foundPosition=-1
        for endCharLocation in range(0,2):
            if originalReversd[endCharLocation] == endChar:
                if endCharLocation>foundPosition:
                    foundPosition= endCharLocation
        if foundPosition==-1:
            return "false"
        else:
            return originalReversd[:foundPosition]

    def getLemmaFromLine(self,line):
        if "^" in line:
            theWord= line.split(":")[1]
            result = theWord.split("^")[1].strip()
            return result
        else:
            return line.split(":")[1].strip()

class Utils:
    def ensure_dir(self, filePath):
        print("ensure_dir been caled "+filePath)
        #directory = os.path.dirname(filePath)
        #if not os.path.exists(directory):
        #    os.makedirs(directory)
        try:
            os.makedirs(filePath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def buildVector(self,line):
        currentVector = []
        for word in line.split():
            if word.isalpha()  :
                continue
            else:
                try:
                    currentVector.append(float(word.replace("]","").replace("[","").replace(",","")))
                except:
                    print("error to convert to float: "+ word)
        return  currentVector

    def readVectorToDictionary(self,sourceFilePath):
        with io.open(sourceFilePath, 'r',encoding="utf-8") as sourceFile:
            resultDict={}
            for line in sourceFile:
                currentWord=line.split()[0]
                resultDict[currentWord] = Utils().buildVector(line)
        return resultDict

class assemble:

    def basicAvarge(self,firstVector, secondVector, thirdVector):
        result =[]
        for a, b, c in itertools.izip(firstVector, secondVector, thirdVector):
            result.append(((a+b+c)/3))
        return result

    def basicAvarge2(self,firstVector, secondVector):
        result =[]
        for a, b in itertools.izip(firstVector, secondVector):
            result.append(((a+b)/2))
        return result

    def weightedAverage(self,firstVector,secondVector,thirdVector):
        result = []
        currentSum =1
        for a, b, c in itertools.izip(firstVector, secondVector, thirdVector):
            currentSum = a+b+c
            aPart = a/currentSum
            bPart = b/currentSum
            cPart = c/currentSum
            result.append((a*aPart + b*bPart + c*cPart) /(aPart+bPart+cPart) )
        return result

    def weightedAverage2(self,firstVector,secondVector):
        result = []
        currentSum =1
        for a, b in itertools.izip(firstVector, secondVector):
            currentSum = a+b
            aPart = a/currentSum
            bPart = b/currentSum
            result.append((a*aPart + b*bPart) /(aPart+bPart) )
        return result

    def sum(self,firstVector,secondVector,thirdVector):
        result = []
        for a, b, c in itertools.izip(firstVector, secondVector, thirdVector):
            result.append((a + b + c))
        return result

    def sum2(self,firstVector,secondVector):
        result = []
        for a, b in itertools.izip(firstVector, secondVector):
            result.append((a + b))
        return result

    def processFileAssembleBasicAvarge(self,sourceDirectory, destinationDirectory,vectorSourceDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            for folder in subFolders:
                # 26/11/17 Or: its the long path to the files
                newSourceDirectory = os.path.join(sourceDirectory, folder)
                newDestinationDirectory = os.path.join(destinationDirectory, folder)
                newVectorSourceDir =  os.path.join(vectorSourceDirectory, folder)
                #print(newDestinationDirectory)
                Utils().ensure_dir(newDestinationDirectory)
                #print("newVectorSourceDir "+newVectorSourceDir)
                self.processFileAssembleBasicAvarge(newSourceDirectory, newDestinationDirectory,newVectorSourceDir)

            # 26/11/17 Or: files are file in root directory
            for currentFile in files:
                if currentFile.endswith(".txt"):
                    start=""
                    middle =""
                    end =""
                    numberOfParts=0
                    inMiddle = False
                    fileName = currentFile.split(".")[0]
                    filePath = os.path.join(sourceDirectory, currentFile)
                    vectorFilePath = os.path.join(vectorSourceDirectory,fileName+"_"+Scripts().SAVE_FILE+".txt")
                    #print("vectorSourceDirectory "+ vectorSourceDirectory)
                    #print("vectorFilePath "+vectorFilePath)
                    try:
                        currentVectorFileDict = self.readVectorToDictionary(vectorFilePath)
                    except:
                        continue
                    destFilePath = os.path.join(destinationDirectory,fileName+".txt")
                    with io.open(filePath, 'r',encoding="utf-8") as sourceFile:
                        with io.open(destFilePath,'w',encoding="utf-8") as desFile:
                            for line in sourceFile:
                                for word in line.split():
                                    try:
                                        if "^$" in word:
                                            if numberOfParts==0:
                                                start = word
                                            if numberOfParts == 1:
                                                middle = word
                                            numberOfParts=numberOfParts+1
                                            inMiddle = True
                                        elif "^&" in word:
                                            if numberOfParts==1:
                                                middle = word
                                            if numberOfParts==2:
                                                end = word
                                            numberOfParts=0
                                            tempStart = start.replace("^$","")
                                            tempMiddle = middle.replace("^$","")
                                            tMiddle = tempMiddle.replace("^&","")
                                            tempEnd = end.replace("^&","")
                                            if tempStart=="" or tempStart is None or tempStart=='':
                                                if tempEnd =="" or tempEnd=='':
                                                    assembledVector = currentVectorFileDict[tMiddle]
                                                else:
                                                    assembledVector =self.basicAvarge2(currentVectorFileDict[tempEnd],currentVectorFileDict[tMiddle])
                                            elif tempEnd =="" or tempEnd=='':
                                                if tMiddle =="" or tMiddle=='':
                                                    assembledVector = currentVectorFileDict[tempStart]
                                                else:
                                                    assembledVector = self.basicAvarge2(currentVectorFileDict[tempStart],
                                                                                        currentVectorFileDict[tMiddle])
                                                #assembledVector = self.basicAvarge2(currentVectorFileDict[tempStart],currentVectorFileDict[tMiddle])
                                            elif tMiddle=="" or tMiddle=='':
                                                if tempEnd =="" or tempEnd=='':
                                                    assembledVector = currentVectorFileDict[tempStart]
                                                else:
                                                    assembledVector = self.basicAvarge2(currentVectorFileDict[tempStart],
                                                                                        currentVectorFileDict[tempEnd])
                                            else:
                                                assembledVector = self.basicAvarge(currentVectorFileDict[tempStart],currentVectorFileDict[tMiddle],currentVectorFileDict[tempEnd])
                                            assembledWord = tempStart+tMiddle+tempEnd
                                            desFile.write(assembledWord+" "+str(assembledVector)+"\n")
                                            start=""
                                            middle = ""
                                            end =""
                                        else:
                                            desFile.write(word+" "+ str(currentVectorFileDict[word])+"\n")
                                    except Exception as e:
                                        print("error in assemble word " + word)
                                        print(e)

    def processFileAssembleWeightedAverage(self,sourceDirectory, destinationDirectory,vectorSourceDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            for folder in subFolders:
                # 26/11/17 Or: its the long path to the files
                newSourceDirectory = os.path.join(sourceDirectory, folder)
                newDestinationDirectory = os.path.join(destinationDirectory, folder)
                newVectorSourceDir =  os.path.join(vectorSourceDirectory, folder)
                #print(newDestinationDirectory)
                Utils().ensure_dir(newDestinationDirectory)
                #print("newVectorSourceDir "+newVectorSourceDir)
                self.processFileAssembleWeightedAverage(newSourceDirectory, newDestinationDirectory,newVectorSourceDir)

            # 26/11/17 Or: files are file in root directory
            for currentFile in files:
                if currentFile.endswith(".txt"):
                    start=""
                    middle =""
                    end =""
                    numberOfParts=0
                    inMiddle = False
                    fileName = currentFile.split(".")[0]
                    filePath = os.path.join(sourceDirectory, currentFile)
                    vectorFilePath = os.path.join(vectorSourceDirectory,fileName+"_"+Scripts().SAVE_FILE+".txt")
                    destFilePath = os.path.join(destinationDirectory,fileName+".txt")
                    #print("vectorSourceDirectory "+ vectorSourceDirectory)
                    #print("vectorFilePath "+vectorFilePath)
                    try:
                        currentVectorFileDict = Utils().readVectorToDictionary(vectorFilePath)
                    except:
                        continue
                    with io.open(filePath, 'r',encoding="utf-8") as sourceFile:
                        with io.open(destFilePath,'w',encoding="utf-8") as desFile:
                            for line in sourceFile:
                                for word in line.split():
                                    try:
                                        if "^$" in word:
                                            if numberOfParts==0:
                                                start = word
                                            if numberOfParts == 1:
                                                middle = word
                                            numberOfParts=numberOfParts+1
                                            inMiddle = True
                                        elif "^&" in word:
                                            if numberOfParts==1:
                                                middle = word
                                            if numberOfParts==2:
                                                end = word
                                            numberOfParts=0
                                            tempStart = start.replace("^$","")
                                            tempMiddle = middle.replace("^$","")
                                            tMiddle = tempMiddle.replace("^&","")
                                            tempEnd = end.replace("^&","")
                                            if tempStart=="" or tempStart is None or tempStart=='':
                                                if tempEnd =="" or tempEnd=='':
                                                    assembledVector = currentVectorFileDict[tMiddle]
                                                else:
                                                    assembledVector =self.weightedAverage2(currentVectorFileDict[tempEnd],currentVectorFileDict[tMiddle])
                                            elif tempEnd =="" or tempEnd=='':
                                                if tMiddle =="" or tMiddle=='':
                                                    assembledVector = currentVectorFileDict[tempStart]
                                                else:
                                                    assembledVector = self.weightedAverage2(currentVectorFileDict[tempStart],
                                                                                        currentVectorFileDict[tMiddle])
                                                #assembledVector = self.basicAvarge2(currentVectorFileDict[tempStart],currentVectorFileDict[tMiddle])
                                            elif tMiddle=="" or tMiddle=='':
                                                if tempEnd =="" or tempEnd=='':
                                                    assembledVector = currentVectorFileDict[tempStart]
                                                else:
                                                    assembledVector = self.weightedAverage2(currentVectorFileDict[tempStart],
                                                                                        currentVectorFileDict[tempEnd])
                                            else:
                                                assembledVector = self.weightedAverage(currentVectorFileDict[tempStart],currentVectorFileDict[tMiddle],currentVectorFileDict[tempEnd])
                                            assembledWord = tempStart+tMiddle+tempEnd
                                            desFile.write(assembledWord+" "+str(assembledVector)+"\n")
                                            start=""
                                            middle = ""
                                            end =""
                                        else:
                                            desFile.write(word+" "+ str(currentVectorFileDict[word])+"\n")
                                    except Exception as e:
                                        print("error in assemble word " + word)
                                        print(e)

    def processFileAssembleSum(self,sourceDirectory, destinationDirectory,vectorSourceDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            for folder in subFolders:
                # 26/11/17 Or: its the long path to the files
                newSourceDirectory = os.path.join(sourceDirectory, folder)
                newDestinationDirectory = os.path.join(destinationDirectory, folder)
                newVectorSourceDir =  os.path.join(vectorSourceDirectory, folder)
                Utils().ensure_dir(newDestinationDirectory)
                self.processFileAssembleSum(newSourceDirectory, newDestinationDirectory,newVectorSourceDir)

            # 26/11/17 Or: files are file in root directory
            for currentFile in files:
                if currentFile.endswith(".txt"):
                    start=""
                    middle =""
                    end =""
                    numberOfParts=0
                    inMiddle = False
                    fileName = currentFile.split(".")[0]
                    filePath = os.path.join(sourceDirectory, currentFile)
                    vectorFilePath = os.path.join(vectorSourceDirectory,fileName+"_"+Scripts().SAVE_FILE+".txt")
                    destFilePath = os.path.join(destinationDirectory,fileName+".txt")
                    try:
                        currentVectorFileDict = Utils().readVectorToDictionary(vectorFilePath)
                    except:
                        continue
                    with io.open(filePath, 'r',encoding="utf-8") as sourceFile:
                        with io.open(destFilePath,'w',encoding="utf-8") as desFile:
                            for line in sourceFile:
                                for word in line.split():
                                    try:
                                        if "^$" in word:
                                            if numberOfParts==0:
                                                start = word
                                            if numberOfParts == 1:
                                                middle = word
                                            numberOfParts=numberOfParts+1
                                            inMiddle = True
                                        elif "^&" in word:
                                            if numberOfParts==1:
                                                middle = word
                                            if numberOfParts==2:
                                                end = word
                                            numberOfParts=0
                                            tempStart = start.replace("^$","")
                                            tempMiddle = middle.replace("^$","")
                                            tMiddle = tempMiddle.replace("^&","")
                                            tempEnd = end.replace("^&","")
                                            if tempStart=="" or tempStart is None or tempStart=='':
                                                if tempEnd =="" or tempEnd=='':
                                                    assembledVector = currentVectorFileDict[tMiddle]
                                                else:
                                                    assembledVector =self.sum2(currentVectorFileDict[tempEnd],currentVectorFileDict[tMiddle])
                                            elif tempEnd =="" or tempEnd=='':
                                                if tMiddle =="" or tMiddle=='':
                                                    assembledVector = currentVectorFileDict[tempStart]
                                                else:
                                                    assembledVector = self.sum2(currentVectorFileDict[tempStart],
                                                                                        currentVectorFileDict[tMiddle])
                                            elif tMiddle=="" or tMiddle=='':
                                                if tempEnd =="" or tempEnd=='':
                                                    assembledVector = currentVectorFileDict[tempStart]
                                                else:
                                                    assembledVector = self.sum2(currentVectorFileDict[tempStart],
                                                                                        currentVectorFileDict[tempEnd])
                                            else:
                                                assembledVector = self.sum(currentVectorFileDict[tempStart],currentVectorFileDict[tMiddle],currentVectorFileDict[tempEnd])
                                            assembledWord = tempStart+tMiddle+tempEnd
                                            desFile.write(assembledWord+" "+str(assembledVector)+"\n")
                                            start=""
                                            middle = ""
                                            end =""
                                        else:
                                            desFile.write(word+" "+ str(currentVectorFileDict[word])+"\n")
                                    except Exception as e:
                                        print("error in assemble word " + word)
                                        print(e)

    def mergeDataSet(self, sourceDirectory, destinationDirectory):
        for root, subFolders, files in os.walk(sourceDirectory):
            for folder in subFolders:
                # 26/11/17 Or: its the long path to the files
                newSourceDirectory = os.path.join(sourceDirectory, folder)
                newDestinationDirectory = os.path.join(destinationDirectory, folder)
                print(newDestinationDirectory)
                Utils().ensure_dir(newDestinationDirectory)
                self.mergeDataSet(newSourceDirectory, newDestinationDirectory)

            # 26/11/17 Or: files are file in root directory
            numberOfFiles = len(files)
            currentFileNumber = 0
            firstFileContent=""
            secondFileContent=""
            for currentFile in files:
                if currentFile.endswith(".txt"):
                    fileName = currentFile.split(".")[0]
                    filePath = os.path.join(sourceDirectory, currentFile)
                    destinationFilePath = os.path.join(destinationDirectory,currentFile)
                    #when number of file are pair this condination are never hit
                    if os.path.exists(filePath):
                        if currentFileNumber % 2 == 1 and numberOfFiles == currentFileNumber:
                            with io.open(filePath, 'r',encoding="utf-8") as content_file:
                                firstFileContent = content_file.read()
                            with io.open(destinationFilePath, 'w', encoding="utf-8") as detFile:
                                detFile.write(firstFileContent+" "+ firstFileContent)
                            firstFileContent=""
                            continue
                        if currentFileNumber % 2 == 0:
                            with io.open(filePath, 'r',encoding="utf-8") as content_file:
                                firstFileContent = content_file.read()
                        else:
                            with io.open(filePath, 'r',encoding="utf-8") as content_file:
                                secondFileContent = content_file.read()
                            with io.open(destinationFilePath, 'w', encoding="utf-8") as detFile:
                                detFile.write(firstFileContent+ firstFileContent+secondFileContent+ secondFileContent)
                            firstFileContent=""
                            secondFileContenift=""
                        currentFileNumber =currentFileNumber+1
                    else:
                        print("file not exsist (could be nothing) "+filePath)

class calcResult:
    def findSimilarity(self,sourceAssembledVectorDirectory,sourceVectorDirectory,destiontionDirectory):
        for root, subFolders, files in os.walk(sourceAssembledVectorDirectory):
            for folder in subFolders:
                # 26/11/17 Or: its the long path to the files
                newSourceDirectory = os.path.join(sourceAssembledVectorDirectory, folder)
                newDestinationDirectory = os.path.join(destiontionDirectory, folder)
                newVectorSourceDir =  os.path.join(sourceVectorDirectory, folder)
                #print(newDestinationDirectory)
                Utils().ensure_dir(newDestinationDirectory)
                #print("newVectorSourceDir "+newVectorSourceDir)
                self.findSimilarity(newSourceDirectory,newVectorSourceDir,newDestinationDirectory)
            biggest = -1
            # 26/11/17 Or: files are file in root directory
            for currentFile in files:
                if currentFile.endswith(".txt"):
                    maxPerFile=-1
                    inMiddle = False
                    fileName = currentFile.split(".")[0]
                    filePath = os.path.join(sourceAssembledVectorDirectory, currentFile)
                    vectorFilePath = os.path.join(sourceVectorDirectory,fileName+"_"+Scripts().SAVE_FILE+".txt")
                    destFilePath = os.path.join(destiontionDirectory,fileName+".txt")
                    try:
                        currentVectorFileDict = Utils().readVectorToDictionary(vectorFilePath)
                    except:
                        continue
                    with io.open(filePath, 'r',encoding="utf-8") as sourceFile:
                        with io.open(destFilePath,'w',encoding="utf-8") as desFile:
                            for line in sourceFile:
                                currentWord = line.split()[0]
                                currentVector = Utils().buildVector(line)
                                try:
                                    currentCosineSimilarity = self.cosine_similarity(currentVector,currentVectorFileDict[currentWord])
                                    if currentCosineSimilarity < 0.85:
                                        if currentCosineSimilarity > maxPerFile:
                                            maxPerFile = currentCosineSimilarity
                                        if currentCosineSimilarity> biggest:
                                            biggest = currentCosineSimilarity
                                        if currentCosineSimilarity>0.4:
                                            print("hit: "+ currentWord+" file is: " + filePath)
                                    desFile.write(currentWord+" "+ str(currentCosineSimilarity)+"\n")
                                except:
                                    print("error in get word: "+ line.split()[0])
                    print("max of this file is: "+ str(maxPerFile))
                    maxPerFile =-1
            print("biggest of all file is: "+str(biggest))
    def cosine_similarity(self,v1, v2):
        "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(v1)):
            x = v1[i];
            y = v2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        return sumxy / math.sqrt(sumxx * sumyy)

    def TTest(self, firstVector, secondVector):
        return stats.ttest_ind(firstVector,secondVector)



#PreProcces().reqConvertFile2UTF8("C:\FinalProject\clean_shut_B4_replace","C:\FinalProject\clean_shut_B4_replace_UTF8")
#PreProcces().genrateTaggerFile("C:\\FinalProject\\wiki","C:\\FinalProject\\wiki_tagger_output")
#BuildDataSet().generateSplittedWord("שמירת","שמירה")
#PreProcces().reqConvertFile2UTF8("C:\\FinalProject\\tests","C:\\FinalProject\\tests_output")
#BuildDataSet().genWitoutHeaderAndTailFile("C:\\FinalProject\\tests","C:\\FinalProject\\tests_output")


#Scripts().porccesFile( "C:\\FinalProject\\wiki_stiming_output", "C:\\FinalProject\\wiki_stiming_glove_200_output")
#print "finish procces stiming file"
#Scripts().porccesFile( "C:\\FinalProject\\wiki_headtail_output", "C:\\FinalProject\\wiki_headtail_glove_200_output")
#print "finish procces headtail file"
#Scripts().porccesFile( "C:\\FinalProject\\wiki_data_set", "C:\\FinalProject\\wiki_glove_200_data_set")
#print "finish procces original file"

#res = calcResult().cosine_similarity( [-0.011307, -0.007101, 0.004882, -0.004832, -0.001817, 0.014935, -0.000892, 0.016511, 0.003416, -0.000687, -5.2e-05, 0.010024, 0.00603, -0.003575, 0.004226, -0.00404, -0.003163, 0.002315, 0.002084, -0.012558, -0.000965, 0.011412, 0.000411, 1.5e-05, -0.00305, -0.001579, -0.002611, 0.011941, 0.007555, -0.003527, -0.000908, 0.014877, 0.003004, 0.004749, 0.00238, -0.005559, 0.000593, -0.006828, 0.001846, -0.00609, -0.01193, -0.004459, -0.00611, 0.0081, 0.005631, -0.011071, 0.003668, -0.0007, -0.002397, 0.004668, -0.002304, 0.010701, -0.005903, 0.01666, 0.011816, -0.001646, -0.006066, -0.020867, 0.012911, 0.003613, 0.005031, -0.011161, 0.008481, -0.001971, 0.006547, -0.000275, 0.002051, 0.004871, 0.00757, 0.006632, -0.005345, -0.016705, 0.003245, -0.007044, 0.00914, 0.009248, -0.003064, -0.003895, -0.00627, 0.001584, 0.00468, 0.006196, 0.001826, 0.015636, 0.012704, 0.014762, 0.007301, -0.008702, -0.008031, 0.005352, -6.9e-05, 0.004202, 0.009804, 0.002139, 0.005313, 0.015562, -0.006604, -0.00992, 0.002773, -0.002743, -0.012329, -0.002989, 0.007833, -0.015609, -0.0076, 0.005131, 0.002003, 0.00405, -0.017919, 0.008013, -0.002604, 0.001783, 0.010333, -0.009545, -0.010931, -0.007183, 0.007523, -0.00327, -0.001665, 0.005502, -0.004715, 0.003123, 0.002899, 0.016369, -0.005659, 0.007467, -0.005964, -0.010206, -0.001801, 0.007069, 0.002063, -0.003646, 0.008054, -0.002761, 0.003458, -0.010809, 0.007291, -0.009683, 0.01157, 0.016225, 0.009057, 0.002605, 0.002291, -0.006414, -0.003228, -0.006989, 0.013714, -0.008133, -0.011512, -0.0037, -0.016915, 0.012893, 0.008101, 0.010489, -0.017332, -0.003613, 0.000783, 0.013705, 2.1e-05, 0.001074, -0.000737, 0.002407, 0.008517, -0.00465, 0.004266, -0.000641, 0.012936, 0.009771, 0.010003, -0.004507, -0.005704, 0.00095, 0.004335, -0.01382, -0.004304, 0.002913, 0.002012, 0.005648, -0.000304, -0.002946, -0.007291, 0.008518, 0.009775, -0.002629, 0.005221, 0.01017, 0.007117, -0.008459, 0.006989, -0.016208, -0.002015, 0.005055, -0.004631, -0.005479, -0.002195, 0.002646, -0.015307, 0.001823, 0.001452, -0.003898]
#,[-0.053541, 0.033162, -0.0037565000000000003, 0.1341485, -0.177876, 0.07353849999999999, 0.2501135, -0.0173575, -0.020377, 0.058961, 0.083596, 0.0229075, -0.0511335, 0.08990200000000001, -0.0062039999999999994, 0.056564, 0.008747999999999999, -0.05978649999999999, 0.128906, -0.0736355, -0.1706405, 0.037310499999999996, 0.002943, -0.0337365, -0.0138375, -0.146568, 0.152339, -0.0965125, 0.074217, -0.160994, 0.164234, -0.1520835, 0.0526495, -0.1441655, 0.0512275, 0.035680500000000004, -0.0060585, 0.0359635, 0.0051635000000000006, 0.10931750000000001, -0.0100805, -0.024727, -0.0497545, 0.017930500000000002, 0.079694, -0.0372495, -0.115911, -0.2702005, -0.099687, 0.048237, 0.0477915, 0.025745, 0.0182125, 0.19573000000000002, -0.071902, 0.0967935, -0.291431, 0.1589915, 0.019546, 0.18990250000000003, 0.175301, -0.22326649999999998, 0.1465395, 0.09011949999999999, 0.012006500000000002, -0.121577, 0.016265, -0.15049099999999999, -0.0010425000000000002, 0.06922800000000001, 0.1032, 0.1311705, -0.1322755, -0.0036155, 0.052506, 0.0111665, -0.033710000000000004, 0.0428855, -0.12206049999999999, 0.2496665, 0.072037, -0.175415, 0.0343315, 0.19584000000000001, -0.0328265, 0.06926550000000001, 0.068297, 0.0251125, -0.061426499999999995, 0.12254999999999999, -0.08437700000000001, 0.0068455, -0.0472325, -0.023127, -0.0333115, -0.101913, -0.1948095, -0.1859265, 0.160012, 0.005469, 0.0186975, 0.1309795, 0.2612745, 0.1573305, 0.12524849999999998, -0.0049365, 0.074153, 0.010576499999999999, 0.1404275, 0.074199, 0.013275, -0.141327, -0.059534, -0.1853565, 0.111527, 0.022434500000000003, -0.1336155, -0.0866865, 0.108899, 0.12055099999999999, 0.1188715, -0.060753, -0.087434, 0.047070499999999994, 0.1200615, 0.0640285, -0.049419500000000005, -0.048163, 0.12658049999999998, -0.0883015, -0.0577595, -0.28126450000000003, -0.236885, 0.2391025, 0.11853649999999999, 0.063076, -0.08322099999999999, -0.102175, -0.0892525, -0.0013629999999999996, 0.11478949999999999, 0.0229135, 0.0940325, 0.182944, 0.24039549999999998, 0.0507375, 0.1360645, -0.1288885, -0.041306999999999996, 0.043437500000000004, 0.0189545, 0.0026984999999999995, 0.058711, -0.0492645, -0.056628, -0.02673, -0.1186125, 0.1940905, -0.0720905, 0.2334955, 0.0732365, -0.068566, -0.036646, 0.2250615, 0.1397155, 0.0830825, 0.0028335, 0.043015, -0.24324049999999997, -0.19159400000000001, 0.1840725, -0.053818, 0.003402, 0.129454, -0.026467, -0.09188349999999999, -0.1870215, -0.012074000000000001, -0.08226149999999999, 0.14015899999999998, -0.040153999999999995, 0.1076425, -0.10543899999999999, -0.04983, 0.09613949999999999, 0.10327549999999999, 0.0140535, 0.020227000000000002, 0.032386, 0.011982, -0.1446535, -0.0038664999999999997, 0.1786705, -0.0258725, -0.11751349999999999, 0.03561, 0.019488500000000002, -0.054540500000000006, -0.093282, 0.1752955]
#)
#print res
#res = calcResult().cosine_similarity([-0.004275 ,-0.000330 ,-0.004851 ,0.000012 ,0.002374 ,-0.002070 ,-0.006415 ,0.001233 ,0.002951 ,-0.000569 ,-0.007449 ,0.006038 ,-0.000942 ,0.006664 ,0.003879 ,-0.000434 ,0.003973 ,0.000725 ,0.003657 ,0.008356 ,0.000395 ,-0.002011 ,0.001202 ,-0.000560 ,-0.010583 ,-0.007859 ,0.001885 ,-0.000894 ,0.000575 ,-0.002046 ,-0.002248 ,-0.003185 ,0.001176 ,0.008922 ,-0.006035 ,0.002838 ,-0.004678 ,-0.006482 ,-0.000523 ,0.004803 ,-0.002844 ,0.003024 ,0.000393 ,-0.002336 ,-0.005891 ,0.000209 ,-0.001268 ,-0.002987 ,0.000239 ,0.001712 ,-0.002347 ,0.007583 ,0.003931 ,-0.003069 ,0.002018 ,0.007838 ,-0.003199 ,0.002614 ,0.000149 ,-0.001477 ,0.000965 ,0.001872 ,-0.001060 ,-0.002229 ,0.000075 ,0.002461 ,0.003153 ,0.004505 ,0.001125 ,0.007413 ,-0.002031 ,-0.002881 ,-0.000434 ,-0.000870 ,-0.001411 ,0.004258 ,-0.000802 ,-0.002412 ,0.002348 ,0.001312 ,-0.005344 ,-0.001871 ,0.003704 ,0.005250 ,0.000657 ,-0.000898 ,0.000409 ,-0.002710 ,0.001834 ,-0.002430 ,-0.003241 ,-0.000398 ,0.000354 ,0.002044 ,0.000827 ,0.005280 ,-0.001836 ,0.006313 ,-0.000140 ,-0.005226 ,0.001595 ,-0.002402 ,0.001116 ,0.002991 ,-0.001279 ,0.001914 ,-0.008464 ,0.003154 ,0.002504 ,0.001362 ,-0.004656 ,0.001486 ,-0.005177 ,-0.007282 ,0.003047 ,-0.000455 ,0.005655 ,-0.000520 ,0.000855 ,0.006658 ,-0.002978 ,0.005833 ,-0.000909 ,-0.000158 ,0.001452 ,-0.000093 ,0.006903 ,-0.000450 ,-0.001939 ,-0.004808 ,0.001874 ,-0.001543 ,0.000650 ,0.000496 ,0.000521 ,-0.004025 ,0.006175 ,-0.001259 ,-0.001023 ,-0.006918 ,-0.003549 ,0.000299 ,0.002038 ,-0.000084 ,0.004166 ,0.002359 ,-0.000477 ,-0.000658 ,0.003513 ,-0.001018 ,-0.003399 ,0.000381 ,-0.000078 ,-0.002127 ,-0.004356 ,-0.006763 ,0.002208 ,0.002473 ,0.000813 ,-0.001874 ,0.002578 ,-0.006914 ,0.001886 ,-0.003876 ,0.006886 ,0.002911 ,-0.000128 ,0.000172 ,-0.001931 ,0.003948 ,0.002785 ,-0.002438 ,0.008797 ,0.001376 ,-0.000193 ,-0.003086 ,0.000833 ,-0.006866 ,0.002395 ,0.002197 ,0.001027 ,0.002469 ,0.002511 ,0.005720 ,-0.000266 ,-0.004523 ,-0.002764 ,-0.004998 ,0.000035 ,-0.003183 ,0.000601 ,0.001409 ,0.000351 ,-0.002082 ,-0.002681 ,0.010721 ,-0.006857 ,0.000717 ,-0.002894 ,0.004787]
#,[0.001777 ,-0.003679 ,-0.003250 ,0.003142 ,0.002379 ,0.000102 ,-0.004402 ,-0.002183 ,0.001269 ,0.000268 ,-0.002353 ,0.007079 ,0.001880 ,0.005309 ,0.000346 ,-0.001862 ,0.003169 ,-0.002382 ,-0.002156 ,0.001996 ,0.000375 ,0.000723 ,0.001498 ,-0.002367 ,-0.000460 ,-0.001128 ,0.003202 ,0.001425 ,0.000730 ,0.001296 ,0.000941 ,0.000596 ,-0.000977 ,-0.002813 ,-0.001622 ,0.001334 ,-0.002006 ,0.001626 ,-0.000058 ,0.000938 ,0.004386 ,-0.002449 ,-0.000977 ,0.002456 ,0.001300 ,-0.002081 ,-0.002757 ,-0.001601 ,0.004301 ,0.001904 ,-0.001556 ,0.000262 ,0.001894 ,-0.001796 ,0.000634 ,-0.001927 ,-0.004027 ,0.002534 ,-0.000479 ,-0.005031 ,0.003257 ,-0.001685 ,0.002979 ,0.000259 ,-0.002212 ,0.003709 ,-0.001138 ,0.002397 ,0.002557 ,-0.000567 ,-0.005033 ,-0.002506 ,0.001789 ,-0.004247 ,-0.000940 ,0.000969 ,-0.002468 ,0.000020 ,0.004036 ,0.003589 ,0.000390 ,-0.002666 ,-0.004130 ,0.001333 ,-0.002456 ,-0.001345 ,-0.002611 ,0.004581 ,-0.000635 ,0.002423 ,-0.001630 ,-0.001744 ,0.005589 ,0.004230 ,-0.000774 ,-0.001004 ,0.003847 ,0.000214 ,0.000283 ,0.002056 ,-0.000979 ,0.000053 ,0.000609 ,0.002278 ,0.000072 ,0.004479 ,-0.001147 ,-0.001873 ,0.003753 ,0.001756 ,-0.006700 ,-0.001318 ,-0.000645 ,-0.002615 ,0.002277 ,0.001963 ,0.005710 ,0.000120 ,0.002676 ,-0.003514 ,0.000818 ,0.001477 ,0.003419 ,-0.001352 ,-0.004393 ,0.003389 ,0.001181 ,0.000729 ,0.001488 ,0.001907 ,0.000887 ,-0.004937 ,0.004294 ,-0.004002 ,-0.004974 ,-0.003780 ,-0.000007 ,-0.000245 ,-0.003133 ,-0.003010 ,0.000744 ,0.002948 ,0.000427 ,0.001884 ,0.000582 ,0.000162 ,-0.001493 ,0.001002 ,0.003437 ,0.001166 ,0.000078 ,-0.000947 ,0.002792 ,0.001499 ,-0.004282 ,0.001483 ,0.000894 ,0.002091 ,0.006956 ,0.001889 ,0.002569 ,-0.002047 ,0.003545 ,-0.005712 ,0.002222 ,-0.003372 ,-0.001806 ,0.001068 ,-0.002542 ,-0.001152 ,0.001629 ,0.002196 ,-0.002335 ,-0.002857 ,-0.000308 ,0.000468 ,0.002884 ,-0.001797 ,0.003949 ,-0.001974 ,0.001409 ,-0.000003 ,-0.000144 ,0.000039 ,-0.004341 ,0.002441 ,-0.002696 ,-0.003678 ,0.002140 ,-0.001179 ,0.001822 ,0.001015 ,0.002410 ,0.003029 ,-0.001419 ,0.004006 ,0.002861 ,-0.000823 ,-0.000637 ,0.002892]
#)
#print res
#res = calcResult().TTest([-0.011307, -0.007101, 0.004882, -0.004832, -0.001817, 0.014935, -0.000892, 0.016511, 0.003416, -0.000687, -5.2e-05, 0.010024, 0.00603, -0.003575, 0.004226, -0.00404, -0.003163, 0.002315, 0.002084, -0.012558, -0.000965, 0.011412, 0.000411, 1.5e-05, -0.00305, -0.001579, -0.002611, 0.011941, 0.007555, -0.003527, -0.000908, 0.014877, 0.003004, 0.004749, 0.00238, -0.005559, 0.000593, -0.006828, 0.001846, -0.00609, -0.01193, -0.004459, -0.00611, 0.0081, 0.005631, -0.011071, 0.003668, -0.0007, -0.002397, 0.004668, -0.002304, 0.010701, -0.005903, 0.01666, 0.011816, -0.001646, -0.006066, -0.020867, 0.012911, 0.003613, 0.005031, -0.011161, 0.008481, -0.001971, 0.006547, -0.000275, 0.002051, 0.004871, 0.00757, 0.006632, -0.005345, -0.016705, 0.003245, -0.007044, 0.00914, 0.009248, -0.003064, -0.003895, -0.00627, 0.001584, 0.00468, 0.006196, 0.001826, 0.015636, 0.012704, 0.014762, 0.007301, -0.008702, -0.008031, 0.005352, -6.9e-05, 0.004202, 0.009804, 0.002139, 0.005313, 0.015562, -0.006604, -0.00992, 0.002773, -0.002743, -0.012329, -0.002989, 0.007833, -0.015609, -0.0076, 0.005131, 0.002003, 0.00405, -0.017919, 0.008013, -0.002604, 0.001783, 0.010333, -0.009545, -0.010931, -0.007183, 0.007523, -0.00327, -0.001665, 0.005502, -0.004715, 0.003123, 0.002899, 0.016369, -0.005659, 0.007467, -0.005964, -0.010206, -0.001801, 0.007069, 0.002063, -0.003646, 0.008054, -0.002761, 0.003458, -0.010809, 0.007291, -0.009683, 0.01157, 0.016225, 0.009057, 0.002605, 0.002291, -0.006414, -0.003228, -0.006989, 0.013714, -0.008133, -0.011512, -0.0037, -0.016915, 0.012893, 0.008101, 0.010489, -0.017332, -0.003613, 0.000783, 0.013705, 2.1e-05, 0.001074, -0.000737, 0.002407, 0.008517, -0.00465, 0.004266, -0.000641, 0.012936, 0.009771, 0.010003, -0.004507, -0.005704, 0.00095, 0.004335, -0.01382, -0.004304, 0.002913, 0.002012, 0.005648, -0.000304, -0.002946, -0.007291, 0.008518, 0.009775, -0.002629, 0.005221, 0.01017, 0.007117, -0.008459, 0.006989, -0.016208, -0.002015, 0.005055, -0.004631, -0.005479, -0.002195, 0.002646, -0.015307, 0.001823, 0.001452, -0.003898]
#,[-0.004275 ,-0.000330 ,-0.004851 ,0.000012 ,0.002374 ,-0.002070 ,-0.006415 ,0.001233 ,0.002951 ,-0.000569 ,-0.007449 ,0.006038 ,-0.000942 ,0.006664 ,0.003879 ,-0.000434 ,0.003973 ,0.000725 ,0.003657 ,0.008356 ,0.000395 ,-0.002011 ,0.001202 ,-0.000560 ,-0.010583 ,-0.007859 ,0.001885 ,-0.000894 ,0.000575 ,-0.002046 ,-0.002248 ,-0.003185 ,0.001176 ,0.008922 ,-0.006035 ,0.002838 ,-0.004678 ,-0.006482 ,-0.000523 ,0.004803 ,-0.002844 ,0.003024 ,0.000393 ,-0.002336 ,-0.005891 ,0.000209 ,-0.001268 ,-0.002987 ,0.000239 ,0.001712 ,-0.002347 ,0.007583 ,0.003931 ,-0.003069 ,0.002018 ,0.007838 ,-0.003199 ,0.002614 ,0.000149 ,-0.001477 ,0.000965 ,0.001872 ,-0.001060 ,-0.002229 ,0.000075 ,0.002461 ,0.003153 ,0.004505 ,0.001125 ,0.007413 ,-0.002031 ,-0.002881 ,-0.000434 ,-0.000870 ,-0.001411 ,0.004258 ,-0.000802 ,-0.002412 ,0.002348 ,0.001312 ,-0.005344 ,-0.001871 ,0.003704 ,0.005250 ,0.000657 ,-0.000898 ,0.000409 ,-0.002710 ,0.001834 ,-0.002430 ,-0.003241 ,-0.000398 ,0.000354 ,0.002044 ,0.000827 ,0.005280 ,-0.001836 ,0.006313 ,-0.000140 ,-0.005226 ,0.001595 ,-0.002402 ,0.001116 ,0.002991 ,-0.001279 ,0.001914 ,-0.008464 ,0.003154 ,0.002504 ,0.001362 ,-0.004656 ,0.001486 ,-0.005177 ,-0.007282 ,0.003047 ,-0.000455 ,0.005655 ,-0.000520 ,0.000855 ,0.006658 ,-0.002978 ,0.005833 ,-0.000909 ,-0.000158 ,0.001452 ,-0.000093 ,0.006903 ,-0.000450 ,-0.001939 ,-0.004808 ,0.001874 ,-0.001543 ,0.000650 ,0.000496 ,0.000521 ,-0.004025 ,0.006175 ,-0.001259 ,-0.001023 ,-0.006918 ,-0.003549 ,0.000299 ,0.002038 ,-0.000084 ,0.004166 ,0.002359 ,-0.000477 ,-0.000658 ,0.003513 ,-0.001018 ,-0.003399 ,0.000381 ,-0.000078 ,-0.002127 ,-0.004356 ,-0.006763 ,0.002208 ,0.002473 ,0.000813 ,-0.001874 ,0.002578 ,-0.006914 ,0.001886 ,-0.003876 ,0.006886 ,0.002911 ,-0.000128 ,0.000172 ,-0.001931 ,0.003948 ,0.002785 ,-0.002438 ,0.008797 ,0.001376 ,-0.000193 ,-0.003086 ,0.000833 ,-0.006866 ,0.002395 ,0.002197 ,0.001027 ,0.002469 ,0.002511 ,0.005720 ,-0.000266 ,-0.004523 ,-0.002764 ,-0.004998 ,0.000035 ,-0.003183 ,0.000601 ,0.001409 ,0.000351 ,-0.002082 ,-0.002681 ,0.010721 ,-0.006857 ,0.000717 ,-0.002894 ,0.004787]
#)
#print res
#assemble().readVectorToDictionary("C:\FinalProject\\tests_output\\Emails_vectors.txt")
#assemble().processFileAssembleBasicAvarge("C:\FinalProject\\wiki_tagger_taaged_output","C:\FinalProject\\wiki_headtail_glove_200_basicAVG_output","C:\FinalProject\\wiki_headtail_glove_200_output")
#assemble().processFileAssembleWeightedAverage("C:\FinalProject\\wiki_tagger_taaged_output","C:\FinalProject\\wiki_headtail_glove_200_weightedAVG_output","C:\FinalProject\\wiki_headtail_glove_200_output")
#assemble().processFileAssembleSum("C:\FinalProject\\wiki_tagger_taaged_output","C:\FinalProject\\wiki_headtail_glove_200_sum_output","C:\FinalProject\\wiki_headtail_glove_200_output")
#calcResult().findSimilarity("C:\FinalProject\\wiki_headtail_glove_200_basicAVG_output","C:\FinalProject\\wiki_glove_200_data_set","C:\FinalProject\\wiki_headtail_glove_200_basicAVG_result_output")
#calcResult().findSimilarity("C:\FinalProject\\wiki_headtail_glove_200_sum_output","C:\FinalProject\\wiki_glove_200_data_set","C:\FinalProject\\wiki_headtail_glove_200_sum_result_output")
#assemble().mergeDataSet("C:\FinalProject\\tests","C:\FinalProject\\tests_output")
#Scripts().porccesFile( "C:\\FinalProject\\tests", "C:\\FinalProject\\tests_output")