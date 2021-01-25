import os
try:
    import pandas as pd
    import openpyxl
    importBool = True
    
except ImportError:
    print("Could not find pandas or openpyxl, please download them using pip if you want to export to excel using.")
    importBool = False


#Creation of lists to store position______________________________________
def offsetin(input_dic):
    position = 40*(2**(len(input_dic.keys())))
    global endpoint; endpoint = position
    for i in input_dic.keys():
        position //= 2
        input_dic[i] = [position,0]


#findingAmountOfOperations________________________________________________
def paranumfunc(str):
    counter = 0
    for i in str:
        if i == '(':
            counter += 1
    return counter

#listOfOperators__________________________________________________________
def xorfunc(a,b):
    if (a == 1 and b ==0) or (a == 0 and b ==1):
        return 1
    else:
        return 0

def andfunc(a,b):
    if (a == 1 and b == 1):
        return 1
    else:
        return 0

def orfunc(a,b):
    if (a == 0 and b == 0):
        return 0
    else:
        return 1
def imfunc(a,b):
    if (a == 1 and b == 0):
        return 0
    else:
        return 1

def nefunc(a):
    if a ==1:
        return 0
    else:
        return 1

def ouexfunc(a,b):
    if (a == 1 and b ==0) or (a == 0 and b ==1):
        return 1
    else:
        return 0

def bifunc(a,b):
    if (a==1 and b==1) or (a==0 and b==0):
        return 1
    else:
        return 0

def nandfunc(a,b):
    if (a == 1 and b==1):
        return 0
    else:
        return 1

#findingExcutions__________________________________________________________
def findParentheses(string,paraNum,input_dic):
    for j in range(paraNum):
        curo = ''
        nexto = ''
        for i in range(len(string)):
            if string[i] ==")":
                nexto = i
                evaluate = string[curo+1:nexto].split()

                if evaluate[1] == 'and':
                    result = andfunc(input_dic[evaluate[0]][1],input_dic[evaluate[2]][1])
                    var = 'variableNumber' + str(j)
                    exec('input_dic[var]= ["null",result]')
                    string = string[0:curo] + var + string[nexto + 1:]
                    
                elif evaluate[1] == 'or':
                    result = orfunc(input_dic[evaluate[0]][1],input_dic[evaluate[2]][1])
                    var = 'variableNumber' + str(j)
                    exec('input_dic[var]= ["null",result]')
                    string = string[0:curo] + var + string[nexto + 1:]

                elif evaluate[1] == 'im':
                    result = imfunc(input_dic[evaluate[0]][1],input_dic[evaluate[2]][1])
                    var = 'variableNumber' + str(j)
                    exec('input_dic[var]= ["null",result]')
                    string = string[0:curo] + var + string[nexto + 1:]

                elif evaluate[0] == 'ne':
                    result = nefunc(input_dic[evaluate[1]][1])
                    var = 'variableNumber' + str(j)
                    exec('input_dic[var]= ["null",result]')
                    string = string[0:curo] + var + string[nexto + 1:]

                elif evaluate[1] == 'ouex':
                    result = ouexfunc(input_dic[evaluate[0]][1],input_dic[evaluate[2]][1])
                    var = 'variableNumber' + str(j)
                    exec('input_dic[var]= ["null",result]')
                    string = string[0:curo] + var + string[nexto + 1:]

                elif evaluate[1] == 'xor':
                    result = xorfunc(input_dic[evaluate[0]][1],input_dic[evaluate[2]][1])
                    var = 'variableNumber' + str(j)
                    exec('input_dic[var]= ["null",result]')
                    string = string[0:curo] + var + string[nexto + 1:]

                elif evaluate[1] == 'bi':
                    result = bifunc(input_dic[evaluate[0]][1],input_dic[evaluate[2]][1])
                    var = 'variableNumber' + str(j)
                    exec('input_dic[var]= ["null",result]')
                    string = string[0:curo] + var + string[nexto + 1:]

                elif evaluate[1] == 'nand':
                    result = nandfunc(input_dic[evaluate[0]][1],input_dic[evaluate[2]][1])
                    var = 'variableNumber' + str(j)
                    exec('input_dic[var]= ["null",result]')
                    string = string[0:curo] + var + string[nexto + 1:]
                #break

            elif string[i] =="(":
                curo = i

    finalValue = input_dic[var][1]
    return finalValue


#inputSettings_____________________________________________________________
def inputSettings(finalInfo, unitTime,locallist,input_dic):
    
    for key in locallist:
        if unitTime == 0:
            input_dic[key][1] = 0
        elif (int(unitTime)%int(input_dic[key][0])) == 0:
            input_dic[key][1] = 0
        elif unitTime%(input_dic[key][0]//2) == 0:
            input_dic[key][1] = 1

#printVariableInformation__________________________________________________
def printVarInfo(finalInfo):
    for j in range(len(finalInfo[0][1])):
        print("The values under column #: " + str(j+1))
        for i in range(finalInfo[-1][0]+1):
            print(finalInfo[i][1][j])
        print()

#printMatrixInformation___________________________________________________
def printResInfo(finalInfo):
    print("Here are the results for the command:")
    for i in range(finalInfo[-1][0]+1):
        print(str(finalInfo[i][2][0]))

#storeInformationInMatrix__________________________________________________
def matrixMake(command, paraNum, endpoint, finalInfo,input_dic):
    currentpoint = 0
    count = 0
    locallist = []
    for key in input_dic.keys():
        if key == 'varialbeNumber0':
            break
        else:
            locallist.append(key)

    for i in range(endpoint//40):
        finalInfo.append([count,[],[]])
        for j in locallist:
            inputSettings(finalInfo, currentpoint,locallist,input_dic)
            finalInfo[count][1].append(input_dic[j][1])
        finalInfo[count][2].append(findParentheses(command,paraNum,input_dic))

        count +=1
        currentpoint += 20

#exportingInformationToExcel_______________________________________________
def exportExcel(importBool, finalInfo):
    '''Loop to ask if they want to export file to excel'''
    given = False
    while given == False:
        ans = input('Do you wish to export this command to excel? y or n: ')
        ans = ''.join(ans.split())
        ans.lower()
        print(ans)
        if ans == 'n':
            given = True
        elif ans == 'y':

            excelDic = {}
            excelColumn = []

            for j in range(len(finalInfo[0][1])):
                    excelDic[str(j+1)] = []
                    for i in range(finalInfo[-1][0]+1):
                        excelDic[str(j+1)].append(finalInfo[i][1][j])

            excelDic['Final'] = []
            for i in range(finalInfo[-1][0]+1):
                excelDic['Final'].append((finalInfo[i][2][0]))
            
            for keys in excelDic.keys():
                excelColumn.append(keys)

            pf = pd.DataFrame(excelDic, columns = excelColumn)
            
            excelfile = (input('Please enter the excel file name: '))
            newFile = (os.path.join((os.path.dirname(os.path.abspath(__file__))), (excelfile + str('.xlsx'))))

            
            '''if os.path.isfile('filename.txt'):
                print ("File exist")
                os.remove(excelfile)'''
            
            check = False
            counter = 1
            while check == False:
                try:
                    pf.to_excel(newFile, index = False, header=True)
                    check = True
                except:
                    newexcelfile = excelfile + str(counter)
                    newFile = (os.path.join((os.path.dirname(os.path.abspath(__file__))), (newexcelfile + str('.xlsx'))))
                    counter += 1
            
            
            given = True


#mainProgram_______________________________________________________________
def me(input_dic,finalInfo,importBool):
    menu = True
    while menu == True:
        input_dic = {}
        finalInfo = []

        command = input("Please input the command: ")
        '(a and b)[a,b]'
        check = True
        counter = 0
        bracketCheck = False

        if '[' in command:
            bracketCheck = True

        while check == True:
            if command[counter] == '[':
                variables = command[counter+1:-1]
                command = command[:counter]
                check = False
            if counter == len(command)-2:
                    check = False
            counter +=1

        if bracketCheck == True:
            variableList = variables.split()
            for i in variableList:
                input_dic[i]= []
        else:
            for i in range(len(command)):
                if command[i] =="(":
                    if command[i+1] != "(":
                        input_dic[command[i+1]] = []
                if command[i] == ")":
                    if command[i-1] !=")":
                        input_dic[command[i-1]] = []

        '''Create the cycles for each variable'''
        offsetin(input_dic)

        '''Detect amount of operations'''
        paraNum = paranumfunc(command)

        '''Simulate every iteration and storing information into input_dic and finalInfo'''
        matrixMake(command, paraNum, endpoint, finalInfo, input_dic)

        '''Go through the different main options'''        
        ask = True
        while ask:
            printOptions = input("Here are the different options\n1 for variable printout\n2 for result printout\n3 for new command\n'end' to stop the program\n->")
            
            if printOptions == '1':
                printVarInfo(finalInfo)
            elif printOptions == '2':
                printResInfo(finalInfo)
                if importBool == True:
                    exportExcel(importBool,finalInfo)
            elif printOptions == '3':
                ask = False
            elif printOptions == 'end':
                ask = False
                menu = False
            else:
                print("You have inputed a wrong option, please select an available option!\n")

#ProgramStartup_____________________________________________________________
def m():
    '''initialize main variable'''
    input_dic = {}
    finalInfo = []
    me(input_dic,finalInfo,importBool)

m()
