import pandas as pd
import os
import re
import csv
import docx2txt
import pdfplumber

def main():
    preppedFiles = walkFiles()
    # readText = fileType(filePaths)
    textProcessed = processText(preppedFiles)
    processedFiles = {}
    # processedFiles.update(textProcessed)

def walkFiles():
    currentDir = os.getcwd()
    preppedFiles = {}
    # dirList = []
    for root, dirs, files in os.walk(currentDir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            filePath = os.path.join(root, file)
            fileLines = fileType(filePath)
            preppedFiles.update(fileLines)
    
    return preppedFiles

def fileType(filePath):
    fileLines = {}
    if filePath.endswith('.txt'):
        with open(filePath, 'r') as readFile:
            fileRead = readFile.readlines()
            fileLines.update({filePath:fileRead})
    elif filePath.endswith('.csv'):
        fileRead = []
        with open(filePath, newline='') as csvFile:
            spamreader = csv.reader(csvFile, delimiter=' ', quotechar='|')
            for row in spamreader:
                fileRead.append(', '.join(row))
        fileLines.update({filePath:fileRead})
    elif filePath.endswith('.docx'):
        # print(filePath)
        openDocx = docx2txt.process(filePath)
        fileRead = openDocx.split('.')
        for row in fileRead:
            fileLines.update({filePath:fileRead})
    elif filePath.endswith('.xlsx') or filePath.endswith('.xls'):
        fileRead = []
        excelFile = pd.read_excel(filePath,sheet_name=None)
        sheetNames = excelFile.keys()
        for s in sheetNames:
            excelSheet = excelFile[s]
            columnList = excelSheet.columns.values.tolist()
            if len(columnList) == 1:
                columnItems = excelSheet[columnList[0]].values.tolist()
                for i in columnItems:
                    fileRead.append(str(i))
            else:
                for c in columnList:
                    columnItems = excelSheet[c].values.tolist()
                    for i in columnItems:
                        if str(i) != 'nan':
                            fileRead.append(str(i))
        fileLines.update({filePath:fileRead})
    elif filePath.endswith('.pdf'):
        with pdfplumber.open("test.pdf") as pdf:
            fileRead = []
            pdfPages = pdf.pages
            for page in range(len(pdfPages)):
                pageText = pdf.pages[page].extract_text()
                textLines = pageText.split('.')
                for l in textLines:
                    if l != ' ':
                        fileRead.append(l)
            fileLines.update({filePath:fileRead})
    else:
        pass
    
    return fileLines

def processText(preppedFiles):
    searchCriteria = {'[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]':'SSN','[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]':'EMPLID','[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]':'Bank',
    '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]':'Bank or Credit','[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]':'Credit'}
    processedFiles = {}
    for r,d in searchCriteria.items():
        for p,t in preppedFiles.items():
            for li in t:
                regex = re.search(r,li)
                if regex:
                    processedFiles.update({p:d})

    print(processedFiles)

if __name__ == "__main__":
    main()