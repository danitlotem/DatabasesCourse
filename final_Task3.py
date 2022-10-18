import numpy

#the function calculates the in degrees of all the vertex in graph (transactions)
def calculateDegrees(matrix, N):
    lst=[0]*N
    
    for row in range (N):
        for col in range (N):    
            if(matrix[row][col]==1): #if there is an edge, we add 1 to list of in degrees
                lst[col]+=1
    return lst

#the function appends to Q list all the vertex that have no in edges
def initQueue(inDegrees,N):
    Q=[]
    for i in range (N):
        if i!=0: #we use extra row and col to match the transaction index (logical) to matrix indexes (physical)
            if inDegrees[i]==0:
                Q.append(i)
    
    return Q

#the function update inDegrees and Q lists by removing neighbours edges
def updateDegrees(v,matrix,N,inDegrees,Q):
    for col in range (N): #looping over (V,col) ,col = V optional neighbours
       if matrix[v][col]==1:
           inDegrees[col]-=1
           if inDegrees[col]==0: #if the in degree is 0, we add the vertex to Q
               Q.append(col)

#the function prints the topological sort of graph
def printTopologicalSort(lst):
    print("\nThe topological sort of the transactions graph is:")
    for i in range(len(lst)):
        print(lst[i], end=" ")
        if(i!=len(lst)-1):
            print("->", end=" ")

#the function apply topological sort on transactions matrix
def topologicalSort(matrix, N):
    inDegrees=calculateDegrees(matrix,N) # calculates the in degrees of all the vertex in graph (transactions)
    Q=initQueue(inDegrees, N) #appends to Q list all the vertex that have no in edges
    printLst=[]
    
    while Q:
        v=Q[0]
        printLst.append(v)
        updateDegrees(v,matrix,N,inDegrees,Q)
        Q.pop(0)
    
    for item in inDegrees:
        if item !=0:
            print ("\nNO",end="")
            return
    
    printTopologicalSort(printLst)
    
#the function create matrix of transactions graph edges
def initMatrix(lstOfTransactions,size):
    matrix=numpy.zeros((size, size), dtype=int) #init matrix
    
    for i in range(len(lstOfTransactions)):
        for j in range(i+1,len(lstOfTransactions)):
            if(lstOfTransactions[i][0]=='W' or lstOfTransactions[j][0]=='W'): #at least one of actions has to be write("W")
                if(lstOfTransactions[i][1]!=lstOfTransactions[j][1]): #the indexes have to be different
                    if(lstOfTransactions[i][2]==lstOfTransactions[j][2]): #the actions need to be on the same table
                        row=lstOfTransactions[i][1]
                        col=lstOfTransactions[j][1]
                        matrix[row][col]=1 #add edge to matrix
    return matrix
                 
#the function get schedule from user and remove unnecessary characters       
def getInputFromUser():
    transaction=input("Please enter your Schedule: ")
    if(transaction[-1]==";"):
        transaction=transaction[:-1] #without ; in the end
    transaction=transaction.upper() #the code works on upper case
    transaction="".join(transaction.split()) #delete spaces
    
    return transaction

#the function split every part of transaction and insert it into list - action(R/W), index, table
def buildLst(transaction):
    lstOfTransactions=transaction.split(";")
    listLen=len(lstOfTransactions)
    newLst=[]
    #create nested list of transactions
    for i in range (listLen):
        newLst.append([])
    
    #create list by action(R/W), index, table of each transaction
    i=0
    for item in lstOfTransactions:
        newLst[i].insert(i, item[0])
        newLst[i].append(int(item[1]))
        newLst[i].append(item[2:5])
        i+=1
    
    return newLst

#the function finds the biggest index of transactions for matrix size
def findMaxValueInMatrix(lstOfTransactions):
    maxVal=lstOfTransactions[0][1]
    for item in lstOfTransactions:
        if item[1]>maxVal:
            maxVal=item[1]
            
    return maxVal+1
    
def main():
    transaction=getInputFromUser()
    lstOfTransactions=buildLst(transaction)
    size=findMaxValueInMatrix(lstOfTransactions) 
    matrix=initMatrix(lstOfTransactions,size)    
    topologicalSort(matrix, size)

if __name__ == "__main__":
    main()