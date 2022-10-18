import random
import math
import copy

#general lists for all functions
operList=["PI","SIGMA","CARTESIAN","NJOIN","TJOIN"]
attrList=["R.A","R.B","R.C","R.D","R.E","S.D","S.E","S.F","S.H","S.I"]
tableList=["R","S"]
subOperList=["(SIGMA","(CARTESIAN"]
operators=["<=",">=","<>","<",">","="]
joinedColoumns=["R.D","R.E","S.D","S.E"]
lstOfRules=["4","4a","5a","11b"]

#-----------------------------------------------GENERAL-----------------------------------------------------  
# function find all operators indexes in given predicat and operator name and return lst of operator indexes
def find_operator_indexes (word, sentence):
    index = 0;
    lst=[]
    while index < len(sentence):
        index = sentence.find(word, index)
        if index == -1:
            break
        lst.append(index)
        index += len(word)
    return lst

#the function check if a predicat is valid condition and returns true/false and index of main operator
def is_condition(str,counter):
    resLeft=resRight=False
    resCond=False
    if(is_simple_condition(str)):
        return [True,-1]

    else:
        #build list of operator indexes
        lst_of_AND=find_operator_indexes("AND", str) 
        lst_of_OR=find_operator_indexes("OR", str)
        listOfOperatos=lst_of_AND+lst_of_OR
        
        #splitting the string by operators 
        for oper_index in listOfOperatos:
            if(str[oper_index:oper_index+3]=='AND'):
                wordLen=3
            else:
                wordLen=2
        
            leftStr=(str[0:oper_index-1]).strip()
            rightStr=(str[oper_index+wordLen+1:]).strip()
            resLeft=is_condition(leftStr,counter)
            resRight=is_condition(rightStr,counter)
            
            if(resLeft and resRight):
                return [True,oper_index+counter]
            
        #delete not-needed brackets
        if(str[0]=='(' and str[-1]==')'):
            str=str[1:-1] 
            resCond=is_condition(str,counter+1)            
        
        return resCond
     
#check if simple condition is valid      
def is_simple_condition(str):    
    operVal=""
    
    #delete not-needed brackets
    while(str[0]=='(' and str[-1]==')'):
         str=str[1:-1]
    
    if ("=" in str):
        operVal="="
    if(operVal==""):
        return False
    else:
        newStr=str.split(operVal,1)
        newStr[0]=newStr[0].strip()
        newStr[1]=newStr[1].strip()
        
        res1=is_constant(newStr[0])
        res2=is_constant(newStr[1])
        return (res1 and res2)
       
    return False

#check if str is valid attribute
def is_attribute(str):
    res=False 
    if (str in attrList):
        res=True
        
    return res

#check if str is constant
def is_constant(str):
    #checking what is the type of each constant
    if (str): # if str is not empty
        if(str.isdigit()):
           return True
        elif(is_attribute(str)):
            return True
        elif((str[0]=='\"' and str[-1]=='\"' ) or (str[0]=='\'' and str[-1]=='\'' )):
            return True
    
    return False

#function get list(algebric query) and choice of rule to apply on the algebric query
def applyRule(choice,lst):
    if(choice=="4"):
        lst=rule4(lst)
        printQuery(lst)
    elif(choice=="4a"):
        lst=rule4a(lst)
        printQuery(lst)
    elif(choice=="5a"):
        lst=rule5a(lst)
        printQuery(lst)
    elif(choice=="6"):
        lst=rule6(lst)
        printQuery(lst)
    elif(choice=="6a"):
        lst=rule6a(lst)
        printQuery(lst)
    elif(choice=="11b"):
        lst=rule11b(lst)
        printQuery(lst)
    elif(choice=="-1"):    
        print("Exit")
    else:
        print("invalid choice")  
        
    return lst
#-----------------------------------------------PART 1-----------------------------------------------------

#the function build a list of query parts by given str
def split_str(str):
    queryParts=str.split("FROM")
    queryParts[0]=queryParts[0].replace("SELECT",'')
    selectText=queryParts[0].strip()
    selectText=" ".join(selectText.split()) #remove multiply spaces
    queryParts1=queryParts[1].split("WHERE")
    fromText=queryParts1[0].strip()
    fromText=" ".join(fromText.split())  #remove multiply spaces
    whereText=queryParts1[1].strip()
    whereText=" ".join(whereText.split())  #remove multiply spaces
    # whereText=deleteBrackets(whereText)
    lst=[selectText,fromText,whereText]
    return lst
#---------------------------------------
#funcrion get str and build it's algebric tree
def queryToAlgebric(str):
    lst=split_str(str)
    selectText=lst[0]
    fromText=lst[1]
    whereText=lst[2]
    
    pi="PI["+selectText+"]"
    sigma="SIGMA["+whereText+"]"
    if("," not in fromText):
        fromText=fromText+","+fromText
    cartesian="CARTESIAN("+fromText+")"
    algebric=pi+"("+sigma+"("+cartesian+"))"
    return algebric
#---------------------------------------
#the function build the main list that represent the algebric query
def BuildArray(str):
     mainList=[[],[],[]] #three sub-lists - pi,sigma,cartesian
     i=0
     
     for oper in subOperList:
        #split
        tempIndex=str.find(oper)
        leftStr=str[0:tempIndex]
        
        #build Node
        for item in operList:
            if item in leftStr:
                mainList[i].append(item) 
                tempStr=leftStr.split(item)
                mainList[i].append(tempStr[1])
                i+=1
                break
        str=str[tempIndex:len(str)-1]
     
     mainList[i].append("CARTESIAN") 
     tempStr=str.split("CARTESIAN")
     if("," in tempStr[1]):
         newStr=tempStr[1].split(",")
         temp=newStr[0]
         temp=temp[1:]
         mainList[i].append(temp)   
         temp=newStr[1]
         temp=temp[0:-1]
         mainList[i].append(temp)      
     else:
         mainList[i].append(tempStr[1])  
         mainList[i].append(tempStr[1])  
     return mainList
#---------------------------------------
#the function build node in order to apply rule 4
def BuildNode(oper,str):
    tempList=[]
    tempList.append(oper)
    tempList.append(str.strip())
    return tempList
#---------------------------------------
#the function find node in lst by oper val
def findNode(lst,oper,operVal):
    for item in lst:
        if oper in item[0]:
            if operVal in item[1]:
                return lst.index(item)
    return -1
#---------------------------------------
#the function find main operator in predicat
def findMainOper(str):
    res=is_condition(str,0)
    if(res[0]):
        index=res[1]
        if(str[index]=="A"):
            return [index,"AND"]
        else:
            return [index,"OR"]
#---------------------------------------
#the function delete cover brackets
def deleteBrackets(str):
     while(str[0]=='(' and str[-1]==')'):
         str=str[1:-1]
     return str
#---------------------------------------
#the function check if it can remove unnecessary brackets
def checkBrackets(predicat,mainOper):
    if(is_simple_condition(predicat)):
        predicat=deleteBrackets(predicat)
    leftBrackets=predicat[0:mainOper[0]].count("(")
    rightBrackets=predicat[0:mainOper[0]].count(")")
    
    if leftBrackets==rightBrackets:
        return predicat
    else:
        dif=leftBrackets-rightBrackets
        for i in range(dif):
            predicat=predicat[1:-1]
    return predicat
#---------------------------------------
#applying rule number 4. if it cannot applied, returns original list
def rule4(lst):
    nodeIndex=-1
    nodeIndex=findNode(lst,"SIGMA","AND")#return index of first SIGMA node with AND
    if nodeIndex != -1:
        node=lst[nodeIndex]
        predicat=node[1]
        predicat=predicat[1:-1]
        mainOper=findMainOper(predicat)
       
        if(mainOper[1] == "OR") : #can't apply this rule on query
            return lst
        else:
            predicat=checkBrackets(predicat,mainOper)
            leftStr=predicat[0:mainOper[0]-1]
            leftStr=leftStr.strip()
            rightStr=predicat[mainOper[0]+3:]
            rightStr=rightStr.strip()
           
            leftMainOp=findMainOper(leftStr)
            leftStr=checkBrackets(leftStr,leftMainOp)

            leftStr=leftStr.strip()
            leftStr="["+leftStr+"]"
            rightMainOp=findMainOper(rightStr)
            rightStr=checkBrackets(rightStr,rightMainOp)
            rightStr=rightStr.strip()
            rightStr="["+rightStr+"]"
            
            lst[nodeIndex][1]=leftStr
            newNode=BuildNode("SIGMA",rightStr)
            lst.insert(nodeIndex+1,newNode)
        
    return lst
#---------------------------------------
#applying rule number 4a. if it cannot applied, returns original list
def rule4a(lst):
    for i in range(len(lst)-1):
        if(lst[i][0]==lst[i+1][0] and lst[i][0]=="SIGMA"):
            nextNode=lst.pop(i+1)
            lst.insert(i,nextNode)
    return lst
#---------------------------------------
#print sigma list in node
def printSigma(node):
    count=0
    for i in range(len(node)):
        if(i!=0):
            print("(",end='')
            count+=1
        count+=printNode(node[i])

    print(")" *count,end='')
    return 0
#---------------------------------------
#print cartsian or njoin in node
def PrintCartOrNjoin(node):
    count=0   
    print(node[0]+"(",end='')
    count+=1
    if(type(node[1])==list):
        count+=printNode(node[1])
    else:
        print(node[1],end='')
    print(",",end='')
    if(type(node[2])==list):
        printNode(node[2])
    else:
        print(node[2],end='')
    print(")",end='')
    count-=1
    return count
#--------------------------------------- 
#print node in list         
def printNode(node):
    count=0
    for item in node:
        if (item=="R" or item=="S"):
            print("("+item+")",end='')

        elif(item[0]=="SIGMA"):
            count+=printSigma(node)
            return count
        elif(item=="CARTESIAN" or item=="NJOIN"):
            count+=PrintCartOrNjoin(node)
            return count
        elif(type(item)==list):
            for i in range(len(item)):    
                count+=printNode(item[i])
            return count
        else:
            print(item,end='')
    return count

#---------------------------------------
#print query by algebric tree
def printQuery(lst):   
    count=0
    for item in lst:
        if(type(item)==list):
            count+=printNode(item)
            if(item[0]!="CARTESIAN" and item[0]!="NJOIN"):
                print("(",end='')
                count+=1
    print(")" *count)
#---------------------------------------
#function create list of sigma attributes
def findAllAttributes(sigmaStr):
    sigmaAttrLst=[]
    for item in attrList: #change to attrList
        if (item in sigmaStr):
            sigmaAttrLst.append(item)
            
    return sigmaAttrLst
#---------------------------------------
#function check if all attributes in pi list is from the same table
def isFromSameTable(tempPiList):
    table=((tempPiList[0].split("."))[0]).strip()
    for item in tempPiList:
        if table not in item:
            return False
    return True
#---------------------------------------
#remove spaces between pi attributes
def removeSpaces(PiStr):
    for i in range(len(PiStr)):
        PiStr[i]=PiStr[i].strip()
    return PiStr
#---------------------------------------
#applying rule number 5a. if it cannot applied, returns original list
def rule5a(lst):
    for i in range(len(lst)-1):
        if(lst[i][0]=="PI" and (lst[i+1][0]=="SIGMA")):
            tempPiStr=(lst[i][1])[1:-1]
            if(tempPiStr=="*"):
                tempPilst=attrList
            else:
                tempPilst=tempPiStr.split(",")
                tempPilst=removeSpaces(tempPilst)
            isPiListOK=isFromSameTable(tempPilst)
            if isPiListOK:
                tempSigmaStr=(lst[i+1][1])[1:-1]# sigma predicat
                tempSigmaLst=findAllAttributes(tempSigmaStr)
                for attr in tempSigmaLst:
                    if (attr not in tempPilst):
                        return lst
                #sigma fields in pi fields
                nextNode=lst.pop(i+1)
                lst.insert(i,nextNode)
    return lst
#---------------------------------------
#function doing Function composition for sigmas nodes
def funcComp(inner,outTable,tempSigmaLst):
    tempInner=inner
    while (tempInner[2]!="S" and tempInner[2]!="R"): #not simple table, there is Function composition
        tempInner=tempInner[2]
        
    for attr in tempSigmaLst: #not the same table
        if(tempInner[2] not in attr):
            return [False,inner]
    
    tempList=[]
    tempList.append(outTable)    
    tempList.append(inner)    
    return [True,tempList]
#---------------------------------------
#applying rule number 5a. if it cannot applied, returns original list
def rule6(lst): 
    for i in range(len(lst)-1):
        #IMPLEMENTATION FOR NJOIN
        if((lst[i][0]=="SIGMA") and (lst[i+1][0]=="NJOIN")):
            tempSigmaStr=(lst[i][1])[1:-1]
            tempSigmaLst=findAllAttributes(tempSigmaStr)
            leftTableInJoin=lst[i+1][1]
            for attr in tempSigmaLst:
                if(leftTableInJoin not in attr):
                    return lst
            lst[i].append(leftTableInJoin) #add to sigma
            lst[i+1][1]=lst[i]
            lst.pop(i)
            return lst
        
        # need to be: sigma,sigma,cartesian
        if((i+2<=len(lst)-1) and ((lst[i][0]=="SIGMA") and (lst[i+1][0]=="SIGMA") and (lst[i+2][0]=="CARTESIAN") and (len(lst[i+2])==3))):
            tempSigmaStr=(lst[i+1][1])[1:-1]
            tempSigmaLst=findAllAttributes(tempSigmaStr)
            leftTableInCartesian=lst[i+2][1]
            if(leftTableInCartesian=="R" or leftTableInCartesian=="S"): #check if simple table
                for attr in tempSigmaLst:
                    if(leftTableInCartesian not in attr):
                        return lst
                lst[i+1].append(leftTableInCartesian)
                lst[i+2][1]=lst[i+1]
                lst.pop(i+1)
                return lst
            else:
                leftTableInCartesian=funcComp(leftTableInCartesian,lst[i+1],tempSigmaLst)
                if(leftTableInCartesian[0]==True):
                    lst[i+2][1]=leftTableInCartesian[1]
                    lst.pop(i+1)
                return lst
    
    return lst
#---------------------------------------
#applying rule number 5a. if it cannot applied, returns original list
def rule6a(lst): 
    for i in range(len(lst)-1):
        #IMPLEMENTATION FOR NJOIN
        if((lst[i][0]=="SIGMA") and (lst[i+1][0]=="NJOIN")):
            tempSigmaStr=(lst[i][1])[1:-1]
            tempSigmaLst=findAllAttributes(tempSigmaStr)
            rightTableInJoin=lst[i+1][2]
            for attr in tempSigmaLst:
                if(rightTableInJoin not in attr):
                    return lst
            
            lst[i].append(rightTableInJoin) #add to sigma
            lst[i+1][2]=lst[i]
            lst.pop(i)
            return lst
        
        # need to be: sigma,sigma,cartesian
        if((i+2<=len(lst)-1) and ((lst[i][0]=="SIGMA") and (lst[i+1][0]=="SIGMA") and (lst[i+2][0]=="CARTESIAN") and (len(lst[i+2])==3))):
            tempSigmaStr=(lst[i+1][1])[1:-1]
            tempSigmaLst=findAllAttributes(tempSigmaStr)
            rightTableInCartesian=lst[i+2][2]
            if(rightTableInCartesian=="R" or rightTableInCartesian=="S"):#check if simple table
                for attr in tempSigmaLst:
                    if(rightTableInCartesian not in attr):
                        return lst        
                lst[i+1].append(rightTableInCartesian)
                lst[i+2][2]=lst[i+1]
                lst.pop(i+1)
                return lst
            else:
              rightTableInCartesian=funcComp(rightTableInCartesian,lst[i+1],tempSigmaLst)
              if(rightTableInCartesian[0]==True):
                  lst[i+2][2]=rightTableInCartesian
                  lst.pop(i+1)
              return lst

    return lst
#---------------------------------------
#check if function can replace operator to njoin
def isGoodToNaturalJoin(predicat,mainOper):
    predicat=deleteBrackets(predicat)
    leftStr=deleteBrackets(predicat[0:mainOper[0]-1])
    rightStr=deleteBrackets(predicat[mainOper[0]+3:])
    
    if(("=" not in leftStr) or("=" not in rightStr)):
        return False
    else:
        leftLst=leftStr.split("=")
        tempLeft=leftLst[0].split(".")
        tempRight=leftLst[1].split(".")
        if(not(tempLeft[0]!=tempRight[0] and tempLeft[1]==tempRight[1])):
            return False
        
        rightLst=rightStr.split("=")
        tempLeft=rightLst[0].split(".")
        tempRight=rightLst[1].split(".")
        if(not(tempLeft[0]!=tempRight[0] and tempLeft[1]==tempRight[1])):
            return False
    return True     
#---------------------------------------
#applying rule number 11b. if it cannot applied, returns original list
def rule11b(lst):
    for i in range(len(lst)-1):
        if(lst[i][0]=="SIGMA" and (lst[i+1][0]=="CARTESIAN")):
            #CHECK PREDICAT
            tempSigmaStr=(lst[i][1])[1:-1]
            tempSigmaLst=findAllAttributes(tempSigmaStr)
            #CHECK IF NOT ALL JOINS ATTR IN PREDICAT
            for attr in joinedColoumns:
                if(attr not in tempSigmaLst): 
                    return lst
            mainOper=findMainOper(tempSigmaStr)
            if(mainOper[1]=="OR"):
                return lst
            predicat=isGoodToNaturalJoin(tempSigmaStr,mainOper)
            if(predicat):
                lst[i+1][0]="NJOIN"
                lst.pop(i)
            
    return lst          
#-----------------------------------------------PART 2-----------------------------------------------------
#function random rules to apply on querys, and return 4 trees
def createRandomTrees(str):
    lst=[[],[],[],[]]
    ruleList=[]
    lst[0]=BuildArray(str)
    lst[1]=BuildArray(str)
    lst[2]=BuildArray(str)
    lst[3]=BuildArray(str)
    index=1
    for tree in range(4):
        for i in range(10):
            ruleList.append(random.choice(lstOfRules))
        
        for i in range(10):    
            print("rule number "+ruleList[i]+" is applied")
            lst[tree]=applyRule(ruleList[i], lst[tree]) 
            print("\n")
        ruleList.clear()
        print("---------------ANOTHER TREE---------------")
    
    print("FINAL Trees:\n ")
    for item in lst:
        print("Tree number"+repr(index)+":")
        printQuery(item)
        print("\n")
        index+=1
    return lst
#-----------------------------------------------PART 3-----------------------------------------------------
#function buils R and S lists with parameters: R_R,N_R,V(A),V(B) and etc.
def buildList(tempList,tableName):
    lst=[[],[],[]]
    if(tableName=="R"):
        lst[0]=["R_R",20] #ADD CONST R_R 
    else:
        lst[0]=["R_S",20] #ADD CONST R_R 

    for i in range(2,len(tempList)):
        tempRow=tempList[i].split('=')
        tempRow[0]=tempRow[0].strip()
        tempRow[1]=tempRow[1].strip()
        tempRow[1]=int(tempRow[1])
        if(i<=2):
            lst[1]=tempRow
        else: 
            lst[2].append(tempRow)
    return lst
#---------------------------------------
#main function that estimate query memory cost
def sizeEstimation(lst):
    i=1
    j=1
    first=1
    lstR=[]
    lstS=[]
    preOutput=[[],[]]
    file=open("statistics.txt")
    cont=file.readlines()
    tempList=cont[0:8]
    lstR=buildList(tempList,"R")
    tempList=cont[9:-1]
    lstS=buildList(tempList,"S")
    
    for tree in lst: 
        print("---------------Tree:"+repr(j)+"---------------")
        for node in reversed(tree):
            print(node[0])
            if(not first):
                print("input: "+"n_Scheme"+repr(i-1)+"="+repr(preOutput[1][1])+" R_Scheme"+repr(i-1)+"="+repr(preOutput[0][1]))
            if(node[0]=="SIGMA"):
                preOutput=estimateSIGMA(node,preOutput,lstR,lstS)
                first=0
            elif(node[0]=="PI"):
                preOutput=estimatePI(node,preOutput,lstR,lstS)
                first=0
            elif(node[0]=='CARTESIAN'):
                preOutput=estimateCARTESIAN(node,preOutput,lstR,lstS)
                first=0
            elif(node[0]=='NJOIN'):
                preOutput=estimateNJOIN(node,preOutput,lstR,lstS)
                first=0
        
            print("output: "+"n_Scheme"+repr(i)+"="+repr(preOutput[1][1])+" R_Scheme"+repr(i)+"="+repr(preOutput[0][1])+"\n")
            i+=1
        j+=1
        i=1
        first=1
        preOutput=[[],[]]
      
    return preOutput
#---------------------------------------  
#function calaculate v value   
def caculateV(simplePredicat,lstR,lstS): 
    # (R).(A)=(S).(E)   ||  R.A=10
    Vright=0
    Vleft=0
    twoTables=False
    temp=(simplePredicat.split("=")) #[R.A],[S.E]
    tempLeft=temp[0].split(".")      # [[R],[A]]
    tempRight=temp[1]                #[S.E]
    tableLeft=tempLeft[0].strip()    #[R]
    colLeft=tempLeft[1].strip()      #[A]
    
    #case of table.col=table.col
    if "." in tempRight:
        tempRight=tempRight.split(".") #[[S],[E]]
        tableRight=tempRight[0]        #[S]
        colRight=tempRight[1]          #[E]
        twoTables=True
    
    if twoTables:         
        if tableLeft==tableRight: #R.? = R.? OR S.? = S.?
            if tableLeft=='R':
                Vlist=lstR[2]
            else:
                Vlist=lstS[2]
            for item in Vlist:
                if(colLeft in item[0]):
                    Vleft=item[1]
                if(colRight in item[0]):
                    Vright=item[1]
            return max(Vleft,Vright)
        else:                       # R.? = S.?
            if tableLeft=='R': 
                VlistLeft=lstR[2]
                VlistRight=lstS[2]
            else: 
                VlistLeft=lstS[2]
                VlistRight=lstR[2]                
            
            for item in VlistLeft:
                if(colLeft in item[0]):
                    Vleft=item[1]
            for item in VlistRight:
                if(colRight in item[0]):
                    Vright=item[1]
            return max(Vleft,Vright)
    else:                           #R.? = CONST OR S.? = CONST  --> one table - one V
        if(tableLeft=='R'):
            Vlist=lstR[2]
        else: 
            Vlist=lstS[2]
        for item in Vlist:
            if(colLeft in item[0]):
                return (item[1])
    return -1   
#--------------------------------------- 
#function check if simple condition (no oprator)       
def simpleCondition(predicat):
    if(("AND" not in predicat) and ("OR" not in predicat)):
        return True
    return False
#---------------------------------------    
#function update v value - not in use, written before lecture update
def updateV(sigmaProb,lstR,lstS):
    for item in lstR[2]:
        item[1]=math.ceil(item[1]*sigmaProb)
    for item in lstS[2]:
        item[1]=math.ceil(item[1]*sigmaProb)
#--------------------------------------- 
#recursive func that estimate sigma memory cost 
def sigmaRec(predicat,lstR,lstS):
    if(simpleCondition(predicat)):
        return caculateV(predicat,lstR,lstS)  

    op=findMainOper(predicat)
    predicat=checkBrackets(predicat,op)
    op=findMainOper(predicat)
    tempL=(predicat[0:op[0]-1]).strip()
    opL=findMainOper(tempL)
    tempL=checkBrackets(tempL,opL)
    tempR=(predicat[op[0]+3:]).strip()
    opR=findMainOper(tempR)
    tempR=checkBrackets(tempR,opR)

    right=sigmaRec(tempR,lstR,lstS)
    left=sigmaRec(tempL,lstR,lstS)
    
    if(op[1]=='AND'):
        return (right)*(left)
    else: #not support in or operator - not in use,written before lecture update
        return ((right)+(left))
#---------------------------------------      
#main func to estimate sigma memory cost   
def estimateSIGMA(node,preOutput,lstR,lstS):
    #R-size of rows - STAY THE SAME
    predi=(node[1])[1:-1]
    sigmaProb=1/sigmaRec(predi,lstR,lstS)
    preOutput[1][1]= math.ceil(sigmaProb*preOutput[1][1])
    #updateV(sigmaProb,lstR,lstS)
    return preOutput  
#---------------------------------------
#main func to estimate pi memory cost   
def estimatePI(node,preOutput,lstR,lstS):
    if("*" in node[1]):
        lstOfPi=attrList
    else:
        lstOfPi=node[1].split(",")
    size=len(lstOfPi)*4
    preOutput[0][1]=size
    
    return preOutput
#---------------------------------------
#sub function to calculate carteisan
def calculateCartesian(index,node,preOutput,lstR,lstS):
    if(node[index][0]=="SIGMA"):
        if(len(node[index])==3 and node[index][2]=="R"): #left table is sigma
            setPreoutput(lstR[0][1],lstR[1][1],preOutput)
        if(len(node[index])==3 and node[index][2]=="S"): #right table is sigma
            setPreoutput(lstS[0][1],lstS[1][1],preOutput)
        res=(estimateSIGMA(node[index],preOutput,lstR,lstS)).copy()
        
    elif(node[index][0]=="PI"):
        res=estimatePI(node[index],preOutput,lstR,lstS)
    elif(node[index][0]=='CARTESIAN'):
        res=estimateCARTESIAN(node[index],preOutput,lstR,lstS)
    elif(node[index][0]=='NJOIN'):
        res=estimateNJOIN(node,preOutput,lstR,lstS)
    return res.copy()
#---------------------------------------
#update preoutput n_R, n_S, R.R, R.S
def setPreoutput(sizeRXS,numRxS,preOutput):
        if(not preOutput[0] and not preOutput[1]):
            preOutput[0].append("Rscheme")
            preOutput[1].append("Nscheme")
            preOutput[0].append(sizeRXS)
            preOutput[1].append(numRxS)
        else: 
            preOutput[0][1]=sizeRXS
            preOutput[1][1]=numRxS
        return preOutput
#---------------------------------------
#main func to estimate cartesian memory cost
def estimateCARTESIAN(node,preOutput,lstR,lstS):
    # NOTICE! in class lectures we have been told that there will be always two different tables. 
    preOutput1=[[],[]]
    preOutput2=[[],[]]
    if(node[1][0] in operList):#left table
        preOutput1=copy.deepcopy(calculateCartesian(1,node,preOutput,lstR,lstS))
        
    if(node[2][0] in operList):#right table
        preOutput2=calculateCartesian(2,node,preOutput,lstR,lstS)
                                      
    # 1) R-size of rows  2)N- num of rows  
    if((not preOutput1[0]) and (not preOutput2[0])): #no operator
        print("input: "+lstR[1][0]+"="+repr(lstR[1][1])+" "+lstS[1][0]+"="+repr(lstS[1][1])+" "+lstR[0][0]+"="+repr(lstR[0][1])+" "+lstS[0][0]+"="+repr(lstR[0][1]))
        sizeRXS=lstR[0][1]+lstS[0][1]
        numRxS=lstR[1][1]*lstS[1][1]
  
    elif((not preOutput1[0]) and preOutput2[0] != ''): #operator only in preOutput2
        print("input: "+lstR[1][0]+"="+repr(lstR[1][1])+" "+lstS[1][0]+"="+repr(lstS[1][1])+" "+lstR[0][0]+"="+repr(lstR[0][1])+" "+lstS[0][0]+"="+repr(lstR[0][1]))
        if(node[1][0]=='R'):
            sizeRXS=lstR[0][1]+preOutput2[0][1]
            numRxS=lstR[1][1]*preOutput2[1][1]
        else:
            sizeRXS=lstS[0][1]+preOutput2[0][1]
            numRxS=lstS[1][1]*preOutput2[1][1]
    
    elif((not preOutput2[0]) and preOutput1[0] != ''):#operator only in preOutput1
        print("input: "+lstR[1][0]+"="+repr(lstR[1][1])+" "+lstS[1][0]+"="+repr(lstS[1][1])+" "+lstR[0][0]+"="+repr(lstR[0][1])+" "+lstS[0][0]+"="+repr(lstR[0][1]))
        if(node[2][0]=='R'):
            sizeRXS=lstR[0][1]+preOutput1[0][1]
            numRxS=lstR[1][1]*preOutput1[1][1]
        else:
            sizeRXS=lstS[0][1]+preOutput1[0][1]
            numRxS=lstS[1][1]*preOutput1[1][1]
    else:#both with operator
        print("input: "+lstR[1][0]+"="+repr(lstR[1][1])+" "+lstS[1][0]+"="+repr(lstS[1][1])+" "+lstR[0][0]+"="+repr(lstR[0][1])+" "+lstS[0][0]+"="+repr(lstR[0][1]))
        sizeRXS=preOutput1[0][1]+preOutput2[0][1]
        numRxS=preOutput1[1][1]*preOutput2[1][1]
            
    preOutput=setPreoutput(sizeRXS,numRxS,preOutput)
    return preOutput        
#---------------------------------------
#main func to estimate njoin memory cost
def estimateNJOIN(node,preOutput,lstR,lstS):
    predicat="[R.D=S.D AND R.E=S.E]"
    sigNode=["SIGMA",predicat]
    carNode=["CARTESIAN",'R','S']
    pre1=estimateCARTESIAN(carNode,preOutput,lstR,lstS)
    pre2=estimateSIGMA(sigNode,pre1,lstR,lstS)
    
    return pre2    
#---------------------------------------
#function get query from user and build list that represent algebric tree
def getQueryInput():
    str=input("Please enter a query:")
    newStr=queryToAlgebric(str)
    lst=BuildArray(newStr)
    return [lst,newStr]
#---------------------------------------
#run part 1
def part1(isPart1):
    choice='0'
    queryRes=getQueryInput()
    while(choice!='-1'):
        choice=input("Please choose the rule you want to apply:\n4, 4a, 5a, 6, 6a, 11b\nfor exit press -1\n\nchoice:")
        lst=queryRes[0]
        lst=applyRule(choice,lst)
#---------------------------------------
#run part 2
def part2():
    queryRes=getQueryInput()
    print("\n")
    lstOfRandomTrees=createRandomTrees(queryRes[1])
    return lstOfRandomTrees
#---------------------------------------
#run part 3
def part3():
    lstOfRandomTrees=part2()
    sizeEstimation(lstOfRandomTrees)
#---------------------------------------
def main():
   choicePart1=0
   cont=0
#----------------------------------------------------------------MENU
   while(cont!='-1'):
        partSelect=input("Please choose the part you want to run:\n1- Part 1  , 2- Part 2  , 3- Part 3  (-1)- exit\nPart: ")
        if(partSelect=="1"):
            print("------------------------PART 1-------------------------")
            while(choicePart1!='0'):
                part1(True)
                choicePart1=input("Do you want to continue in part 1 with new query?  1-yes, 0-no\n")
        elif(partSelect=="2"):
            print("------------------------PART 2-------------------------")
            part2()
        else:
            print("------------------------PART 3-------------------------")
            part3()

if __name__=="__main__":
    main()
    