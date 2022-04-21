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
        try:
            with open(filePath, 'r') as readFile:
                fileRead = readFile.readlines()
                fileLines.update({filePath:fileRead})
        except:
            fileLines.update({filePath:'Error'})
    elif filePath.endswith('.csv'):
        try:
            fileRead = []
            with open(filePath, newline='') as csvFile:
                spamreader = csv.reader(csvFile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    fileRead.append(', '.join(row))
            fileLines.update({filePath:fileRead})
        except:
            fileLines.update({filePath:'Error'})
    elif filePath.endswith('.docx'):
        try:
            openDocx = docx2txt.process(filePath)
            fileRead = openDocx.split('.')
            for row in fileRead:
                fileLines.update({filePath:fileRead})
        except:
            fileLines.update({filePath:'Error'})
    elif filePath.endswith('.xlsx') or filePath.endswith('.xls'):
        try:
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
        except:
            fileLines.update({filePath:'Error'})
    elif filePath.endswith('.pdf'):
        try:
            with pdfplumber.open(filePath) as pdf:
                fileRead = []
                pdfPages = pdf.pages
                for page in range(len(pdfPages)):
                    pageText = pdf.pages[page].extract_text()
                    textLines = pageText.split('.')
                    for l in textLines:
                        if l != ' ':
                            fileRead.append(l)
                fileLines.update({filePath:fileRead})
        except:
            fileLines.update({filePath:'Error'})
    else:
        pass
    
    return fileLines

def processText(preppedFiles):
    searchCriteria = {'Category 4':{'[0-9]{3}-[0-9]{2}-[0-9]{4}':'SSN','[0-9]{12}':'Bank','[0-9]{17}':'Bank or Credit','[0-9][0-9]{16}':'Credit',
    '^((?!11-1111111)(?!22-2222222)(?!33-3333333)(?!44-4444444)(?!55-5555555)(?!66-6666666)(?!77-7777777)(?!88-8888888)(?!99-9999999)(?!12-3456789)(?!00-[0-9]{7})([0-9]{2}-[0-9]{7}))*$':'Tax ID',
    '^(\d)\1-\1{7}$':'Tax ID','^(?=.{12}$)[A-Z]{1,7}[A-Z0-9\\*]{4,11}$':'WADL'},'Category 3':{'[0-9]{9,11}':'EMPLID','[mM]ale|[fF]emale':'Gender',
    '[wW]hite|[pP]acific [iI]slander|[bB]lack/[aA]frican [aA]merican|[aA]merican [iI]ndian|[hH]ispanic|[nN]ative [hH]awaiian or [oO]ther [pP]acific [iI]slander|'\
    '[aA]laska [nN]ative|[mM]ulti-[rR]acial|[oO]ther [rR]ace ':'Race','[sS]ingle parent with children or other dependents|[cC]ouple with children or other dependents'\
    '[wW]ithout children or other dependents':'Family Status','[fF]ull [tT]ime|[pP]art [tT]ime':'Employment Status'}}
    # processedFiles = {}
    processedFilesList = []   
    for c,i in searchCriteria.items():
        for r,d in i.items():
            for p,t in preppedFiles.items():
                for li in t:
                    regex = re.search(r,li)
                    if regex:
                        piiList = [p,d,c]
                        processedFilesList.append(piiList)
    reportDataFrame = pd.DataFrame(processedFilesList,columns=['Filepath','PII Type','PII Category'])                    

    reportDataFrame.to_csv('ReportFile.csv',index=False)
    

if __name__ == "__main__":
    main()